#!/usr/bin/python3

import sys
import numpy

def numbers(digits):
  """
    Return a numpy array with all numbers bewtween 0 and 10^digits - 1
  """
  return numpy.arange(1,10**digits)


def main():
  args = sys.argv[1:]
  digits = int(args[0])
  print(numbers(digits))


if __name__ == '__main__':
  main()
