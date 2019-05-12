#!/usr/bin/python

from mpi4py import MPI

def main():
  root_process = 0

  comm = MPI.COMM_WORLD
  rank = comm.Get_rank()

  if rank == root_process:
    size = comm.Get_size()
    ranks_range = range(size)
  else:
    ranks_range = None

  my_rank = comm.scatter(ranks_range, root=root_process)
  data = comm.gather(pow(my_rank, 2), root=root_process)

  if rank == root_process:
    print('root received', data)

if __name__ == '__main__':
  main()