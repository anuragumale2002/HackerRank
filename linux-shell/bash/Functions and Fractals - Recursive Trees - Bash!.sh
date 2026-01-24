ROWS=63
COLS=100
declare -a field

function put {
    field[$(($2 * $COLS + $1))]=$3
}

function fill {
    for y in `seq 0 $(($ROWS - 1))`
    do
        for x in `seq 0 $(($COLS - 1))`
        do
            put $x $y $1
        done
    done
}

function output {
    for y in `seq 0 $(($ROWS - 1))`
    do
        for x in `seq 0 $(($COLS - 1))`
        do
            echo -n  "${field[$(($y * $COLS + $x))]}"
        done
        echo ""
    done
}

function draw_tree {

    if [ $4 -eq 0 ]
    then
        return
    fi

    for i in `seq 0 $(($3 - 1))`
    do
        put $1 $(($2 - $i)) '1'
        put $(($1 - $i - 1)) $(($2 - $3 - $i)) '1'
        put $(($1 + $i + 1)) $(($2 - $3 - $i)) '1'
    done

    draw_tree $(($1 - $3)) $(($2 - 2 * $3)) $(($3 / 2)) $(($4 - 1))
    draw_tree $(($1 + $3)) $(($2 - 2 * $3)) $(($3 / 2)) $(($4 - 1))
}

read N
fill '_'
draw_tree 49 62 16 $N
output
