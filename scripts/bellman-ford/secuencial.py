#!/usr/bin/python
# import numpy as np

import time
import lib as utils

def main():
  start_time = time.time()

  n, graph = utils.read_graph()
  # print('n', n)
  # print(graph)

  results = open('secuencial.txt', 'w+')

  for origin in range(n):
    dist, pred = utils.bellman_ford(graph, n, origin)
    # print('dist', dist)
    # print('pred', pred)
    utils.write_vertex(n, pred, origin)

  print("Tiempo de ejecucion: %f" % (time.time() - start_time))

if __name__ == '__main__':
  main()