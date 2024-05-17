import numpy as np


def solve(data):

    # This array is provided in the description.
    base = np.array([[0, 0, 1], [0, 1, 0], [1, 0, 0]])

    shape = data.shape[0]
    out = []
    # Loop over x and y mutiplying the base array with the cells provided.
    for y in range(0, shape-2):
        out_x = []
        for x in range(0, shape-2):
            result = np.multiply(data[x:(x+3), y:(y+3)].astype(int), base)
            out_x.append(result.sum())
        out.append(out_x) 
    result_step_1 = np.array(out).T
    
    # Loop over the new array for step 2 of the problem.
    shape = result_step_1.shape[0]
    out_2 = []
    for y in range(0, shape-1, 2):
        out_x = []
        for x in range(0, shape-1, 2):
            result = result_step_1[x:(x+2), y:(y+2)].max()
            out_x.append(result)
        out_2.append(out_x)

    # Wanneer je deze output-array hebt kun je het antwoord berekenen. Het antwoord bestaat uit twee delen:
    # 1) bekijk wat de maximale waarde is in de array
    # 2) bekijk hoe vaak deze waarde in de array voorkomt.
    out = np.array(out_2)
    max_val = out.max()
    count = np.count_nonzero(out == max_val)

    print(max_val * count)


# First try it on the demo data
output = []
demo = """024234
404823
204924
103893
293001
102939"""
for i in demo.split("\n"):
    output.append([*i.strip()])
demo_data = np.array(output)

# 21. Correct.
solve(demo_data)


# Now for real
# Read and process the data
output = []
with open("opdrachten/verdediging5/input.txt", "r") as fin:
    for i in fin:
        output.append([*i.strip()])
data = np.array(output)
data = data.astype(int)

# 48
solve(data)
# Answer submitted.
# Correct!