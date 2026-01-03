#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'swapNodes' function below.
#
# The function is expected to return a 2D_INTEGER_ARRAY.
# The function accepts following parameters:
#  1. 2D_INTEGER_ARRAY indexes
#  2. INTEGER_ARRAY queries
#

def swapNodes(indexes, queries):
    # Write your code here
    from collections import deque

    class Node:
        def __init__(self, val):
            self.val = val
            self.left = None
            self.right = None

    # Step 1: Build the tree
    nodes = [None] + [Node(i) for i in range(1, len(indexes) + 1)]

    for i, (l, r) in enumerate(indexes):
        if l != -1:
            nodes[i + 1].left = nodes[l]
        if r != -1:
            nodes[i + 1].right = nodes[r]

    root = nodes[1]

    def swap_iterative(k):
        queue = deque()
        queue.append((root, 1))  # (node, depth)

        while queue:
            node, depth = queue.popleft()
            if node is None:
                continue
            if depth % k == 0:
                node.left, node.right = node.right, node.left
            queue.append((node.left, depth + 1))
            queue.append((node.right, depth + 1))

    def inorder_iterative():
        result = []
        stack = []
        current = root

        while stack or current:
            while current:
                stack.append(current)
                current = current.left
            current = stack.pop()
            result.append(current.val)
            current = current.right

        return result

    # Step 3: Process queries
    output = []
    for k in queries:
        swap_iterative(k)
        output.append(inorder_iterative())

    return output

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input().strip())

    indexes = []

    for _ in range(n):
        indexes.append(list(map(int, input().rstrip().split())))

    queries_count = int(input().strip())

    queries = []

    for _ in range(queries_count):
        queries_item = int(input().strip())
        queries.append(queries_item)

    result = swapNodes(indexes, queries)

    fptr.write('\n'.join([' '.join(map(str, x)) for x in result]))
    fptr.write('\n')

    fptr.close()
