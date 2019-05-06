# Build cluster and connect to head
```
  ./connect
```

# Run script inside head
```
  bash
  mpiexec -n $CORES --hostfile ~/scripts/hosts python $1 $n
```

## Build openmpi image
```
  docker build -t openmpi .
```

## Create hosts file
* From /etc/hosts to scripts/hosts (copy only the IP adresses, nothing else) 
```
  docker inspect -f "{{ .NetworkSettings.IPAddress }}" $NODE_CONTAINER_NAME
```

## Compile mpi binary
```
  mpicc primes.v2.c -o primes -lm
```
