## Setup
```
  docker build -t openmpi .
  docker-compose scale mpi_node=3 mpi_head=1
  chmod 400 ssh/id_rsa (generate idrsa)
  ssh -i ssh/id_rsa -p $DOCKER_HEAD_PORT mpirun@localhost (docker ps to get the head port)
```

## Create hosts file
* From /etc/hosts to scripts/hosts (copy only the IP adresses, nothing else) 
```
  docker inspect -f "{{ .NetworkSettings.IPAddress }}" $NODE_CONTAINER_NAME
  (\d+\.\d+\.\d\.\d)(.*)
```

## Run
```
  mpiexec -hostfile hosts -n 3 python main.py $DIGITS
  ./test_script.sh main.py > Resultados_GX.txt
```
## Compile
```
  mpicc primes.v2.c -o primes -lm
```
