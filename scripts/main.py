#!/usr/bin/python3

import sys
import generator
import verificator

def verify_numbers(numbers_array):
  """
    Return the quantity of primes numbers on an array
  """
  primes_cont = 0
  for number in numbers_array:
    if verificator.is_prime(number): 
      primes_cont += 1
  return primes_cont

def main():
  args = sys.argv[1:]
  if not args:
    print('usage: [--cores number] digits')
    sys.exit(1)

  cores = None
  if args[0] == '--cores':
    cores = args[1]
    del args[0:2]

  if len(args) == 0:
    print('error: must specify the number digits')
    sys.exit(1)

  digits = args[0]

  numbers_array = generator.numbers(int(digits))
  print(verify_numbers(numbers_array))
  if cores: 
    print(cores)

if __name__ == '__main__':
  main()

  

