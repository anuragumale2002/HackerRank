#!/usr/bin/env python3
import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)

    n = int(next(it))
    m = int(next(it))
    root = int(next(it)) - 1

    adj = [[] for _ in range(n)]
    for _ in range(n - 1):
        a = int(next(it)) - 1
        b = int(next(it)) - 1
        adj[a].append(b)
        adj[b].append(a)

    # read colors and compress to 0..K-1 for faster hashing
    raw_colors = [int(next(it)) for _ in range(n)]
    comp = {}
    cid = [0] * n
    nxt = 0
    for i, c in enumerate(raw_colors):
        v = comp.get(c)
        if v is None:
            comp[c] = nxt
            v = nxt
            nxt += 1
        cid[i] = v

    queries = [int(next(it)) - 1 for _ in range(m)]

    # root the tree iteratively
    parent = [-1] * n
    children = [[] for _ in range(n)]
    order = []
    stack = [root]
    parent[root] = root
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            children[u].append(v)
            stack.append(v)

    # DSU on tree
    maps = [None] * n
    distinct = [0] * n

    for u in reversed(order):
        big = -1
        big_size = -1
        for v in children[u]:
            mv = maps[v]
            if mv is not None:
                sz = len(mv)
                if sz > big_size:
                    big_size = sz
                    big = v

        if big == -1:
            mp = {}
        else:
            mp = maps[big]

        for v in children[u]:
            if v == big:
                continue
            mv = maps[v]
            if mv:
                for col, cnt in mv.items():
                    mp[col] = mp.get(col, 0) + cnt
            maps[v] = None  # free memory

        col_u = cid[u]
        mp[col_u] = mp.get(col_u, 0) + 1

        maps[u] = mp
        distinct[u] = len(mp)

    out = "\n".join(str(distinct[s]) for s in queries)
    sys.stdout.write(out)

if __name__ == "__main__":
    solve()
