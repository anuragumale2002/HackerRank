#!/bin/python3

import math
import os
import random
import re
import sys
from collections import deque

#
# Complete the 'minimumMoves' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. STRING_ARRAY grid
#  2. INTEGER startX
#  3. INTEGER startY
#  4. INTEGER goalX
#  5. INTEGER goalY
#

def minimumMoves(grid, startX, startY, goalX, goalY):
    # Write your code here
    n = len(grid)
    INF = 10**9

    dist = [[INF] * n for _ in range(n)]
    dist[startX][startY] = 0

    q = deque()
    q.append((startX, startY))

    while q:
        x, y = q.popleft()
        d = dist[x][y]

        if x == goalX and y == goalY:
            return d

        # Slide in 4 directions
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy

            while 0 <= nx < n and 0 <= ny < n and grid[nx][ny] != 'X':
                if dist[nx][ny] > d + 1:
                    dist[nx][ny] = d + 1
                    q.append((nx, ny))

                nx += dx
                ny += dy

    return dist[goalX][goalY]

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    grid = []

    for _ in range(n):
        grid_item = input()
        grid.append(grid_item)

    first_multiple_input = input().rstrip().split()

    startX = int(first_multiple_input[0])

    startY = int(first_multiple_input[1])

    goalX = int(first_multiple_input[2])

    goalY = int(first_multiple_input[3])

    result = minimumMoves(grid, startX, startY, goalX, goalY)

    fptr.write(str(result) + '\n')

    fptr.close()
