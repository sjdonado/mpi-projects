#!/usr/bin/python

import sys
import numpy
from mpi4py import MPI

def main():
  root_process = 0
  digits = 0
  non_primes_cont = 0
  
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()

  start_time = MPI.Wtime()

  if rank == root_process:
    digits = int(sys.argv[1:][0])

  digits = comm.bcast(digits, root=root_process)

  min = 10**(digits - 1)
  max = 10**digits
  unread_indexes = (max - min) % size
  container_range = range(0, size)

  for num in range(rank * size + min, max, size * size):
    # if max - unread_indexes == num: container_range = range(0, unread_indexes)
    for container in container_range:
      i = 2
      print 'rank', rank, 'num', (num + container)
      while i <= (num + container) / i:
        if (num + container) % i == 0:
          non_primes_cont += 1
          break
        i += 1 if i == 2 else 2  

  print 'FINISHED ---->', 'rank', rank

  result = comm.reduce(sendobj=non_primes_cont, root=root_process, op=MPI.SUM)

  if rank == root_process:
    print 'El numero de primos de', digits, 'digitos es', (max - min) - result, 'Tiempo:', MPI.Wtime() - start_time

main()
