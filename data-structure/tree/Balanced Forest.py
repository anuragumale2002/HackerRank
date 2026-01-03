#!/bin/python3

import math
import os
import random
import re
import sys

#
# Complete the 'balancedForest' function below.
#
# The function is expected to return an INTEGER.
# The function accepts following parameters:
#  1. INTEGER_ARRAY c
#  2. 2D_INTEGER_ARRAY edges
#

def balancedForest(c, edges):
    # Write your code here
    sys.setrecursionlimit(1_000_000)

    n = len(c)
    g = [[] for _ in range(n)]
    for u, v in edges:
        u -= 1
        v -= 1
        g[u].append(v)
        g[v].append(u)

    # ---------- build parent + order (iterative) ----------
    parent = [-1] * n
    order = []
    stack = [0]
    parent[0] = 0
    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if parent[v] == -1:
                parent[v] = u
                stack.append(v)

    # ---------- subtree sums (postorder) ----------
    sub = c[:]  # start with node value
    for u in reversed(order):
        for v in g[u]:
            if parent[v] == u:
                sub[u] += sub[v]

    S = sub[0]
    INF = 10**30
    ans = INF

    done = set()   # sums from fully processed subtrees (disjoint)
    path = set()   # sums along current root->node path (ancestors)

    # ---------- DFS with explicit enter/exit states ----------
    st = [(0, 0)]  # (node, state) state=0 enter, 1 exit
    while st:
        u, state = st.pop()

        if state == 0:
            s = sub[u]

            # --- checks (adapted from venom1724's Python logic) ---
            # checks = [s, S - 2*s]
            # if 2*s <= S <= 3*s and any(x in done or (x+s) in path for x in checks):
            #     ans = min(ans, 3*s - S)
            # if S > 3*s and ((S - s)/2 in done or (S + s)/2 in path):
            #     ans = min(ans, (S - 3*s)/2)
            # Source: HackerRank discussion comment. :contentReference[oaicite:2]{index=2}

            if 2 * s <= S <= 3 * s:
                w = 3 * s - S  # candidate added value
                x1 = s
                x2 = S - 2 * s
                if (x1 in done) or ((x1 + s) in path) or (x2 in done) or ((x2 + s) in path):
                    if w < ans:
                        ans = w

            if S > 3 * s:
                # need (S - s) even and (S + s) even (same parity anyway)
                if (S - s) % 2 == 0:
                    half1 = (S - s) // 2
                    half2 = (S + s) // 2
                    w = (S - 3 * s) // 2
                    if (half1 in done) or (half2 in path):
                        if w < ans:
                            ans = w

            # enter bookkeeping
            path.add(s)
            st.append((u, 1))
            for v in g[u]:
                if parent[v] == u:
                    st.append((v, 0))

        else:
            # exit bookkeeping
            s = sub[u]
            path.remove(s)
            done.add(s)

    return -1 if ans == INF else ans

if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    q = int(input().strip())

    for q_itr in range(q):
        n = int(input().strip())

        c = list(map(int, input().rstrip().split()))

        edges = []

        for _ in range(n - 1):
            edges.append(list(map(int, input().rstrip().split())))

        result = balancedForest(c, edges)

        fptr.write(str(result) + '\n')

    fptr.close()
