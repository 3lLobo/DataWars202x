# Not used for the submission but matches what was submitted.
# Potential answer: 3076 - matches what was submitted

from shapely.geometry import Polygon
import matplotlib.pyplot as plt

file = "excercises/def_7/input.txt"

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


# Plot for the pretty.
plt.scatter(x=[i[0] for i in coords], y=[i[1] for i in coords])
plt.savefig("excercises/def_7/test.png")

# Aka, "python, do the thing".
pgon = Polygon(coords)
print(f"flag: {round(pgon.length)}")
