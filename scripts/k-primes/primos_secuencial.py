#!/usr/bin/python

import sys
import time

def is_prime(number):
  # Return true if a number is prime
  i = 2
  prime = True
  while i <= (number / 2) + 1:
    if number % i == 0:
      prime = False
      break
    i += 1
  return prime

def main():
  primes_cont = 0
  number = 2
  
  max = int(sys.argv[1:][0])
  start_time = time.time()

  while number <= max:
    primes_cont += int(is_prime(number))
    number += 1

  print 'El numero de primos es:', primes_cont
  print 'Tiempo de ejecucion:', time.time() - start_time

if __name__ == '__main__':
  main()
