read N
result=0
read line
for i in $line
do
    result=`echo $((result ^ $i))`
done
echo $result
