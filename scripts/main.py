#!/usr/bin/python3

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


def verify_numbers(min, max):
  """
    Retutn the amount of prime numbers in an interval
  """
  primes_cont = 0
  for number in numpy.arange(min, max, dtype='i'):
    if is_prime(number): primes_cont += 1
  return primes_cont


def main():
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()

  print('My rank is: ',rank, )

  if rank == 0:
    # 2 4 6 8 10 12 14 16
    size = comm.Get_size() - 1
    # print('size', size)

    args = sys.argv[1:]
    if len(args) == 0:
      print('error: must specify the number digits')
      sys.exit(1)
    
    start = time.time()
    
    # 2 4 6 8
    digits = int(args[0])
    range_limit = (10**digits -  10**(digits - 1)) / size
    # print('range_limit', range_limit)
    results = []

    if size > 1:
      # First range
      comm.send((10**(digits - 1) + 1, range_limit), dest=1, tag=0)
      results.append(comm.recv(source=1, tag=1))

      # Last range
      comm.send((range_limit*(size-1) + 1, 10**digits - 1), dest=size, tag=0)
      results.append(comm.recv(source=size, tag=1))

      for i in reversed(range(2,size)):
        comm.send((range_limit*(i-1) + 1, range_limit*i), dest=i, tag=0)
        results.append(comm.recv(source=i, tag=1))
    else:
      comm.send((10**(digits - 1) + 1, 10**digits - 1), dest=size, tag=0)
      results.append(comm.recv(source=size, tag=1))

    end = time.time()
    print('result:', sum(results), end - start)
  else:
    data = comm.recv(source=0, tag=0)
    # print('params', data)
    primes = verify_numbers(data[0], data[1])
    comm.send(primes, dest=0, tag=1)


if __name__ == '__main__':
  main()

  

