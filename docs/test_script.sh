echo "RESULTADOS DE ALGORITMO PRIMOS"
echo "------------------------------"
echo "------------------------------"

echo "------ TEST BEGINS -----------"
for cores in {2..16..2}
do
echo "----------------------------------"
echo "Numero de cores funcionando -->"  $cores
	for n in {2..8..2}
	do
	 echo "Longitud de primos -->"  $n
	 mpiexec -n $cores --hostfile hosts python $1 $n
	done
done

echo "--------------------------------"
echo "---------------END--------------"

