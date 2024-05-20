# Solution: 7650
# Result: Correct

file = "excercises/intel_1/Intergalactic Language/input.txt"

with open(file, "r") as fh:
    text = fh.read().strip()

letter_count = 0
word_count = 0
for word in text.split(" "):
    # If word is equal to the reversed word, score.
    if word == word[::-1]:
        word_count += 1
        letter_count += len(word)

print("Flag:", word_count * letter_count)
