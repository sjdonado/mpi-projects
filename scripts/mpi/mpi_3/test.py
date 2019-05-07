from mpi4py import MPI
import numpy as np
import time
import sys

shared_comm = MPI.COMM_WORLD.Split_type(MPI.COMM_TYPE_SHARED)
print("Shared comm contains: ", shared_comm.Get_size(), " processes")

shared_comm.Barrier()

leader_rank = 0
is_leader = shared_comm.rank == leader_rank

# Set up a large array as example
_nModes = 45

float_size = MPI.DOUBLE.Get_size()

print("COMM has ", shared_comm.Get_size(), " processes")

size = (_nModes)

if is_leader:
  total_size = np.prod(size)
  nbytes = total_size * float_size
  print("Expected array size is ", nbytes/(1024.**3), " GB")
else:
  nbytes = 0

# Create the shared memory, or get a handle based on shared communicator                                                                  
shared_comm.Barrier()                      
win = MPI.Win.Allocate_shared(nbytes, float_size, comm=shared_comm)
# Construct the array                                                                                                                     

buf, itemsize = win.Shared_query(leader_rank)
# _storedZModes = np.ndarray(buffer=buf, dtype='d', shape=size)

# Fill the shared array with only the leader rank
win.Fence()
if is_leader:
  print("RANK: ", shared_comm.Get_rank() , " is filling the array ")
  #_storedZModes[...] = np.ones(size)
  win.Put(np.array([1, 2, 3], dtype='i'), leader_rank)
  print("RANK: ", shared_comm.Get_rank() , " SUCCESSFULLY filled the array ")
  print("Sum should return ", np.prod(size))
win.Fence()

win.Fence()
if shared_comm.rank == 2:
  print("RANK: ", shared_comm.Get_rank() , " is querying the array "); sys.stdout.flush()
  # Do a (bad) explicit sum to make clear it is not a copy problem within numpy sum()
  array = np.empty(3, dtype='i')
  win.Get(array, leader_rank)
  print("RANK: ", shared_comm.Get_rank() , " is filling the array ")
  np.append(array, 4)
  win.Put(np.array([1, 2, 3, 4, 5], dtype='i'), leader_rank)
  array = np.empty(5, dtype='i')
  win.Get(array, leader_rank)
  print(array)                                                            
  # print("RANK: ", shared_comm.Get_rank() , " SUCCESSFULLY queried the array ", tSUM)
win.Fence()

# Access the array - if we don't do this, then memory usage is as expected. If I do this, then I find that memory usage goes up to twice t
# he size, as if it's copying the array on access
if shared_comm.rank == 1:
  print("RANK: ", shared_comm.Get_rank() , " is querying the array "); sys.stdout.flush()
  # Do a (bad) explicit sum to make clear it is not a copy problem within numpy sum()
  array = np.empty(3, dtype='i')
  win.Get(array, leader_rank)
  print(array)                                                                                    
  # print("RANK: ", shared_comm.Get_rank() , " SUCCESSFULLY queried the array ", tSUM)

shared_comm.Barrier()

# Wait for a while to make sure slurm notices any issues before finishing
time.sleep(500)