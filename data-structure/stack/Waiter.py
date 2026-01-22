#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'waiter' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER_ARRAY number
#  2. INTEGER q
#

def waiter(number, q):
    # Write your code here
    # --- generate first q primes ---
    primes = []
    candidate = 2
    while len(primes) < q:
        is_prime = True
        for p in primes:
            if p * p > candidate:
                break
            if candidate % p == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(candidate)
        candidate += 1 if candidate == 2 else 2  # after 2, check only odd numbers

    ans = []
    A = number[:]   # stack with TOP at end (HackerRank expects this)

    for p in primes:
        A_next = []
        B = []

        # process from top to bottom by popping from end
        while A:
            x = A.pop()
            if x % p == 0:
                B.append(x)
            else:
                A_next.append(x)

        # move B to answers (top to bottom)
        while B:
            ans.append(B.pop())

        A = A_next

    # after q iterations, dump remaining A (top to bottom)
    while A:
        ans.append(A.pop())

    return ans

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    q = int(first_multiple_input[1])

    number = list(map(int, input().rstrip().split()))

    result = waiter(number, q)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')

    fptr.close()
