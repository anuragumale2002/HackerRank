#!/bin/python3

import os
import sys

MOD = 10**9 + 7

class Fenwick:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, delta):
        # i is 1-based
        n = self.n
        bit = self.bit
        while i <= n:
            bit[i] = (bit[i] + delta) % MOD
            i += i & -i

    def sum(self, i):
        # prefix sum, i is 1-based
        s = 0
        bit = self.bit
        while i > 0:
            s += bit[i]
            s %= MOD
            i -= i & -i
        return s

    def range_sum(self, l, r):
        # l, r are 1-based
        return (self.sum(r) - self.sum(l - 1)) % MOD


def polynomialDivision(a, b, queries):
    global c, n

    a %= MOD
    b %= MOD

    # root r = -b / a (mod MOD)
    inv_a = pow(a, MOD - 2, MOD)
    r = (-b * inv_a) % MOD

    out = []

    # Special case: r == 0
    # P(0) = c[l] only, so divisible iff c[l] == 0.
    if r == 0:
        for typ, x, y in queries:
            if typ == 1:
                i = x
                val = y % MOD
                c[i] = val
            else:
                l = x
                # r endpoint doesn't matter for evaluation at 0
                out.append("Yes" if (c[l] % MOD) == 0 else "No")
        return out

    # Precompute powers of r and inverse powers
    pow_r = [1] * n
    for i in range(1, n):
        pow_r[i] = (pow_r[i - 1] * r) % MOD

    inv_r = pow(r, MOD - 2, MOD)
    pow_inv_r = [1] * n
    for i in range(1, n):
        pow_inv_r[i] = (pow_inv_r[i - 1] * inv_r) % MOD

    # Build Fenwick on w[i] = c[i] * r^i
    fw = Fenwick(n)
    for i in range(n):
        fw.add(i + 1, (c[i] % MOD) * pow_r[i] % MOD)

    for typ, x, y in queries:
        if typ == 1:
            i = x
            newv = y % MOD
            oldv = c[i] % MOD
            if newv != oldv:
                c[i] = newv
                delta = (newv - oldv) % MOD
                fw.add(i + 1, delta * pow_r[i] % MOD)

        else:
            l = x
            rr = y
            s = fw.range_sum(l + 1, rr + 1)          # sum c[i]*r^i from i=l..rr
            val = (s * pow_inv_r[l]) % MOD           # multiply by r^{-l} => P(r)
            out.append("Yes" if val == 0 else "No")

    return out


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    first_multiple_input = input().rstrip().split()
    n = int(first_multiple_input[0])
    a = int(first_multiple_input[1])
    b = int(first_multiple_input[2])
    q = int(first_multiple_input[3])

    c = list(map(int, input().rstrip().split()))

    queries = []
    for _ in range(q):
        queries.append(list(map(int, input().rstrip().split())))

    result = polynomialDivision(a, b, queries)

    fptr.write('\n'.join(result))
    fptr.write('\n')
    fptr.close()
