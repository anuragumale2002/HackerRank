#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'solve' function below.
#
# The function is expected to return an INTEGER.
# The function accepts INTEGER_ARRAY arr as parameter.
#

def solve(arr):
    # Write your code here
    n = len(arr)
    left = [0] * n
    right = [0] * n

    # Nearest greater on left (store 1-based index, else 0)
    st = []
    for i, x in enumerate(arr):
        while st and arr[st[-1]] <= x:
            st.pop()
        left[i] = (st[-1] + 1) if st else 0
        st.append(i)

    # Nearest greater on right (store 1-based index, else 0)
    st = []
    for i in range(n - 1, -1, -1):
        x = arr[i]
        while st and arr[st[-1]] <= x:
            st.pop()
        right[i] = (st[-1] + 1) if st else 0
        st.append(i)

    ans = 0
    for i in range(n):
        prod = left[i] * right[i]
        if prod > ans:
            ans = prod
    return ans

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    arr_count = int(input().strip())

    arr = list(map(int, input().rstrip().split()))

    result = solve(arr)

    fptr.write(str(result) + '\n')

    fptr.close()
