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
  digits_input = 0
  primes_cont = 0
  
  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()
  size = comm.Get_size()

  start_time = MPI.Wtime()

  if rank == root_process:
    digits = int(sys.argv[1:][0])
    min = 10**(digits - 1) + 1
    max = 10**digits - 1
    numbers_range = range(min, max)
    range_size = range(0, (max - min) / size)
    # print('range_size', range_size, 'min', min, 'max', max, 'range_size', (min - max) / size)
    for rank_i in range(1, size):
      send_numbers = []
      for i in range_size:
        index = random.randint(0, len(numbers_range) - 1)
        number = numbers_range.pop(index)
        print 'index', index, 'number', number
        send_numbers.append(number)
      comm.send(send_numbers, dest=rank_i, tag=0)
  else:
    numbers_range = comm.recv(source=root_process, tag=0)
  
  # print('rank', rank, 'numbers_range', numbers_range)

  for num in numbers_range:
    if is_prime(num): primes_cont += 1

  print 'FINISHED ---->', 'rank', rank, 'results', primes_cont

  result = comm.reduce(sendobj=primes_cont, root=root_process, op=MPI.SUM)

  if rank == root_process:
    print'El numero de primos de', digits, 'digitos es', result, 'Tiempo:', MPI.Wtime() - start_time

main()