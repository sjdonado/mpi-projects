#!/usr/bin/python

import lib as utils
import numpy as np
from mpi4py import MPI

def main():
  root_process = 0
  n = 0
  graph = []
  results = []

  disp_unit = MPI.INT.Get_size()

  world_comm = MPI.COMM_WORLD
  size = world_comm.Get_size()

  node_comm = world_comm.Split_type(MPI.COMM_TYPE_SHARED)
  rank = node_comm.rank

  if rank == root_process:
    start_time = MPI.Wtime()
    n, graph = utils.read_graph()
    memory_size = disp_unit
  else:
    memory_size = 0

  win = MPI.Win.Allocate_shared(memory_size, disp_unit, comm=node_comm)

  if rank == root_process:
    win.Put(np.zeros(shape=(1,), dtype='i'), 0)

  array = np.empty(shape=(1,), dtype='i')

  (n, graph) = world_comm.bcast((n,graph), root=root_process)

  while True:
    win.Lock(MPI.LOCK_EXCLUSIVE, 1)

    win.Get(array, 0)
    vertex = array[0]
    array[0] += 1
    win.Put(array, 0)

    win.Unlock(1)

    # print('RANK -->', rank, 'vertex: ', vertex, 'exit', vertex >= n)
    if vertex >= n: break
    dist, pred = utils.bellman_ford(graph, n, vertex)
    results.append((pred, vertex))

  data = world_comm.gather(results, root=root_process)

  if rank == root_process:
    for arr_results in data:
      for (pred, vertex) in arr_results:
        utils.write_vertex(n, pred, vertex)
    print("Tiempo de ejecucion: %f" % (MPI.Wtime() - start_time))

if __name__ == '__main__':
  main()
