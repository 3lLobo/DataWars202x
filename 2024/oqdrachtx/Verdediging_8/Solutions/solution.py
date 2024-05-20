# !!!Not submitted!!!
# Potential answer: 52305

from shapely.geometry import Polygon
import matplotlib.pyplot as plt

file = "excercises/def_8/Galactic Trench War (pt. 2)/input.txt"

coords = [(0,0)]
with open(file) as fh:
    for idx, line in enumerate(fh):
        line = line.strip()
        direction, count = line.split(" ")
        count = int(count)
        last_coords = coords[-1]
        if direction == "W":
            coords.append((last_coords[0] + count , last_coords[1]))
        elif direction == "O":
            coords.append((last_coords[0] - count , last_coords[1]))
        elif direction == "N":
            coords.append((last_coords[0], last_coords[1] - count))
        elif direction == "Z":
            coords.append((last_coords[0], last_coords[1] + count))
        else:
            raise Exception(f"damn: {direction}")


# Aka, "python, do the thing".
pgon = Polygon(coords)
print(f"flag: {round(pgon.area)}")

# Little test using my infantile geometry knowledge..
x = [0,5,5,0,-2,-2]
y = [0,0,5,5, 5, 0]
plt.scatter(x=x, y=y)
# For visual inspection
plt.savefig("excercises/def_8/Galactic Trench War (pt. 2)/test_square.png")
pgon = Polygon(zip(x,y))
# Magical.
print(pgon.area == (5*5 + 2*5))
plt.clf()

# And a beautiful triangle to keep testing.
x = [0,13,5]
y = [0,0,5]
plt.scatter(x=x, y=y)
plt.savefig("excercises/def_8/Galactic Trench War (pt. 2)/test_triangle.png")
pgon = Polygon(zip(x,y))
# Good enough for me, I trust the library with my life...
print(pgon.area == 32.5)

