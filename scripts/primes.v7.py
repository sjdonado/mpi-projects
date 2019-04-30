#!/usr/bin/python

import sys
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
  size = None
  run = True
  digits = []
  data = []

  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()

  if rank == root_process:
    start_time = MPI.Wtime()
    size = comm.Get_size()

    n = int(sys.argv[1:][0])
    min = 10**(n - 1)
    max = 10**n

    digits = range(min, max)

  while run:  
    number = comm.scatter(digits[:size], root=root_process)
    data = comm.gather(is_prime(number), root=root_process)

    if rank == root_process:
      primes_cont += sum(data)
      digits = digits[size:]
      run = len(digits) > size

    run = comm.bcast(run, root=root_process)

  if rank == root_process:
    print 'El numero de primos de', n, 'digitos es', primes_cont, 'Tiempo:', MPI.Wtime() - start_time

if __name__ == '__main__':
  main()