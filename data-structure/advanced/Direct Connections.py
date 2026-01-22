#!/bin/python3

import os
import sys

MOD = 1_000_000_007
CUR_POPS = None


class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        while i <= self.n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s


def solve(arr):
    # arr = coordinates (x)
    global CUR_POPS
    xs = arr
    ps = CUR_POPS  # populations (p)

    n = len(xs)

    # coordinate compression
    sorted_x = sorted(set(xs))
    comp = {x: i + 1 for i, x in enumerate(sorted_x)}  # 1-based

    # sort by population asc
    cities = list(zip(ps, xs))
    cities.sort()

    bit_cnt = BIT(len(sorted_x))
    bit_sum = BIT(len(sorted_x))

    total_cnt = 0
    total_sum = 0
    ans = 0

    for p, x in cities:
        idx = comp[x]

        left_cnt = bit_cnt.sum(idx)
        left_sum = bit_sum.sum(idx)

        right_cnt = total_cnt - left_cnt
        right_sum = total_sum - left_sum

        dist_sum = x * left_cnt - left_sum + (right_sum - x * right_cnt)
        ans = (ans + (p % MOD) * (dist_sum % MOD)) % MOD

        bit_cnt.add(idx, 1)
        bit_sum.add(idx, x)
        total_cnt += 1
        total_sum += x

    return ans


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    t = int(sys.stdin.readline().strip())

    for _ in range(t):
        n = int(sys.stdin.readline().strip())

        # coordinates line
        arr = list(map(int, sys.stdin.readline().split()))

        # populations line (THIS WAS MISSING)
        CUR_POPS = list(map(int, sys.stdin.readline().split()))

        result = solve(arr)
        fptr.write(str(result) + '\n')

    fptr.close()
