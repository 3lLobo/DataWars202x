# Find the coordinates for the 3 tankstations with k-nearest neighbor.

import pandas as pd
import os
from sklearn.neighbors import NearestNeighbors

# path of current file
base_path = os.path.dirname(os.path.realpath(__file__))
data_path = os.path.join(base_path, 'input.txt')


def read_data():
  """
  Read the input file.
  Return one dataframe with the 12 potential target coordinates
  and one dataframe with the meassurements.
  """
  column_names = ['x', 'y', 'z', 't']
  switch = False
  targets = []
  measurements = []
  with open(data_path, 'r') as f:
    for line in f.readlines():
      line = line.strip('\n')
      if switch:
        measurements.append(line.split(','))
      else:
        if line.startswith('#'):
          switch = True
        else:
          targets.append(line.replace('[', '').replace(']', '').split(','))

  df_target = pd.DataFrame(targets, columns=column_names).astype(float)
  df_measurements = pd.DataFrame(measurements, columns=column_names).astype(float)

  return df_target, df_measurements


def  


def main():
  df_target, df_measurements = read_data()
  print(df_target.head())
  print(df_measurements.head())

if __name__ == '__main__':
  main()