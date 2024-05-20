# Never submitted and untested.

import pandas as pd

# Should be 35
example = """
[-, #, #, #, #, -]
[#, -, -, #, #, -]
[-, #, -, -, -, -]
[-, -, -, -, -, -]
""".strip().replace("[", "").replace("]", "")

clean = [row.split(", ") for row in example.split("\n")]

df = pd.DataFrame(clean)
col_counts = df.eq("#").sum(axis=0)
# There are 4 rows, so 4 units.
flag = ""
for target_val in reversed(range(1, len(clean)+1)):
    flag += str(sum(col_counts >= target_val))

# Woohoo.
print(int(flag) == 35)


# Now for real.
file = "excercises/def_5/Ruimtepuin (pt. 1)/ruimtepuin_B.txt"

with open(file, "r") as fh:
    data = fh.read().strip().replace("[", "").replace("]", "")

# Small adjustment, the demo has extra spaces, this doesnt.
clean = [row.split(",") for row in data.split("\n")]

df = pd.DataFrame(clean)
col_counts = df.eq("#").sum(axis=0)
# There are 4 rows, so 4 units.
flag = ""
for target_val in reversed(range(1, len(clean)+1)):
    flag += str(sum(col_counts >= target_val))

print(f"Flag: {int(flag)}")
