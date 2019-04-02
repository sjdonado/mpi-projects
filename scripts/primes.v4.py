#!/usr/bin/python

import sys
import numpy
import time
import math
from mpi4py import MPI

# def sieveOfAtkin(limit):
#   P = [2,3]
#   sieve=[False]*(limit+1)
#   for x in range(1,int(math.sqrt(limit))+1):
#     for y in range(1,int(math.sqrt(limit))+1):
#       n = 4*x**2 + y**2
#       if n<=limit and (n%12==1 or n%12==5) : sieve[n] = not sieve[n]
#       n = 3*x**2+y**2
#       if n<= limit and n%12==7 : sieve[n] = not sieve[n]
#       n = 3*x**2 - y**2
#       if x>y and n<=limit and n%12==11 : sieve[n] = not sieve[n]
#   for x in range(5,int(math.sqrt(limit))):
#     if sieve[x]:
#       for y in range(x**2,limit+1,x**2):
#         sieve[y] = False
#   for p in range(5,limit):
#     if sieve[p] : P.append(p)
#   return P

# print sieveOfAtkin(100)

def main():
  root_process = 0
  digits = 0
  primes_cont = 0
  result = 0
  
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()

  start_time = time.time()

  if rank == root_process:
    digits = int(sys.argv[1:][0])

  digits = comm.bcast(digits, root=root_process)

  min = 10**(digits - 1)
  max = 10**digits
  unread_indexes = (max - min) % size
  container_range = range(0, size)
  interval_size = (max - min) / size
  limit = (rank +  1) * interval_size + min
  # print 'limit', limit, 'interval_limit', interval_limit

  P = [2,3]
  sieve=[False]*(limit+1)
  for x in range(min,int(math.sqrt(limit))+1):
    for y in range(min,int(math.sqrt(limit))+1):
      n = 4*x**2 + y**2
      if n<=limit and (n%12==1 or n%12==5) : sieve[n] = not sieve[n]
      n = 3*x**2+y**2
      if n<= limit and n%12==7 : sieve[n] = not sieve[n]
      n = 3*x**2 - y**2
      if x>y and n<=limit and n%12==11 : sieve[n] = not sieve[n]
      sieve = comm.bcast(sieve, root=rank)
  print 'rank', rank, sieve
  for x in range(5,int(math.sqrt(limit))):
    if sieve[x]:
      for y in range(x**2,limit+1,x**2):
        sieve[y] = False
  for p in range(5,limit):
    if sieve[p] : 
      P.append(p)
      primes_cont += 1
  
  # for num in xrange(rank * size + min, max, size * size):
  #   if max - unread_indexes == num: container_range = range(0, unread_indexes)
  #   # print 'rank', rank, 'num', num, 'max - size + 1 - unread_indexes', max - unread_indexes, 'container_range', container_range
  #   for container in container_range:
  #     if is_prime(num + container): primes_cont += 1

  primes = numpy.array(primes_cont, 'i')
  result = numpy.array(0, 'i')

  comm.Reduce([primes, MPI.INT], [result, MPI.INT], op=MPI.SUM, root=root_process)

  if rank == root_process:
    end_time = time.time()
    print'El numero de primos de', digits, 'digitos es', result, 'Tiempo:', end_time - start_time
  # comm.Disconnect()

main()