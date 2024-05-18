import sys

# because of the fill recursion, the limit should be quite high...
sys.setrecursionlimit(50_000)

base = "2024/oqdrachtx/Verdediging_8/Galactic Trench War (pt. 2)/"

with open(base + "input.txt", "r") as fin:
    lines = fin.readlines()

def insert(trench_rows, x, y):
    if x < 0:
        for trench_row in trench_rows:
            trench_row.insert(0, ".")

        return insert(trench_rows=trench_rows, x=x + 1, y=y)
    elif x >= len(trench_rows[0]):
        for trench_row in trench_rows:
            trench_row.append(".")
        return insert(trench_rows=trench_rows, x=x, y=y)
    elif y < 0:
        new_row = ["."] * len(trench_rows[0])
        trench_rows.insert(0, new_row)
        return insert(trench_rows=trench_rows, x=x, y=y + 1)

    elif y >= len(trench_rows):
        new_row = ["."] * len(trench_rows[0])
        trench_rows.append(new_row)
        return insert(trench_rows=trench_rows, x=x, y=y)

    trench_rows[y][x] = "#"

    return trench_rows, x, y


def get_left_top(trench_rows):
    for y, row in enumerate(trench_rows):
        for x, col in enumerate(row):
            if col == "#":
                return x + 1, y + 1


def fill(trench_rows, x, y):
    try:
        cell = trench_rows[y][x]
    except IndexError:
        return

    if cell == "#":
        return

    trench_rows[y][x] = "#"

    fill(trench_rows, x + 1, y)
    fill(trench_rows, x - 1, y)
    fill(trench_rows, x, y + 1)
    fill(trench_rows, x, y - 1)

    return trench_rows

total = 0

trench_rows = [[]]
y = 0
x = 0

for line in lines:
    d, steps = line.split(" ")

    for step in range(int(steps.strip("\n"))):
        if d == "N":
            y -= 1
        elif d == "O":
            x += 1
        elif d == "Z":
            y += 1
        elif d == "W":
            x -= 1
        trench_rows, x, y = insert(trench_rows=trench_rows, x=x, y=y)

ltx, lty = get_left_top(trench_rows)
fill(trench_rows, ltx, lty)

for row in trench_rows:
    total += row.count("#")

    print("".join(row))
print()

print(f"m2 need: {total}")

with open(base+"../Solutions/visual_ouput.txt", 'w') as f:
    for row in trench_rows:
        f.write(f"{"".join(row)}\n")
