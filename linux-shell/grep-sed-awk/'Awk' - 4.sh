awk 'BEGIN{i=1}{line[i++]=$0}END{j=1; while (j<i) {print line[j]";"line[j+1]; j+=2}}'
