read N
S=0
C=0
while [ $C -lt $N ]; do
    read A
    S=$(($S+$A))
    C=$(($C+1))
done

printf "%.3f" $(echo "$S / $N" | bc -l)
