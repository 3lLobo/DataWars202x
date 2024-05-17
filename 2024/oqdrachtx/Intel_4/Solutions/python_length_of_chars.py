import math

base = "2024/oqdrachtx/Intel_4/Keylog (pt. 1)/"

with open(base + "access_log.txt", "r") as f:
    lines = f.readlines()

after_dict = {}

# the first line is useless so skip it -> afterwards ACCESS GRANTED must be within the targeted lines (2 lines per code; so i + 1).
# the code is always -15:-9 from the back of the log string.
for i in range(1, len(lines), 2):
    if "ACCESS GRANTED" not in lines[i + 1]:
        continue

    code = lines[i][-15:-9]

    for entry_index, entry in enumerate(code):
        after_dict[entry] = list(
            set(list(after_dict.get(entry, [])) + list(code[entry_index + 1 :]))
        )

solution = ""
for k in sorted(after_dict, key=lambda k: len(after_dict[k]), reverse=True):
    solution += k

print(f"The solution should be: {solution}")
