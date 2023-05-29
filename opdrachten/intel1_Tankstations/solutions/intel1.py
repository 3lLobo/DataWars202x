"""
Disclaimer -> leads to the same answer as the KNN approach but this is much sloppier

The goal is to get the 3 largest clusters of observations that
match a predefined list of potential targets. The obstacle lies in the error of the 
observations. In this solution, this error is "removed" by rounding the observations.
"""
import pandas as pd


observation_df = pd.read_csv("opdrachten\intel1_Tankstations\input.txt",
                 names=["x", "y", "z", "t"],
                 header=None,
                 skiprows=13)
observation_df = observation_df[["x", "y", "z", "t"]]
observation_df = observation_df.round(0).astype(int)
observation_counts = observation_df.value_counts().reset_index()


## Process the target section of the input file
# Read the first 12 rows in and store as a dataframe with 1 row per line
potential_targets = pd.read_table("opdrachten\intel1_Tankstations\input.txt",
                 header=None,
                 names=["target"],
                 nrows=12)
# The structure of `potential_targets` is a list embedded in a string
# Use eval to convert to list, then convert the structure to a list so that it can be used as input
targets = potential_targets["target"].apply(eval).to_list()
potential_targets[["x", "y", "z", "t"]] = pd.DataFrame(targets)

# Merge on the targets onto the dataframe
observation_counts = observation_counts.merge(potential_targets, on=["x", "y", "z", "t"], how="left")
# Keep the observation counts that are in the potental target list
observation_counts = observation_counts[~observation_counts["target"].isna()]
# Only keep the top 3 for the assignment
observation_counts = observation_counts.head(3)
# [65, 43, 95, 16]
# [68, 43, 98, 16]
# [68, 40, 95, 16]
# The flag requires multiplying these values. Written out manually..
flag = 65 * 43 * 95 * 16 * 68 * 43 * 98 * 16 * 68 * 40 * 95 * 16
print(flag)
# Correct!