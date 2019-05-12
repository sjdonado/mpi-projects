#!/usr/bin/python

import secuencial as utils
import numpy as np
from mpi4py import MPI

def main():
  root_process = 0
  n = 0
  graph = []

  disp_unit = MPI.INT.Get_size()

  world_comm = MPI.COMM_WORLD
  size = world_comm.Get_size()

  node_comm = world_comm.Split_type(MPI.COMM_TYPE_SHARED)
  rank = node_comm.rank

  if rank == root_process:
    start_time = MPI.Wtime()
    n, graph = utils.read_graph()
    memory_size = disp_unit**n

    open('paralela.txt', 'w').close()
  else:
    memory_size = 0

  (n, graph) = world_comm.bcast((n,graph), root=root_process)
  
  win = MPI.Win.Allocate_shared(memory_size, disp_unit, comm=node_comm)

  win.Fence()
  if rank == root_process:
    win.Put(np.zeros(shape=(n,), dtype='i'), root_process)
  win.Fence()

  results = open('paralela.txt', 'a')

  while True:
    win.Fence()
    array = np.empty(shape=(n,), dtype='i')
    win.Get(array, root_process)
    vertex = np.argmin(array)
    if array[vertex] == 1: break
    array[vertex] = 1
    win.Put(array, root_process)
    win.Fence()

    dist, pred = utils.bellman_ford(graph, n, vertex)
    utils.write_vertex(results, pred, n, vertex)

  world_comm.barrier()

  if rank == root_process:
    print 'Tiempo de ejecucion:', MPI.Wtime() - start_time

if __name__ == '__main__':
  main()
