#!/bin/python3

import os
import sys
from bisect import bisect_left

#
# Complete the 'solve' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER_ARRAY c
#  2. 2D_INTEGER_ARRAY tree
#  3. 2D_INTEGER_ARRAY queries
#

def solve(c, tree, queries):
    # ---- setup ----
    n = len(c)
    q = len(queries)

    # compress values in c (0-indexed nodes in c => node id = i+1)
    vals = sorted(set(c))
    comp = [bisect_left(vals, x) for x in c]
    m = len(vals)

    # build adjacency
    g = [[] for _ in range(n + 1)]
    for u, v in tree:
        g[u].append(v)
        g[v].append(u)

    # ---- Euler tour (2n) + LCA (binary lifting) ----
    LOG = (n).bit_length()
    up = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    parent = [0] * (n + 1)

    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    euler = [0] * (2 * n)

    # iterative DFS from root 1
    stack = [1]
    parent[1] = 1
    depth[1] = 0
    it_idx = [0] * (n + 1)

    timer = 0
    tin[1] = timer
    euler[timer] = 1
    timer += 1

    while stack:
        u = stack[-1]
        if it_idx[u] < len(g[u]):
            v = g[u][it_idx[u]]
            it_idx[u] += 1
            if v == parent[u]:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            stack.append(v)

            tin[v] = timer
            euler[timer] = v
            timer += 1
        else:
            tout[u] = timer
            euler[timer] = u
            timer += 1
            stack.pop()

    for v in range(1, n + 1):
        up[0][v] = parent[v]
    for k in range(1, LOG):
        prev = up[k - 1]
        cur = up[k]
        for v in range(1, n + 1):
            cur[v] = prev[prev[v]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1
        if a == b:
            return a
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        return up[0][a]

    def make_interval(u, v):
        # returns (l, r, extra_lca_or_-1) for Mo-on-tree path representation
        if tin[u] > tin[v]:
            u, v = v, u
        w = lca(u, v)
        if w == u:
            return tin[u], tin[v], -1
        else:
            return tout[u], tin[v], w

    # ---- build 2D-Mo queries (two paths per query) ----
    mos = []
    for idx, (w, x, y, z) in enumerate(queries):
        l1, r1, e1 = make_interval(w, x)
        l2, r2, e2 = make_interval(y, z)
        mos.append((l1, r1, e1, l2, r2, e2, idx))

    N = 2 * n
    block = int(N ** (2.0 / 3.0)) or 1

    def mo_key(qu):
        l1, r1, e1, l2, r2, e2, idx = qu
        return (l1 // block, l2 // block, r1 // block, r2)

    mos.sort(key=mo_key)

    # ---- maintain dot product of frequencies and intersection ----
    cntA = [0] * m
    cntB = [0] * m
    inA = bytearray(n + 1)
    inB = bytearray(n + 1)

    dot = 0     # sum_v cntA[v] * cntB[v]
    inter = 0   # number of nodes active in both sets

    # localize for speed
    eulerL = euler
    compL = comp
    cntAL = cntA
    cntBL = cntB
    inAL = inA
    inBL = inB

    def toggleA(node):
        nonlocal dot, inter
        v = compL[node - 1]  # comp is 0-indexed by node-1
        if inAL[node]:
            if inBL[node]:
                inter -= 1
            dot -= cntBL[v]
            cntAL[v] -= 1
            inAL[node] = 0
        else:
            if inBL[node]:
                inter += 1
            dot += cntBL[v]
            cntAL[v] += 1
            inAL[node] = 1

    def toggleB(node):
        nonlocal dot, inter
        v = compL[node - 1]
        if inBL[node]:
            if inAL[node]:
                inter -= 1
            dot -= cntAL[v]
            cntBL[v] -= 1
            inBL[node] = 0
        else:
            if inAL[node]:
                inter += 1
            dot += cntAL[v]
            cntBL[v] += 1
            inBL[node] = 1

    L1 = 0; R1 = -1
    L2 = 0; R2 = -1

    ans = [0] * q

    for (l1, r1, e1, l2, r2, e2, qi) in mos:
        while L1 > l1:
            L1 -= 1
            toggleA(eulerL[L1])
        while R1 < r1:
            R1 += 1
            toggleA(eulerL[R1])
        while L1 < l1:
            toggleA(eulerL[L1])
            L1 += 1
        while R1 > r1:
            toggleA(eulerL[R1])
            R1 -= 1

        while L2 > l2:
            L2 -= 1
            toggleB(eulerL[L2])
        while R2 < r2:
            R2 += 1
            toggleB(eulerL[R2])
        while L2 < l2:
            toggleB(eulerL[L2])
            L2 += 1
        while R2 > r2:
            toggleB(eulerL[R2])
            R2 -= 1

        if e1 != -1:
            toggleA(e1)
        if e2 != -1:
            toggleB(e2)

        # ordered pairs with equal values minus forbidden (u,u) for u in both paths
        ans[qi] = dot - inter

        if e2 != -1:
            toggleB(e2)
        if e1 != -1:
            toggleA(e1)

    return ans


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()
    n = int(first_multiple_input[0])
    q = int(first_multiple_input[1])

    c = list(map(int, input().rstrip().split()))

    tree = []
    for _ in range(n - 1):
        tree.append(list(map(int, input().rstrip().split())))

    queries = []
    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    result = solve(c, tree, queries)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')
    fptr.close()



# passed 3/10 cases others timed out