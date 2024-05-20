# Solution: 79NJT@-9UI9(K5U
# Result: Correct

import pandas as pd

file = "excercises/def_1/Handleiding TELEX.html"
input_codes = "excercises/def_1/input.txt"

# Get second table in html
df = pd.read_html(file)[1]
df.columns = df.columns.str.lower()
df = df.set_index("code")

# Create a map of the codes and their meanings
translate_raw_dict = df.to_dict("tight")
translation_dict = {}
for idx, key in enumerate(translate_raw_dict["index"]):
    translation_dict[key] = {
        "letter": translate_raw_dict["data"][idx][0],
        "teken": translate_raw_dict["data"][idx][1],
    }


text = ""
use_letter = None
with open(input_codes, "r") as fh:
    for idx, line in enumerate(fh):
        line = line.strip()
        if line[3] != "o":
            raise Exception(f"miss-rotated {idx}")
        data = translation_dict[line]
        if data["letter"] == '[Schakel naar Letters]':
            use_letter = True
        elif data["letter"] == '[Schakel naar Tekens]':
            use_letter = False
        elif data["letter"] in ['[WAGEN TERURLOOP / CARRIAGE RETURN]', '[NIEUWE REGEL / LINE FEED]']:
            text += "\n"
        elif data["letter"] == "[SPATIE]":
            text += " "
        else:
            if use_letter is None:
                raise Exception("Unclear which mode should be active.")
            text += data["letter"] if use_letter else data["teken"]

# Code is in the text.
print(text)