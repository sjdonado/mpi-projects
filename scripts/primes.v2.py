#!/usr/bin/python

import sys
import numpy
import time
from mpi4py import MPI

def is_prime(number):
  """
    Return true if a number is prime
  """
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

  if rank == root_process:
    start_time = time.time()
    args = sys.argv[1:]
    if len(args) == 0:
      print 'error: must specify the number digits'
      sys.exit(1)
    digits_input = int(args[0])


  digits = numpy.array(digits_input, 'i')
  comm.Bcast([digits, MPI.INT], root=root_process)

  min = 10**(digits-1)
  max = 10**digits
  interval_size = (max - min) / size
  max_interval = (rank +  1) * interval_size + min
  if rank == size: max_interval = max

  # print 'interval_size', interval_size
  # print 'numbers', rank, numpy.arange(rank*interval_size + min, max_interval, dtype='i')

  for number in numpy.arange(rank*interval_size + min, max_interval, dtype='i'):
    if is_prime(number): primes_cont += 1

  # print 'primes_cont', primes_cont
  primes = numpy.array(primes_cont, 'i')
  result = numpy.array(0, 'i')

  comm.Reduce([primes, MPI.INT], [result, MPI.INT], op=MPI.SUM, root=root_process)

  if rank == root_process:
    end_time = time.time()
    # print 'results', result, 'Time', end_time - start_time
    print'El numero de primos de', digits, 'digitos es ', result, 'Tiempo: ', end_time - start_time
  # comm.Disconnect()

main()