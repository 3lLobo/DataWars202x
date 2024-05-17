import pandas as pd
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from typing import List
import requests
import PIL

# 1. Load images
base_path = os.path.dirname(os.path.abspath(__file__))
images_path = os.path.join(base_path, 'input')

base_url = "http://localhost:9993"
    
def load_images(i_layer: int):
    """
    Load images from the input folder.

    Args:
        i_layer (int): The number of the layer - 0-5.
    Returns a list of images.
    """
    images = []
    layer_path = os.path.join(images_path, str(i_layer))
    for filename in os.listdir(layer_path):
        img = cv2.imread(os.path.join(layer_path, filename))
        if img is not None:
            images.append(img.tolist())
    return images

def load_pil(i_layer: int):
    """
    Load images from the input folder.

    Args:
        i_layer (int): The number of the layer - 0-5.
    Returns a list of images.
    """
    images = []
    layer_path = os.path.join(images_path, str(i_layer))
    for filename in os.listdir(layer_path):
        img = PIL.Image.open(os.path.join(layer_path, filename))
        if img is not None:
            images.append(img)
    return images

def load_raw_images(i_layer: int):
    """
    Get the raw images from the input folder.
    """
    images = []
    numbers = []
    layer_path = os.path.join(images_path, str(i_layer))
    for filename in os.listdir(layer_path):
        with open(os.path.join(layer_path, filename), 'rb') as f:
            images.append(f.read())
            res = requests.post('http://localhost:9993/get_text', files={'image': f.read()})
            numbers.append(res.json()['text'])
    return images, numbers

def glue_images(images: List):
    """
    return one image of all the images glued together.
    the first being on the left and the last on the right.
    """
    return np.concatenate(images, axis=1)

def get_text(i_layer: int, batch_size: int = 256) -> List:
    """
    Load a batch of images from the layer folder and send it to the /get_text_batch endpoint.

    Args:
        i_layer (int): The number of the layer - 0-5.
        batch_size (int): The batch size to send to the endpoint.
    Returns:
        List of text from the images.
    """
    numbers = []
    layer_path = os.path.join(images_path, str(i_layer))
    len_layer = len(os.listdir(layer_path))

    for i in range(0, len_layer, batch_size):
        batch = []
        for filename in os.listdir(layer_path)[i:i+batch_size]:
            with open(os.path.join(layer_path, filename), 'rb') as f:
                batch.append(f.read())
        image_batch = zip(['images'] * len(batch), batch)
        response = requests.post(base_url + "/get_text_batch", files=image_batch)
        numbers.extend(response.json()['texts'])            
            
    # for filename in os.listdir(layer_path):
    #     with open(os.path.join(layer_path, filename), 'rb') as f:
    #         res = requests.post('http://localhost:9993/get_text', files={'image': f.read()})
    #         numbers.append(res.json()['text'])
    return numbers
    
def get_text_recognition(image_list: List, batch_size: int = 256):
    """
    Send the list of images to the /get_text_batch endpoint.
    server is on localhost:9993

    Args:
        image_list (List): List of images.
    Returns:
        List of text from the images.
    """
    url = base_url + "/get_text_batch_cv2"
    texts = []
    for i in range(0, len(image_list), batch_size):
        batch = image_list[i:i+batch_size]
        # batch = zip(['images'] * len(batch), batch)

        image_batch = {'images': batch}
        response = requests.post(url, json=image_batch)
        try:
          texts.extend(response.json()['texts'])
          print(response.json()['texts'])
        except:
          print(response.json())
    return texts

def save_numbers(numbers: List, i_layer: int):
    """
    Save the numbers to a file.
    """
    with open(os.path.join(base_path, str(i_layer) + '_numbers.txt'), 'w') as f:
        f.write('\n'.join(numbers))

def get_numbers():

  i = 1
  # raw_images = load_pil(i)
  raw_images = load_images(i)

  for i in range(6):
    images = load_images(i)
    print('N images:', len(images))
    texts = get_text_recognition(images, batch_size=128)
    # print(texts)
    save_numbers(texts, i)
    print(i, ' done!')

  # _, numbers = load_raw_images(i)
  # numbers = get_text(i)
  # print(numbers)

def load_numbers(i_layer: int):
    """
    Load the numbers from a file.
    """
    with open(os.path.join(base_path, str(i_layer) + '_numbers.txt'), 'r') as f:
        numbers = f.read().split('\n')
    numbers = [int(n) for n in numbers]
    numbers = np.array(numbers)
    return numbers

# Whats the highet number in the most occuring color? -> N

def get_color(image: List) -> str:
    """
    Get the most occuring color from image, return in hex format.
    Flatten the image, filter for triples which are not [0, 0, 0].
    Exclude black.
    Args:
        image (np.ndarray): The image to get the color from.
    Returns:
        The color in hex format.
    """
    image = np.array(image)
    image = image.reshape(-1, 3)
    df_image = pd.DataFrame(image, columns=['r', 'g', 'b'])
    df_image['hex'] = df_image.apply(lambda x: '#%02x%02x%02x' % (x['r'], x['g'], x['b']), axis=1)
    # for color, count in df_image['hex'].value_counts().items():
    #     print(color, count)
    # remove black]
    df_image = df_image[df_image['hex'] != '#000000']
    color = df_image['hex'].value_counts().index[0]
    return color
        

def get_color_numbers_df(i_layer: int)-> pd.DataFrame:
    """
    create a dataframe with a dict where the key is color_number and value is the count of number occurence per color.
    """
    numbers = load_numbers(i_layer)
    images = load_images(i_layer)
    colors = [get_color(image) for image in images]
    df = pd.DataFrame({'numbers': numbers, 'colors': colors})
    return df


def get_n_x(i_layer: int) -> List:
    df_cn = get_color_numbers_df(i_layer)
    most_common_color = df_cn['colors'].value_counts().index[0]
    print('Most common color:', most_common_color)
    df_cn_mc = df_cn[df_cn['colors'] == most_common_color]
    # most occuring number
    n = df_cn_mc['numbers'].value_counts().index[0]
    # most occuring number count
    x = df_cn_mc['numbers'].value_counts().values[0]
    return n, x
  


# How offten does N occure? -> X ✅

# What is the most occuring color for the most occuring number? -> Y

def most_common_color(i_layer: int) -> str:
    """
    Get the most occuring color count from the most occuring number.
    """
    df_cn = get_color_numbers_df(i_layer)
    most_common_number = df_cn['numbers'].value_counts().index[0]
    print('Most common number:', most_common_number)
    df_cn_mc = df_cn[df_cn['numbers'] == most_common_number]
    # most occuring color
    color = df_cn_mc['colors'].value_counts().index[0]
    color_count = df_cn_mc['colors'].value_counts().values[0]
    print('Most common color:', color, '\tcount:', color_count)
    return color_count

def main():
    i_cost = []
    for i in range(6):
        print('Layer:', i)
        n,x = get_n_x(i)
        y = most_common_color(i)
        print('n:', n, '\tx:', x, '\ty:', y)
        cost = n * x * y
        i_cost.append(cost)
    #  sum of all costs
    flag = np.sum(i_cost)
    print('Flag:', flag)


if __name__ == "__main__":
    main()