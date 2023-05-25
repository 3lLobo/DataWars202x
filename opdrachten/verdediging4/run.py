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

def main():

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

# Whats the highet number in the most occuring color? -> N

def get_color(image: np.ndarray) -> str:
    """
    Get the most occuring color from image in hex format with cv2.
    Exclude black.
    Args:
        image (np.ndarray): The image to get the color from.
    Returns:
        The color in hex format.
    """
    




# How offten does N occure? -> X

# What is the most occuring color for the most occuring number? -> Y


if __name__ == "__main__":
    main()