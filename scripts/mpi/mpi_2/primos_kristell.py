#!/usr/bin/python

import sys
from mpi4py import MPI

def main():
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()

  primes = 0
  nodes_death = 0
  init = True
  validations = [0]*size

  if rank == 0:
    start_time = MPI.Wtime()
    limit = int(sys.argv[1:][0])
    number = 2
    head_finish = True
  else:
    limit = 0
    number = 0
    head_finish = False

  (number, limit) = comm.bcast((number, limit), root=0)
  
  while number < limit or head_finish:  
    if rank == 0:
      if init:
        for node_rank in range(1, size):
          comm.send(number, dest=node_rank)
          number += 1
        init = False

      (node_rank, node_data) = comm.recv(source=MPI.ANY_SOURCE)
      # print('node_rank', node_rank, 'node_data', node_data)
      primes += int(node_data)
      validations[node_rank] += 1

      comm.send(number, dest=node_rank)

      if number < limit:
        number += 1
      else:
        nodes_death += 1

      if nodes_death == size - 1: break
    else:
      number = comm.recv(source=0)
      # print(number)
      if number < limit:
        is_prime = True
        for i in range(2, (number / 2) + 1):
          if number % i == 0:
            is_prime = False
        comm.send((rank, is_prime), dest=0)

  # print('finished', rank)

  if rank == 0:
    print 'El numero de primos es:', primes
    print 'Tiempo de ejecucion:', MPI.Wtime() - start_time
    print 'Numero de validaciones por proceso:'
    for index, value in enumerate(validations):
      print 'Proceso:', index, 'Total:', value

if __name__ == '__main__':
  main()
