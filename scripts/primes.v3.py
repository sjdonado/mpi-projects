#!/usr/bin/python

import sys
import numpy
import time
from mpi4py import MPI

def is_prime(number):
  # Return true if a number is prime
  i = 2
  prime = True
  while i <= (number / i):
    if number % i == 0:
      prime = False
      break
    i += 1 if i == 2 else 2
  return prime

def main():
  root_process = 0
  digits_input = 0
  primes_cont = 0
  
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()

  start_time = time.time()

  if rank == root_process:
    digits_input = int(sys.argv[1:][0])

  digits = numpy.array(digits_input, 'i')
  comm.Bcast([digits, MPI.INT], root=root_process)

  min = 10**(digits - 1)
  max = 10**digits
  container_range = range(0, size)

  for num in xrange(rank * size + min, max, size * size):
    if num + size - 1 < max:
      # print 'rank', rank, 'num', num, 'end', num + size
      for container in container_range:
        if is_prime(num + container): primes_cont += 1

  # print 'primes_cont', primes_cont
  primes = numpy.array(primes_cont, 'i')
  result = numpy.array(0, 'i')

  comm.Reduce([primes, MPI.INT], [result, MPI.INT], op=MPI.SUM, root=root_process)

  if rank == root_process:
    end_time = time.time()
    print'El numero de primos de', digits, 'digitos es ', result, 'Tiempo: ', end_time - start_time
  # comm.Disconnect()

main()