#!/usr/bin/env python3
import sys

MOD = 10**9 + 7

def S(L: int) -> int:
    return L * (L + 1) // 2

def F(L: int) -> int:
    # ordered pairs (a<=b<c<=d) within one segment of length L
    # = C(L+2, 4)
    if L < 2:
        return 0
    return (L - 1) * L * (L + 1) * (L + 2) // 24

class DSU:
    __slots__ = ("p", "sz", "active")
    def __init__(self, n: int):
        self.p = [-1] * n
        self.sz = [0] * n
        self.active = [False] * n

    def find(self, x: int) -> int:
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def make(self, x: int):
        self.p[x] = x
        self.sz[x] = 1
        self.active[x] = True

    def union(self, a: int, b: int) -> int:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return ra
        if self.sz[ra] < self.sz[rb]:
            ra, rb = rb, ra
        self.p[rb] = ra
        self.sz[ra] += self.sz[rb]
        return ra

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    arr = data[1:1+n]

    idxs = list(range(n))
    idxs.sort(key=arr.__getitem__, reverse=True)

    dsu = DSU(n)

    totalS = 0      # sum S(L)
    totalS2 = 0     # sum S(L)^2
    totalF = 0      # sum F(L)

    def add_len(L: int):
        nonlocal totalS, totalS2, totalF
        s = S(L)
        totalS += s
        totalS2 += s * s
        totalF += F(L)

    def rem_len(L: int):
        nonlocal totalS, totalS2, totalF
        s = S(L)
        totalS -= s
        totalS2 -= s * s
        totalF -= F(L)

    def current_pairs() -> int:
        # P = totalF + sum_{i<j} S_i*S_j
        return totalF + (totalS * totalS - totalS2) // 2

    ans = 0
    prevP = 0

    i = 0
    while i < n:
        v = arr[idxs[i]]

        # activate all indices with this value v
        while i < n and arr[idxs[i]] == v:
            pos = idxs[i]
            dsu.make(pos)
            add_len(1)

            # merge with left segment
            if pos - 1 >= 0 and dsu.active[pos - 1]:
                r1 = dsu.find(pos)
                r2 = dsu.find(pos - 1)
                if r1 != r2:
                    rem_len(dsu.sz[r1])
                    rem_len(dsu.sz[r2])
                    root = dsu.union(r1, r2)
                    add_len(dsu.sz[root])

            # merge with right segment
            if pos + 1 < n and dsu.active[pos + 1]:
                r1 = dsu.find(pos)
                r2 = dsu.find(pos + 1)
                if r1 != r2:
                    rem_len(dsu.sz[r1])
                    rem_len(dsu.sz[r2])
                    root = dsu.union(r1, r2)
                    add_len(dsu.sz[root])

            i += 1

        curP = current_pairs()
        delta = curP - prevP
        ans = (ans + (delta % MOD) * (v % MOD)) % MOD
        prevP = curP

    print(ans)

if __name__ == "__main__":
    solve()
