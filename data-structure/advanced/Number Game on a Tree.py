#!/usr/bin/env python3
import sys
sys.setrecursionlimit(1_000_000)

# ---------- fast input ----------
def ints():
    data = sys.stdin.buffer.read()
    n = len(data)
    i = 0
    while i < n:
        while i < n and data[i] <= 32:
            i += 1
        if i >= n:
            break
        sign = 1
        if data[i] == 45:  # '-'
            sign = -1
            i += 1
        v = 0
        while i < n and data[i] > 32:
            v = v * 10 + (data[i] - 48)
            i += 1
        yield sign * v

# ---------- splitmix64: deterministic 64-bit hash ----------
MASK = (1 << 64) - 1
def splitmix64(x: int) -> int:
    x = (x + 0x9E3779B97F4A7C15) & MASK
    x = (x ^ (x >> 30)) * 0xBF58476D1CE4E5B9 & MASK
    x = (x ^ (x >> 27)) * 0x94D049BB133111EB & MASK
    return x ^ (x >> 31)

def solve():
    it = ints()
    try:
        g = next(it)
    except StopIteration:
        return

    out_lines = []
    hash_cache = {}

    for _ in range(g):
        n = next(it)
        adj = [[] for _ in range(n + 1)]
        for _ in range(n - 1):
            u = next(it); v = next(it); w = next(it)
            # hash weight (cache)
            hw = hash_cache.get(w)
            if hw is None:
                hw = splitmix64(w)
                hash_cache[w] = hw
            adj[u].append((v, hw))
            adj[v].append((u, hw))

        # iterative DFS to compute prefix xors
        px = [0] * (n + 1)
        parent = [0] * (n + 1)
        parent[1] = -1
        stack = [1]
        order = [1]

        while stack:
            u = stack.pop()
            for v, hw in adj[u]:
                if v == parent[u]:
                    continue
                parent[v] = u
                px[v] = px[u] ^ hw
                stack.append(v)
                order.append(v)

        # count equal prefix-xors
        freq = {}
        for u in order:
            x = px[u]
            freq[x] = freq.get(x, 0) + 1

        total_pairs = n * (n - 1) // 2
        losing_pairs = 0
        for c in freq.values():
            losing_pairs += c * (c - 1) // 2

        out_lines.append(str(total_pairs - losing_pairs))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    solve()
