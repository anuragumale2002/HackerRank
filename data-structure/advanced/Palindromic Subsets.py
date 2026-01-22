#!/bin/python3

import os
import sys

MOD = 1_000_000_007
ALPH = 26
FULLMASK = (1 << ALPH) - 1

def rot(mask, t):
    t %= ALPH
    if t == 0:
        return mask
    return ((mask << t) | (mask >> (ALPH - t))) & FULLMASK

class SegTree:
    def __init__(self, s):
        self.n = len(s)
        self.mask = [0] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
        self._build(1, 0, self.n - 1, s)

    def _build(self, v, tl, tr, s):
        if tl == tr:
            self.mask[v] = 1 << (ord(s[tl]) - 97)
            return
        tm = (tl + tr) // 2
        self._build(v * 2, tl, tm, s)
        self._build(v * 2 + 1, tm + 1, tr, s)
        self.mask[v] = self.mask[v * 2] | self.mask[v * 2 + 1]

    def _apply(self, v, t):
        t %= ALPH
        if t:
            self.mask[v] = rot(self.mask[v], t)
            self.lazy[v] = (self.lazy[v] + t) % ALPH

    def _push(self, v):
        if self.lazy[v]:
            t = self.lazy[v]
            self._apply(v * 2, t)
            self._apply(v * 2 + 1, t)
            self.lazy[v] = 0

    def update(self, l, r, t):
        self._update(1, 0, self.n - 1, l, r, t % ALPH)

    def _update(self, v, tl, tr, l, r, t):
        if l > r:
            return
        if l == tl and r == tr:
            self._apply(v, t)
            return
        self._push(v)
        tm = (tl + tr) // 2
        self._update(v * 2, tl, tm, l, min(r, tm), t)
        self._update(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r, t)
        self.mask[v] = self.mask[v * 2] | self.mask[v * 2 + 1]

    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)

    def _query(self, v, tl, tr, l, r):
        if l > r:
            return 0
        if l == tl and r == tr:
            return self.mask[v]
        self._push(v)
        tm = (tl + tr) // 2
        left = self._query(v * 2, tl, tm, l, min(r, tm))
        right = self._query(v * 2 + 1, tm + 1, tr, max(l, tm + 1), r)
        return left | right

if __name__ == '__main__':
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()

    # precompute powers of 2 up to n
    pow2 = [1] * (n + 1)
    for i in range(1, n + 1):
        pow2[i] = (pow2[i - 1] * 2) % MOD

    st = SegTree(s)

    out = []
    idx = 3
    for _ in range(q):
        typ = int(data[idx]); idx += 1
        if typ == 1:
            i = int(data[idx]); j = int(data[idx + 1]); t = int(data[idx + 2]); idx += 3
            st.update(i, j, t)
        else:
            i = int(data[idx]); j = int(data[idx + 1]); idx += 2
            mask = st.query(i, j)
            L = mask.bit_count()
            length = j - i + 1
            ans = (pow2[length - L] * (L + 1) - 1) % MOD
            out.append(str(ans))

    sys.stdout.write("\n".join(out))
