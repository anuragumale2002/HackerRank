#!/bin/python3

import math
import os
import random
import re
import sys
import heapq
#
# Complete the 'minimumAverage' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY customers as parameter.
#

def minimumAverage(customers):
    # Write your code here
    customers.sort(key=lambda x: x[0])
    n = len(customers)
    i = 0
    time = 0
    total_wait = 0
    heap = []  # (cook_time, arrival_time)

    while i < n or heap:
        if not heap and time < customers[i][0]:
            time = customers[i][0]

        while i < n and customers[i][0] <= time:
            arrival, cook = customers[i][0], customers[i][1]
            heapq.heappush(heap, (cook, arrival))
            i += 1

        cook, arrival = heapq.heappop(heap)
        time += cook
        total_wait += time - arrival

    return total_wait // n

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    customers = []

    for _ in range(n):
        customers.append(list(map(int, input().rstrip().split())))

    result = minimumAverage(customers)

    fptr.write(str(result) + '\n')

    fptr.close()
