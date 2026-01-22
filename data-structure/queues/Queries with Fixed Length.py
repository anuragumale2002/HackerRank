#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'solve' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER_ARRAY arr
#  2. INTEGER_ARRAY queries
#

def solve(arr, queries):
    # Write your code here
    n = len(arr)
    INF = 10**18

    # prevGreater[i] = index of previous element strictly greater than arr[i], else -1
    prevGreater = [-1] * n
    stack = []
    for i in range(n):
        while stack and arr[stack[-1]] <= arr[i]:
            stack.pop()
        prevGreater[i] = stack[-1] if stack else -1
        stack.append(i)

    # nextGreaterEq[i] = index of next element >= arr[i], else n
    nextGreaterEq = [n] * n
    stack = []
    for i in range(n - 1, -1, -1):
        while stack and arr[stack[-1]] < arr[i]:
            stack.pop()
        nextGreaterEq[i] = stack[-1] if stack else n
        stack.append(i)

    # best[len] = minimum possible maximum value for some window where that maximum's span is len
    best = [INF] * (n + 1)

    for i in range(n):
        span = nextGreaterEq[i] - prevGreater[i] - 1
        if arr[i] < best[span]:
            best[span] = arr[i]

    # For window size d, we need min over spans >= d
    for d in range(n - 1, 0, -1):
        if best[d + 1] < best[d]:
            best[d] = best[d + 1]

    return [best[d] for d in queries]

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    q = int(first_multiple_input[1])

    arr = list(map(int, input().rstrip().split()))

    queries = []

    for _ in range(q):
        queries_item = int(input().strip())
        queries.append(queries_item)

    result = solve(arr, queries)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
