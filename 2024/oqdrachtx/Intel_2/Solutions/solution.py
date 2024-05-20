# Solution: 15840484
# Result: Correct

from PIL import Image

f1 = "excercises/intel_2/Echo Pixel/sat1.png"
f2 = "excercises/intel_2/Echo Pixel/sat2.png"

im = Image.open(f1)
im2 = Image.open(f2)

# Get the dimensions of an image
x_max, y_max = im.size
print(x_max, y_max)

# Load pixels
pixels1 = im.load()
pixels2 = im2.load()
for row_index in range(x_max):
    for col_index in range(y_max):
        if pixels1[row_index, col_index] != pixels2[row_index, col_index]:
            print("HIT!", row_index, col_index)
            # Lazy way to break out of both loops
            raise Exception(f"Flag: {row_index * 10000 + col_index}")
        col_index += 1
    row_index += 1

