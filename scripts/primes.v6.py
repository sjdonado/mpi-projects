#!/usr/bin/python

import sys
import random
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
  primes_cont = 0
  num = 0

  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()


  if rank == root_process:
    start_time = MPI.Wtime()

    digits = int(sys.argv[1:][0])
    min = 10**(digits - 1)
    max = 10**digits

    for number in range(min, max + 1, size - 1):
      for rank_offset in range(1, size):
        if number < max:
          comm.send(number +  rank_offset, dest=rank_offset, tag=0)
        else:
          comm.send(-1, dest=rank_offset, tag=0)
      comm.barrier()
  else:
    while True:
      number = comm.recv(source=root_process, tag=0)
      # print 'rank -->', rank, 'number:', number
      if number == -1: break
      if is_prime(number):
        primes_cont += 1
      comm.barrier()

    comm.barrier()
      
  result = comm.reduce(sendobj=primes_cont, root=root_process, op=MPI.SUM)
  
  if rank == root_process:
    print 'El numero de primos de', digits, 'digitos es', result, 'Tiempo:', MPI.Wtime() - start_time
  # comm.Disconnect()

main()
