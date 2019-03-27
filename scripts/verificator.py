#!/usr/bin/python3

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


def main():
  num = input("Number: ")
  result = is_prime(num)
  if result: print('{} es primo').format(num)
  else: print('No es primo')

if __name__ == '__main__':
  main()
