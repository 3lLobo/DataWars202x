import math

base = "2024/oqdrachtx/Aanval_2/Rocket Equation (pt. 2)/"

with open(base + "input.txt", "r") as f:
    lines = f.readlines()


def get_total_fuel(fuel):
    req = math.floor(fuel / 3) - 2
    if req < 0:
        return 0
    return req + get_total_fuel(req)


sum = 0
for line in lines:
    sum += get_total_fuel(int(line.strip("\n")))

print(f"Total sum is: {sum}")
