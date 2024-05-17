import math

base = "2024/oqdrachtx/Aanval_1/Rocket Equation (pt. 1)/"

with open(base + "input.txt", "r") as f:
    lines = f.readlines()

sum = 0
for line in lines:
    sum += math.floor(int(line.strip("\n")) / 3) - 2

print(f"Total sum is: {sum}")
