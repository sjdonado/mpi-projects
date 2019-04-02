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

  for num in xrange(rank * size + min, max, size * size):
    if max - unread_indexes == num: container_range = range(0, unread_indexes)
    # print 'rank', rank, 'num', num, 'max - size + 1 - unread_indexes', max - unread_indexes, 'container_range', container_range
    for cont in container_range:
      i = 2
      x = num + cont
      while i <= x / i:
        if x % i == 0:
          non_primes_cont += 1
          break
        i += 1 if i == 2 else 2  
  # for num in xrange(rank * size + min, max, size * size):
  #   # if max - unread_indexes == num: container_range = range(0, unread_indexes)
  #   # print 'rank', rank, 'num', num, 'max - size + 1 - unread_indexes', max - unread_indexes, 'container_range', container_range
  #   dir = True
  #   for container in container_range:
  #     if dir:
  #       primes_cont = is_prime(primes_cont, num + container);
  #     else:
  #       primes_cont = is_prime(primes_cont, max - (num + container) + min);
  #     dir = not dir

  result = comm.reduce(sendobj=non_primes_cont, root=root_process, op=MPI.SUM)

  if rank == root_process:
    print 'El numero de primos de', digits, 'digitos es', (max - min) - result, 'Tiempo:', MPI.Wtime() - start_time
  # comm.Disconnect()

main()
