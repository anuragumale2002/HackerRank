#!/usr/bin/env python3
import sys
from bisect import bisect_left, bisect_right
from math import isqrt

# -------- fast input --------
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
        N = next(it); Q = next(it); V = next(it)  # V unused (y doesn't change)
    except StopIteration:
        return

    pts = []
    for _ in range(N):
        x = next(it)      # unused
        y = next(it)
        f = next(it)
        pts.append((y, f))

    pts.sort()
    ys = [y for y, _ in pts]
    freqs_raw = [f for _, f in pts]

    # compress frequencies
    comp = {}
    freqs = [0] * N
    cur = 0
    for i, f in enumerate(freqs_raw):
        v = comp.get(f)
        if v is None:
            comp[f] = cur
            v = cur
            cur += 1
        freqs[i] = v
    M = cur  # number of distinct frequencies

    # map queries to [L, R] in sorted-by-y array
    qr = []
    for qi in range(Q):
        YU = next(it); YD = next(it); T = next(it)  # T unused
        # inclusive range [YD, YU]
        L = bisect_left(ys, YD)
        R = bisect_right(ys, YU) - 1
        if L > R:
            qr.append((0, -1, qi))  # empty
        else:
            qr.append((L, R, qi))

    # Mo's ordering
    B = max(1, int(N / max(1, isqrt(Q))) )  # good practical block size
    # Alternative simple: B = int(isqrt(N)) + 1

    def mo_key(item):
        l, r, idx = item
        b = l // B
        # odd-even trick to reduce moves
        return (b, r if (b & 1) == 0 else -r)

    order = sorted(qr, key=mo_key)

    # data structures for mode count
    cnt = [0] * M                 # count per frequency
    freqCount = [0] * (N + 1)     # how many frequencies appear exactly k times
    maxCount = 0

    def add(pos):
        nonlocal maxCount
        v = freqs[pos]
        c = cnt[v]
        if c:
            freqCount[c] -= 1
        c += 1
        cnt[v] = c
        freqCount[c] += 1
        if c > maxCount:
            maxCount = c

    def remove(pos):
        nonlocal maxCount
        v = freqs[pos]
        c = cnt[v]
        freqCount[c] -= 1
        c -= 1
        cnt[v] = c
        if c:
            freqCount[c] += 1
        while maxCount > 0 and freqCount[maxCount] == 0:
            maxCount -= 1

    ans = [0] * Q
    curL = 0
    curR = -1

    for L, R, qi in order:
        if R < L:
            ans[qi] = 0
            continue

        while curL > L:
            curL -= 1
            add(curL)
        while curR < R:
            curR += 1
            add(curR)
        while curL < L:
            remove(curL)
            curL += 1
        while curR > R:
            remove(curR)
            curR -= 1

        ans[qi] = maxCount

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()
