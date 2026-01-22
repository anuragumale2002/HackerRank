#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'contacts' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts 2D_STRING_ARRAY queries as parameter.
#

def contacts(queries):
    # Write your code here
    root = {}          # trie root: dict(char -> node)
    cnt_key = "#"      # stores prefix count at each node

    res = []
    for op, s in queries:
        if op == "add":
            node = root
            for ch in s:
                nxt = node.get(ch)
                if nxt is None:
                    nxt = {cnt_key: 0}
                    node[ch] = nxt
                nxt[cnt_key] += 1
                node = nxt
        else:  # "find"
            node = root
            ok = True
            for ch in s:
                node = node.get(ch)
                if node is None:
                    ok = False
                    break
            res.append(node[cnt_key] if ok else 0)
    return res


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    queries_rows = int(input().strip())

    queries = []

    for _ in range(queries_rows):
        queries.append(input().rstrip().split())

    result = contacts(queries)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
