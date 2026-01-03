#!/bin/python3

import math
import os
import random
import re
import sys
from collections import deque
import heapq
#
# Complete the 'treeCoordinates' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. 2D_INTEGER_ARRAY edges
#  3. 2D_INTEGER_ARRAY points
#

def treeCoordinates(n, edges, points):
    # Write your code here
    sys.setrecursionlimit(300000)

    # ---------- build tree ----------
    g = [[] for _ in range(n + 1)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # ---------- BFS helper ----------
    def bfs_far(src):
        dist = [-1] * (n + 1)
        q = deque([src])
        dist[src] = 0
        far = src
        while q:
            u = q.popleft()
            if dist[u] > dist[far]:
                far = u
            for v in g[u]:
                if dist[v] == -1:
                    dist[v] = dist[u] + 1
                    q.append(v)
        return far, dist

    # tree diameter endpoints: a -- b
    a, _ = bfs_far(1)
    b, _ = bfs_far(a)

    # ---------- Euler tour (iterative) + depths ----------
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    first = [-1] * (n + 1)
    euler = []

    stack = [(a, 0, 0)]  # (node, parent, next_index_in_adj)
    parent[a] = 0
    depth[a] = 0

    while stack:
        u, p, i = stack[-1]
        if i == 0:
            if first[u] == -1:
                first[u] = len(euler)
            euler.append(u)

        if i < len(g[u]):
            v = g[u][i]
            stack[-1] = (u, p, i + 1)
            if v == p:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            stack.append((v, u, 0))
        else:
            stack.pop()
            if stack:
                euler.append(stack[-1][0])

    L = len(euler)
    euler_depth = [depth[x] for x in euler]

    # ---------- RMQ Sparse Table for LCA ----------
    log = [0] * (L + 1)
    for i in range(2, L + 1):
        log[i] = log[i // 2] + 1

    st = [list(range(L))]
    k = 1
    while (1 << k) <= L:
        prev = st[k - 1]
        span = 1 << (k - 1)
        cur = [0] * (L - (1 << k) + 1)
        for i in range(len(cur)):
            i1 = prev[i]
            i2 = prev[i + span]
            cur[i] = i1 if euler_depth[i1] <= euler_depth[i2] else i2
        st.append(cur)
        k += 1

    def lca(u, v):
        i, j = first[u], first[v]
        if i > j:
            i, j = j, i
        k = log[j - i + 1]
        i1 = st[k][i]
        i2 = st[k][j - (1 << k) + 1]
        return euler[i1] if euler_depth[i1] <= euler_depth[i2] else euler[i2]

    def dist(u, v):
        w = lca(u, v)
        return depth[u] + depth[v] - 2 * depth[w]

    # ---------- build candidate set (key trick to avoid O(m^2)) ----------
    # We compute a few "extreme" score functions based on diameter endpoint b.
    # Then we only brute-force among ~800 points.
    K = 250  # safe in Python; you can try 200/300 too

    def lca_with_b(u):
        return depth[lca(u, b)]

    # store: (key, idx)
    top1, top3 = [], []
    bot2, bot4 = [], []

    # We'll maintain small heaps manually (faster than sorting all m)
    # top heaps as min-heap of size K, bottom heaps as max-heap of size K (use negative)
    def push_top(heap, key, idx):
        if len(heap) < K:
            heapq.heappush(heap, (key, idx))
        else:
            if key > heap[0][0]:
                heapq.heapreplace(heap, (key, idx))

    def push_bot(heap, key, idx):
        # store (-key, idx) so heap[0] is the *largest* key (worst among bottom)
        nk = -key
        if len(heap) < K:
            heapq.heappush(heap, (nk, idx))
        else:
            if nk > heap[0][0]:  # means key < current worst bottom key
                heapq.heapreplace(heap, (nk, idx))

    for idx, (x, y) in enumerate(points):
        lx = lca_with_b(x)
        ly = lca_with_b(y)

        k1 = depth[x] + depth[y]
        k2 = -depth[x] - depth[y] + 2 * lx + 2 * ly
        k3 = depth[x] + depth[y] - 2 * lx
        k4 = -depth[x] - depth[y] + 2 * ly

        push_top(top1, k1, idx)   # want max
        push_bot(bot2, k2, idx)   # want min
        push_top(top3, k3, idx)   # want max
        push_bot(bot4, k4, idx)   # want min

    cand_idx = set()
    for _, i in top1: cand_idx.add(i)
    for _, i in top3: cand_idx.add(i)
    for _, i in bot2: cand_idx.add(i)
    for _, i in bot4: cand_idx.add(i)

    cand = [points[i] for i in cand_idx]
    c = len(cand)

    # ---------- brute force only among candidates ----------
    ans = 0
    for i in range(c):
        x1, y1 = cand[i]
        for j in range(i + 1, c):
            x2, y2 = cand[j]
            d = dist(x1, x2) + dist(y1, y2)
            if d > ans:
                ans = d

    return ans


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()

    n = int(first_multiple_input[0])

    m = int(first_multiple_input[1])

    edges = []

    for _ in range(n - 1):
        edges.append(list(map(int, input().rstrip().split())))

    points = []

    for _ in range(m):
        points.append(list(map(int, input().rstrip().split())))

    result = treeCoordinates(n, edges, points)

    fptr.write(str(result) + '\n')

    fptr.close()
