#!/usr/bin/python

import sys
import time
import numpy as np
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
  max = 0
  primes_cont = 0

  disp_unit = MPI.INT.Get_size()
  world_comm = MPI.COMM_WORLD
  node_comm = world_comm.Split_type(MPI.COMM_TYPE_SHARED)
  size = world_comm.Get_size()

  rank = node_comm.rank

  if rank == root_process:
    start_time = MPI.Wtime()

    n = int(sys.argv[1:][0])
    min = 10**(n - 1)
    max = 10**n

    memory_size = disp_unit
  else:
    memory_size = 0

  max = world_comm.bcast(max, root=root_process)

  # arr = np.ndarray(dtype='i', shape=(1,))
  # win = MPI.Win.Create(arr, 1, comm=comm)
  
  win = MPI.Win.Allocate_shared(memory_size, disp_unit, comm=node_comm)
  buf, itemsize = win.Shared_query(0)

  buf = np.array(buf, dtype='B', copy=False)
  arr = np.ndarray(buffer=buf, dtype='i', shape=(1,1))

  if rank == root_process:
    win.Fence()
    arr[0,0] = [min]

  world_comm.barrier()

  while True:
    win.Fence()
    number = arr[0,0]
    arr[0,0] += 1
    win.Fence()
    if number >= max: break
    print('RANK:', rank, 'NUMBER:', number)
    if is_prime(number): primes_cont += 1

  result = world_comm.reduce(sendobj=primes_cont, root=root_process, op=MPI.SUM)

  if rank == root_process:
    print 'El numero de primos de', n, 'digitos es', result, 'Tiempo:', MPI.Wtime() - start_time

if __name__ == '__main__':
  main()
