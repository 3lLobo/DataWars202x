import turtle

base = "2024/oqdrachtx/Verdediging_7/Galactic Trench War (pt. 1)/"

with open(base + "input.txt", "r") as fin:
    lines = fin.readlines()

scale = 1

lookup_table = {"N": 90, "O": 0, "Z": 270, "W": 180}
total = 0

turtle.delay(0)  # this apparently speeds up the turtle by A LOT

for line in lines:
    d, steps = line.split(" ")

    turtle.setheading(lookup_table[d])
    turtle.forward(int(steps.strip("\n")) * scale)
    # turtle was checked if there were overlapping trenches; there weren't so we could just count the amount of steps for this answer.

    total += int(steps.strip("\n"))

print(f"m2 needed: {total}")
input()  # dont close our turtle drawing.
