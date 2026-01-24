while read line
do
    my_array=("${my_array[@]}" $line)
done
echo ${my_array[@]}
