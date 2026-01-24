while read line
do
    my_array=("${my_array[@]}" $line)
done
declare -a patter=( ${my_array[@]/*[aA]*/} )
echo ${patter[@]}
