import threading
import time
from cube import cube, N




if __name__ == "__main__":
  start = time.time()
  
  threads = []
  for i in range(10,N):
    t = threading.Thread(target=cube, args=(i,))
    threads.append(t)
    t.start()

  for t in threads:
    t.join()

  end = time.time()

  print("Program finished!")
  print("Execution Time: {}".format(end-start))
    