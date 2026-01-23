#!/usr/bin/env python3
import sys

INF_NEG = -10**30

# ---------- Fenwick for prefix sums of B ----------
class Fenwick:
    __slots__ = ("n", "bit")
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, delta):
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] += delta
            i += i & -i

    def sum(self, i):
        s = 0
        bit = self.bit
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

# ---------- Lazy segtree: range add, range max, point set-max ----------
class SegTreeMaxAdd:
    __slots__ = ("n", "mx", "lz")
    def __init__(self, n):
        self.n = n
        self.mx = [INF_NEG] * (4 * n)
        self.lz = [0] * (4 * n)

    def _push(self, v):
        lzv = self.lz[v]
        if lzv:
            lv = v << 1
            rv = lv | 1
            self.mx[lv] += lzv
            self.lz[lv] += lzv
            self.mx[rv] += lzv
            self.lz[rv] += lzv
            self.lz[v] = 0

    def add_range(self, ql, qr, delta, v=1, tl=1, tr=None):
        if tr is None:
            tr = self.n
        if ql > tr or qr < tl:
            return
        if ql <= tl and tr <= qr:
            self.mx[v] += delta
            self.lz[v] += delta
            return
        self._push(v)
        tm = (tl + tr) >> 1
        self.add_range(ql, qr, delta, v << 1, tl, tm)
        self.add_range(ql, qr, delta, (v << 1) | 1, tm + 1, tr)
        self.mx[v] = self.mx[v << 1] if self.mx[v << 1] > self.mx[(v << 1) | 1] else self.mx[(v << 1) | 1]

    def query_max(self, ql, qr, v=1, tl=1, tr=None):
        if tr is None:
            tr = self.n
        if ql > tr or qr < tl:
            return INF_NEG
        if ql <= tl and tr <= qr:
            return self.mx[v]
        self._push(v)
        tm = (tl + tr) >> 1
        a = self.query_max(ql, qr, v << 1, tl, tm)
        b = self.query_max(ql, qr, (v << 1) | 1, tm + 1, tr)
        return a if a > b else b

    def setmax_point(self, pos, val, v=1, tl=1, tr=None):
        if tr is None:
            tr = self.n
        if tl == tr:
            if val > self.mx[v]:
                self.mx[v] = val
            return
        self._push(v)
        tm = (tl + tr) >> 1
        if pos <= tm:
            self.setmax_point(pos, val, v << 1, tl, tm)
        else:
            self.setmax_point(pos, val, (v << 1) | 1, tm + 1, tr)
        self.mx[v] = self.mx[v << 1] if self.mx[v << 1] > self.mx[(v << 1) | 1] else self.mx[(v << 1) | 1]

# ---------- Fast input ----------
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
        if data[i] == 45:
            sign = -1
            i += 1
        v = 0
        while i < n and data[i] > 32:
            v = v * 10 + (data[i] - 48)
            i += 1
        yield sign * v

def solve():
    it = ints()
    try:
        n = next(it)
    except StopIteration:
        return

    X = [0] * n
    A = [0] * n
    B = [0] * n
    for i in range(n):
        X[i] = next(it)
        A[i] = next(it)
        B[i] = next(it)

    # coordinate compression of X (unique by statement) :contentReference[oaicite:3]{index=3}
    xs = sorted(X)
    rank = [0] * n
    # map value->rank using dict (O(n))
    mp = {}
    for idx, val in enumerate(xs, 1):
        mp[val] = idx
    for i in range(n):
        rank[i] = mp[X[i]]

    m = n  # unique coords => ranks 1..n

    fenw = Fenwick(m)
    segL = SegTreeMaxAdd(m)  # stores dp + P(rank-1)
    segR = SegTreeMaxAdd(m)  # stores dp - P(rank)

    best = 0

    for i in range(n):
        r = rank[i]

        # prefix sums of B for already opened restaurants (< i)
        pref_r_1 = fenw.sum(r - 1)
        pref_r = pref_r_1 + fenw.sum(r) - fenw.sum(r - 1)  # but sum(r) is extra log; avoid:
        # better compute pref_r as fenw.sum(r):
        pref_r = fenw.sum(r)

        left_best = segL.query_max(1, r - 1) if r > 1 else INF_NEG
        right_best = segR.query_max(r + 1, m) if r < m else INF_NEG

        cand = 0
        if left_best != INF_NEG:
            v = left_best - pref_r_1
            if v > cand:
                cand = v
        if right_best != INF_NEG:
            v = right_best + pref_r
            if v > cand:
                cand = v

        dp = A[i] + cand
        if dp > best:
            best = dp

        # insert restaurant i into both structures (using current prefix sums)
        segL.setmax_point(r, dp + pref_r_1)
        segR.setmax_point(r, dp - pref_r)

        # now "open" its sadness for future days:
        bi = B[i]
        if bi != 0:
            # L: ranks > r increase by +bi
            if r + 1 <= m:
                segL.add_range(r + 1, m, bi)
            # R: ranks >= r decrease by bi
            segR.add_range(r, m, -bi)

        fenw.add(r, bi)

    if best < 0:
        best = 0  # print 0 if no trip cheers him up :contentReference[oaicite:4]{index=4}
    sys.stdout.write(str(best))

if __name__ == "__main__":
    solve()
