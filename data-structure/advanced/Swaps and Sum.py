#!/usr/bin/env python3
import sys
import random

sys.setrecursionlimit(1_000_000)

# ---------- Implicit Treap (by position) ----------
class Node:
    __slots__ = ("val", "prio", "cnt", "sum", "l", "r")
    def __init__(self, val: int):
        self.val = val
        self.prio = random.getrandbits(31)
        self.cnt = 1
        self.sum = val
        self.l = None
        self.r = None

def cnt(t):
    return t.cnt if t else 0

def sm(t):
    return t.sum if t else 0

def upd(t):
    if t:
        t.cnt = 1 + cnt(t.l) + cnt(t.r)
        t.sum = t.val + sm(t.l) + sm(t.r)

def split(t, k):
    """
    Split by size: first k nodes go to left, rest to right.
    Returns (a, b).
    """
    if not t:
        return (None, None)
    if cnt(t.l) >= k:
        a, b = split(t.l, k)
        t.l = b
        upd(t)
        return (a, t)
    else:
        a, b = split(t.r, k - cnt(t.l) - 1)
        t.r = a
        upd(t)
        return (t, b)

def merge(a, b):
    if not a or not b:
        return a or b
    if a.prio > b.prio:
        a.r = merge(a.r, b)
        upd(a)
        return a
    else:
        b.l = merge(a, b.l)
        upd(b)
        return b

class ImplicitTreap:
    __slots__ = ("root",)
    def __init__(self):
        self.root = None

    def append(self, val: int):
        self.root = merge(self.root, Node(val))

    def range_sum(self, l: int, r: int) -> int:
        # split root into [0..r], [r+1..]
        left, right = split(self.root, r + 1)
        # split left into [0..l-1], [l..r]
        a, mid = split(left, l)
        ans = sm(mid)
        # restore
        self.root = merge(a, merge(mid, right))
        return ans

def tswap(t1: ImplicitTreap, l1: int, r1: int, t2: ImplicitTreap, l2: int, r2: int):
    """
    Swap subsegment [l1..r1] in t1 with [l2..r2] in t2 (0-indexed within each treap).
    """
    # t1: p1 | p2 | p3
    p2, p3 = split(t1.root, r1 + 1)
    p1, p2 = split(p2, l1)

    # t2: q1 | q2 | q3
    q2, q3 = split(t2.root, r2 + 1)
    q1, q2 = split(q2, l2)

    # swap p2 <-> q2
    t1.root = merge(p1, merge(q2, p3))
    t2.root = merge(q1, merge(p2, q3))

# ---------- Main (matches setter mapping) ----------
def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)
    n = next(it)
    q = next(it)

    t = [ImplicitTreap(), ImplicitTreap()]

    # build: a[0] into t[0], a[1] into t[1], ...
    for i in range(n):
        v = next(it)
        t[i & 1].append(v)

    out = []

    for _ in range(q):
        typ = next(it)
        l = next(it) - 1
        r = next(it) - 1

        # compute ql/qr for parity 0 and 1 exactly like setter
        ql = [0, 0]
        qr = [0, 0]
        for par in (0, 1):
            if l == r and (l & 1) != par:
                ql[par] = 0
                qr[par] = -1
            else:
                ql[par] = (l // 2) if ((l & 1) == par) else ((l + 1) // 2)
                qr[par] = (r // 2) if ((r & 1) == par) else ((r - 1) // 2)

        if typ == 1:
            # swap mapped segments between even/odd treaps
            tswap(t[0], ql[0], qr[0], t[1], ql[1], qr[1])
        else:
            ans = 0
            if ql[0] <= qr[0]:
                ans += t[0].range_sum(ql[0], qr[0])
            if ql[1] <= qr[1]:
                ans += t[1].range_sum(ql[1], qr[1])
            out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()


# Timing out