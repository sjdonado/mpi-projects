#!/usr/bin/python

import sys
import time
import random as rand
import numpy as np
from mpi4py import MPI

def main():
  root_process = 0
  k = 0
  attr_size = 5

  world_comm = MPI.COMM_WORLD
  size = world_comm.Get_size()
  disp_unit = MPI.INT.Get_size()

  node_comm = world_comm.Split_type(MPI.COMM_TYPE_SHARED)

  if node_comm.rank == root_process:
    start_time = MPI.Wtime()
    memory_size = size * disp_unit**attr_size
  else:
    memory_size = 0
  
  win = MPI.Win.Allocate_shared(memory_size, disp_unit, comm=node_comm)
  buf, itemsize = win.Shared_query(0)

  buf = np.array(buf, dtype='B', copy=False)
  arr = np.ndarray(buffer=buf, dtype='i', shape=(size, attr_size))

  if node_comm.rank == root_process:
    if len(sys.argv[1:]) == 1:
      k = int(sys.argv[1:][0])
    else:
      print('Error! k not supplied')

    if node_comm.size > 2:
      for node in range(1, node_comm.size):
        right_node = node + 1
        left_fork = 0
        right_fork = 0
        if node == node_comm.size - 1: right_node = 1
        if node == 0:
          left_fork = rand.randint(0, 1)
          right_fork = rand.randint(0, 1)

        # If my left partner doesn't have the fork I can get it
        if node - 1 > 0 and not arr[node - 1][3]:
          arr[node-1][3] = rand.randint(0, 1)
        # If my right partner doesn't have the fork I can get it
        if len(arr) > right_node and len(arr[right_node]) > 0 and not arr[right_node][2]:
          arr[right_node][2] = rand.randint(0, 1)

        # [kind, right_node, left_fork, right_fork, finished]
        # kind -> 0: Friendly, 1: Ambitious
        arr[node] = np.array([0, right_node, left_fork, right_fork, 0], dtype='i')
    
      ambitious = np.random.choice(node_comm.size, 2)
      # print(arr)
      arr[ambitious[0]][0] = 1
      arr[ambitious[1]][0] = 1

  k = world_comm.bcast(k, root=root_process)

  if node_comm.rank == root_process:
    while all(not node[4] for node in arr):
      time.sleep(1)
      print(arr)
  else:
    for task in range(0, k):
      print('NODE', node_comm.rank, 'TASK', task, '-->', 'arr', arr[node_comm.rank], 'k', k)
      time.sleep(rand.randint(7, 10))
      ready_to_eat = False

      if not arr[node_comm.rank - 1][3]:
        arr[node_comm.rank][3] = 1
        arr[node_comm.rank][2] = 1

        if arr[node_comm.rank + 1][2]:
          if arr[node_comm.rank][0]:
            while arr[node_comm.rank + 1][2]: time.sleep(1)
            ready_to_eat = True
          else:
            time.sleep(rand.randint(5, 15))
            ready_to_eat = not arr[node_comm.rank + 1][2]
        else:
          ready_to_eat = True

      if ready_to_eat:
        arr[node_comm.rank + 1][2] = 1
        arr[node_comm.rank][3] = 1

        time.sleep(rand.randint(2, 5))
        
        print('TEST -->', node_comm.rank, len(arr[node_comm.rank]))
        arr[node_comm.rank + 1][2] = 0
        arr[node_comm.rank][3] = 0
      else:
        print('TEST -->', node_comm.rank, len(arr[node_comm.rank]))
        arr[node_comm.rank][3] = 0
        arr[node_comm.rank + 1][2] = 0

      time.sleep(rand.randint(7, 10))

    arr[node_comm.rank][4] = 1

  # world_comm.Barrier()
  print('FINISH', node_comm.rank, arr)

  # for index in range(0, nodes_size):

  #   props = [int(x) for x in bin(arr[index])[2:]]
  #   while len(props) < 3: props.insert(0, 0)

  #   # print(index, arr[index], props)

  #   kind =  'Ambicioso' if props[2] else 'Amigable'
  #   left = 'x' if props[0] else '-'
  #   right = 'x' if props[1] else '-'
  #   none = 'x' if not props[0] and not props[1] else '-'

  #   print('Filosofo', index, kind, left, right, none)


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
