#!/usr/bin/python

import sys
import time
import random as rand
import numpy as np
from mpi4py import MPI

def print_table(table, size):
  header = "\t"
  fork = "\t"
  avaliable_fork = "\t"
  for idx in range(size):
    header += "Filosofo %d (%s) \t\t" % (idx + 1, 'Ambicioso' if table[idx, 0] else 'Amigable')
    fork += "\t%s | %s \t\t\t" % ('x' if table[idx, 3] else '-', 'x' if table[idx, 4] else '-')
    avaliable_fork += "\t  %s\t\t\t" % ('x' if not table[idx, 3] and not table[idx, 4] else '-')

  limiter = "=" * (len(header) + 27)
  print(" |%s| \n |%s| \n |%s| \n |%s| \n |%s| \n |%s| \n |%s| \n" % (limiter, header, limiter, fork, limiter, avaliable_fork, limiter))

def main():
  root_process = 0
  k = 0
  attr_size = 6

  disp_unit = MPI.INT.Get_size()
  world_comm = MPI.COMM_WORLD
  size = world_comm.Get_size() - 1
  rank = world_comm.Get_rank()

  if rank == root_process:
    start_time = MPI.Wtime()
    memory_size = size * disp_unit**attr_size
  else:
    memory_size = 0
  
  win = MPI.Win.Allocate_shared(memory_size, disp_unit, comm=world_comm.Split_type(MPI.COMM_TYPE_SHARED))
  buf, itemsize = win.Shared_query(0)

  buf = np.array(buf, dtype='B', copy=False)
  table = np.ndarray(buffer=buf, dtype='i', shape=(size, attr_size))

  if rank == root_process:
    start_time = MPI.Wtime()

    if len(sys.argv[1:]) == 1:
      k = int(sys.argv[1:][0])
    else:
      print('Error! k not supplied')

    if size > 2:
      for node in range(size):
        right_node = node + 1
        left_node = node - 1
        left_fork = 0
        right_fork = 0

        if node == size - 1: right_node = 0
        if left_node < 0: left_node = size - 1

        if node == 0:
          left_fork = rand.randint(0, 1)
          right_fork = rand.randint(0, 1)

        # If my left partner doesn't have the right fork I can get it
        if not table[left_node, 4]:
          table[node, 3] = rand.randint(0, 1)
        # If my right partner doesn't have the left fork I can get it
        if not table[right_node, 3]:
          table[node, 4] = rand.randint(0, 1)

        # [kind, left_node, right_node, left_fork, right_fork, finished]
        # kind -> 0: Friendly, 1: Ambitious
        table[node] = np.array([0, left_node, right_node, left_fork, right_fork, 0], dtype='i')
    
      ambitious = np.random.choice(size, 2)
      # print(arr)
      table[ambitious[0], 0] = 1
      table[ambitious[1], 0] = 1

    else:
      print('Error! Min 3 philosophers')
      exit(1)

  k = world_comm.bcast(k, root=root_process)

  if rank == root_process:
    while True:
      # print('TABLE ->', table, 'BREAK -->', all(node[5] for node in table))
      if all(node[5] for node in table): break
      print_table(table, size)
      time.sleep(1)
    print("Tiempo de ejecucion: %f" % (MPI.Wtime() - start_time))
  else:
    rank_pos = rank - 1

    for task in range(k):
      time.sleep(rand.randint(7, 10))
      ready_to_eat = False

      # print('LEFT_FORK -->, rank_pos', rank_pos, 'table', table[rank_pos], 'left_table', table[table[rank_pos, 1]])
      if not table[table[rank_pos, 1], 4]:
        win.Lock(MPI.LOCK_EXCLUSIVE, 1)
        table[rank_pos, 3] = 1
        win.Unlock(1)

        # print('RIGHT_FORK -->, rank_pos', rank_pos, 'table', table[rank_pos], 'left_table', table[table[rank_pos, 2]])
        if table[table[rank_pos, 2], 3]:
          if table[rank_pos, 0]:
            while table[table[rank_pos, 2], 3]: time.sleep(0.01)
            ready_to_eat = True
          else:
            time.sleep(rand.randint(5, 15))
            ready_to_eat = not table[table[rank_pos, 2], 3]
        else:
          ready_to_eat = True

      if ready_to_eat:
        win.Lock(MPI.LOCK_EXCLUSIVE, 1)
        table[rank_pos, 4] = 1
        win.Unlock(1)

        time.sleep(rand.randint(2, 5))

        win.Lock(MPI.LOCK_EXCLUSIVE, 1)
        table[rank_pos, 4] = 0
        table[rank_pos, 3] = 0
        win.Unlock(1)

      else:
        win.Lock(MPI.LOCK_EXCLUSIVE, 1)
        table[rank_pos, 4] = 0
        table[rank_pos, 3] = 0
        win.Unlock(1)

      time.sleep(rand.randint(7, 10))

    table[rank_pos, 5] = 1

if __name__ == '__main__':
  main()
