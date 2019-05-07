#!/usr/bin/python

import sys
import numpy
from mpi4py import MPI

def main():
  root_process = 0
  digits = 0
  non_primes_cont = 0
  num = 0
  max = 0

  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()

  start_time = MPI.Wtime()

  rank_range = range(0, size)
  rank_range.remove(rank)

  if rank == root_process:
    digits = int(sys.argv[1:][0])
    min = 10**(digits - 1)
    max = 10**digits

    numbers = range(min, max)
    for node_rank in rank_range: comm.send((min, max), dest=node_rank, tag=0)

  else:
    (min, max) = comm.recv(source=root_process, tag=0)
    numbers = range(min, max)

  while True:
    if not numbers: break
    num = numbers[rank]
    del numbers[rank]

    print 'numbers -before', numbers

    # Use all to all and build a unique numbers array by rank
    numbers = comm.bcast(numbers, root=0)

    print 'rank', rank, 'num', num
    print 'numbers', numbers

    # comm.send(num + 1, dest=free_processes[0], tag=0)
    # del free_processes[0]

    # print 'rank', rank, 'num', num
    # i = 2
    # while i <= num / i:
    #   if num % i == 0:
    #     non_primes_cont += 1
    #     break
    #   i += 1 if i == 2 else 2

    # print 'free_processes after after', free_processes
    # for node_rank in rank_range: 
    #   free_processes.append(rank)
    #   comm.send(free_processes, dest=node_rank, tag=2)

  print 'FINISHED ---->', 'rank', rank, 'non_primes_cont', non_primes_cont
  # if num != -1:
  #   for node_rank in rank_range: comm.send(-1, dest=node_rank, tag=0)

  # result = comm.reduce(sendobj=non_primes_cont, root=root_process, op=MPI.SUM)

  if rank == root_process:
    print 'El numero de primos de', digits, 'digitos es', (max - min) - result, 'Tiempo:', MPI.Wtime() - start_time
  # comm.Disconnect()

main()
