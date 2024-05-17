from multiprocessing import Pool
import time
from cube import cube, N

if __name__ == "__main__":
  start = time.time()
  with Pool() as pool:
    result = pool.map(cube, range(10,N))
  end = time.time()
  print("Program finished!")
  print("Execution Time: {}".format(end-start))
    