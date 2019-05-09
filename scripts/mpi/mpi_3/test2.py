import numpy as np
import random as rand
from mpi4py import MPI

world_comm = MPI.COMM_WORLD
node_comm  = world_comm.Split_type(MPI.COMM_TYPE_SHARED)
size = world_comm.Get_size()

disp_unit = MPI.INT.Get_size()
win = MPI.Win.Allocate_shared(size * disp_unit if node_comm.rank == 0 else 0, disp_unit, comm = node_comm)

buf, itemsize = win.Shared_query(0)

print('RESPONSE', buf, itemsize)
# assert itemsize == MPI.DOUBLE.Get_size()
buf = np.array(buf, dtype='B', copy=False)
ary = np.ndarray(buffer=buf, dtype='i', shape=(size,))

if node_comm.rank == 1:
  ary[:size] = np.arange(size)
node_comm.Barrier()

if node_comm.rank == 0:
  print ary[:size]