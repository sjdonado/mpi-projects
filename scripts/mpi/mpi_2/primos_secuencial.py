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
  digits = []

  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()

  if rank == root_process:
    start_time = MPI.Wtime()
    size = comm.Get_size()
    
    nodes_statistics = {}
    max = int(sys.argv[1:][0])
    number = 1

    for node_rank in range(1, size):
      nodes_statistics[str(node_rank)] = 0

    while number <= max:
      for node_rank in range(1, size):
        if number <= max:
          comm.send(number, dest=node_rank)
          (node_rank, node_data) = comm.recv(source=MPI.ANY_SOURCE)
          primes_cont += int(node_data)
          nodes_statistics[str(node_rank)] += 1
          number += 1

    for node_rank in range(1, size):
      comm.send(-1, dest=node_rank)
  else:
    while True:  
      number = comm.recv(source=root_process)
      if number == -1: break
      comm.send((rank, is_prime(number)), dest=root_process)

  if rank == root_process:
    print 'El numero de primos es:', primes_cont
    print 'Tiempo de ejecucion:', MPI.Wtime() - start_time
    print 'Numero de validaciones por proceso:'
    for key in sorted(nodes_statistics.keys()):
      print 'Proceso:', key, 'Total:', nodes_statistics[key]

if __name__ == '__main__':
  main()
