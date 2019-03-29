#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <stdbool.h>
#include <mpi.h>
#include <time.h>


main(int argc, char **argv) 
{
  int my_id, root_process, num_procs, ierr, digits, sum, i, j, min, max, interval_size, max_interval, primes_cont;
  clock_t start_time, end_time;
  bool is_prime;
  MPI_Status status;

  /* Let process 0 be the root process. */
  
  root_process = 0;

  /* Now replicate this process to create parallel processes. */

  ierr = MPI_Init(&argc, &argv);

  /* Find out MY process ID, and how many processes were started. */

  ierr = MPI_Comm_rank(MPI_COMM_WORLD, &my_id);
  ierr = MPI_Comm_size(MPI_COMM_WORLD, &num_procs);

  if (my_id == root_process) 
  {
    start_time = clock();
    digits = (int) strtol(argv[1], (char **)NULL, 10);
    // printf("digits: %i, num_procs: %i\n", digits, num_procs);
  }


  /* Then...no matter which process I am:
    *
    * I engage in a broadcast so that the number of intervals is 
    * sent from the root process to the other processes, and ...
    **/
  ierr = MPI_Bcast(&digits, 1, MPI_INT, root_process, MPI_COMM_WORLD);

  /* calculate the limits range */
  min = pow(10, digits - 1);
  max = pow(10, digits);

  interval_size = (int) (max - min) / num_procs;
  max_interval = (my_id + 1) * interval_size + min;

  if(my_id == num_procs)
  {
    max_interval = max;
  }

  // printf("rank: %i, min: %i, max: %i, interval: %i\n", my_id, min, max, max_interval);

  /* then calculate the sum of the areas of the rectangles for
    * which I am responsible.  Start with the (my_id +1)th
    * interval and process every num_procs-th interval thereafter.
    **/
  primes_cont = 0;
  for (i = my_id * interval_size + min; i < max_interval + 1; i += 1) 
  { 
    j = 2;
    is_prime = true;
    while (j <= i / j)
    {
      if (i % j == 0)
      {
        is_prime = false;
        break;
      }
      j += j == 2 ? 1 : 2;
    }
    if (is_prime)
    {
      primes_cont += 1;
    }
  }
  
  // printf("proc %i result: %i\n", my_id, primes_cont);

  /* and finally, engage in a reduction in which all partial sums 
    * are combined, and the grand sum appears in variable "sum" in
    * the root process,
    **/
  ierr = MPI_Reduce(&primes_cont, &sum, 1, MPI_DOUBLE, MPI_SUM, root_process, MPI_COMM_WORLD);

  /* and, if I am the root process, print the result. */

  if (my_id == root_process)
  {
    end_time = clock();
    printf("El numero de primos de %i, digitos es %i, Tiempo: %f\n", digits, sum, (float)(end_time - start_time) / CLOCKS_PER_SEC);
  } 

  /* Close down this processes. */
  ierr = MPI_Finalize();
}
