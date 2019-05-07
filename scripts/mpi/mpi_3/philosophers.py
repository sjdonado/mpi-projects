#!/usr/bin/python

import sys
import numpy as np
from mpi4py import MPI

def main():
  root_process = 0
  size = 0
  start = False

  world_comm = MPI.COMM_WORLD
  disp_unit = MPI.INT.Get_size()

  node_comm = world_comm.Split_type(MPI.COMM_TYPE_SHARED)
  nodes_size = node_comm.size - 1

  if node_comm.rank == root_process:
    start_time = MPI.Wtime()
    (friendly, ambitious) = (0, 0)
    size = nodes_size * disp_unit
    
    # Generate randomly
    friendly = 1
    ambitious = 1
  
  win = MPI.Win.Allocate_shared(size, disp_unit, comm=node_comm)
  buf, itemsize = win.Shared_query(0)

  arr = np.ndarray(buffer=np.array(buf, dtype='B', copy=False), dtype='i', shape=(nodes_size,))

  if node_comm.rank == root_process:
    # 0 1 2 4

    # Amigable: Si no tiene tenedor --> 0 - 000
    # Amigable: Si tiene el tenedor de la derecha --> 2 - 010 
    # Amigable: Si tiene el tenedor de la izquierda --> 4 - 100
    
    # Ambicioso: Si no tiene tenedor --> 1 - 001
    # Ambicioso: Si tiene el tenedor de la derecha --> 3 - 011
    # Ambicioso: Si tiene el tenedor de la izquierda --> 5 - 101
    arr[:nodes_size] = np.array([1, 4], dtype='i')

  while True:
    if node_comm.rank == root_process:
      for index in range(0, nodes_size):

        props = [int(x) for x in bin(arr[index])[2:]]
        while len(props) < 3: props.insert(0, 0)

        # print(index, arr[index], props)

        kind =  'Ambicioso' if props[2] else 'Amigable'
        left = 'x' if props[0] else '-'
        right = 'x' if props[1] else '-'
        none = 'x' if not props[0] and not props[1] else '-'

        print('Filosofo', index, kind, left, right, none)
        # print arr[:nodes_size]
    # else:
    #   print arr[:nodes_size]

  # teams_list = ['Filosofo 1', 'Filosofo 2', 'Filosofo 3']
  # data = np.array([[1, 2, 1],
  #                 [0, 1, 0],
  #                 [2, 4, 2]])

  # row_format ="{:>15}" * (len(teams_list) + 1)
  # print row_format.format("", *teams_list)
  # for team, row in zip(teams_list, data):
  #     print row_format.format(team, *row)
  # print 'Tiempo de ejecucion:', MPI.Wtime() - start_time

if __name__ == '__main__':
  main()
