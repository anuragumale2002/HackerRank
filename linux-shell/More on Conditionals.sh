read A
read B
read C
if [ "$A" == "$B" ]; then
    if [ "$A" == "$C" ]; then
        echo "EQUILATERAL"
    else
        echo "ISOSCELES"
    fi
elif [ "$A" == "$C" -o "$B" == "$C" ]; then
    echo "ISOSCELES"
else
    echo "SCALENE"
fi
