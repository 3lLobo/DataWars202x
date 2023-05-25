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


def knn_predict(df_target, df_measurements, k=1):
  """
  Fit the KNN on the targets, then get the nearest neighbors for the measurements.
  Return the count of neighbors for each target.
  """
  nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(df_target)
  distances, indices = nbrs.kneighbors(df_measurements)
  return indices

def knn_graph(df_target, df_measurements, k=1):
  """
  Fit the KNN on the targets, then get the graph of the nearest neighbors for the measurements.
  Return 
  """
  nbrs = NearestNeighbors(n_neighbors=k, algorithm='ball_tree').fit(df_target)
  sparse_graph = nbrs.kneighbors_graph(df_measurements).toarray()
  # sum per target
  graph = sparse_graph.sum(axis=0)
  return graph

def get_top_k(indices, k=3):
  """
  Get the top k values from the list.
  """
  df_indices = pd.DataFrame()
  df_indices['indices'] = indices
  top = df_indices['indices'].value_counts()
  print(top)
  top_k = top.head(k)
  return top_k

def main():
  df_target, df_measurements = read_data()
  # print(df_target.head())
  # print(df_measurements.head())
  # indices = knn_predict(df_target, df_measurements)
  # top_k = get_top_k(indices)
  # print(top_k)
  graph = knn_graph(df_target, df_measurements)
  print(graph)
  # 

if __name__ == '__main__':
  main()