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
    for container in container_range:
      i = 2
      print 'rank', rank, 'num', (num + container)
      while i <= (num + container) / i:
        if (num + container) % i == 0:
          non_primes_cont += 1
          break
        i += 1 if i == 2 else 2  

  print 'FINISHED ---->', 'rank', rank
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

  # primes = numpy.array(non_primes_cont, 'i')
  # result = numpy.array(0, 'i')

  result = comm.reduce(sendobj=non_primes_cont, root=root_process, op=MPI.SUM)
  # comm.Reduce([primes, MPI.INT], [result, MPI.INT], op=MPI.SUM, root=root_process)

  if rank == root_process:
    print 'result', result, 'max', max, 'min', min, (max - min) - result
    print 'El numero de primos de', digits, 'digitos es', (max - min) - result, 'Tiempo:', MPI.Wtime() - start_time
  # comm.Disconnect()

main()
