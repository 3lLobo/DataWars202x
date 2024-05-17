# light-weight image processing library
from PIL import Image
# (Advanced) processing of (multi)dimensional arrays 
import numpy as np

# Loop across images printing any image that has a pixel color that differs from what was seen before.
types = []
for image in range(0, 1000):
    new_image = f"opdrachten/intel2_Supernova/input/{image}.png"
    new_image = Image.open(new_image)
    # use set() to get the unique pixel colors
    new_image = set(new_image.getdata())
    if new_image in types:
        # Colors have been seen before. ignore.
        pass
    else:
        # Something novel and maybe interesting.
        print(image, new_image)
        types.append(new_image)

# Two types seen, the first (creating a baseline) and 937 which has a new pixel color - something reddish
#0 {(255, 243, 109), (0, 0, 0), (173, 216, 0), (255, 255, 255)}
#937 {(255, 243, 109), (255, 127, 80), (0, 0, 0), (173, 216, 0), (255, 255, 255)}

# At this point Paint can be used to get the target pixel(s)

target_color = (255, 127, 80)
target_image = 937
target = f"opdrachten/intel2_Supernova/input/{target_image}.png"
target = Image.open(target)

im  = np.array(target)
# Get X and Y coordinates of all blue pixels
Y, X = np.where(np.all(im==target_color,axis=2))

# all x, y coordinates 
# How many times was the pixel seen in the image:
print(len(X)) # once.
# Were:
print(X[0],Y[0])
# 439 x 413

# Answer = image id * pixel cordinates
target_image * X[0] * Y[0]
# Result: correct! 🎉