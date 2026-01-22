#!/bin/python3
import sys
import math

def maximumValue(a):
    sys.setrecursionlimit(1_000_000)
    n = len(a)
    ans = 0  # at least 0 (single element => sum-max = 0)

    def solve(l, r):
        nonlocal ans
        if l > r:
            return
        if l == r:
            # single element subarray gives 0
            return

        mid = (l + r) >> 1

        # Build right prefixes: mid..j
        right = []
        s = 0
        mx = -10**30
        g = 0
        for j in range(mid, r + 1):
            v = a[j]
            s += v
            if v > mx:
                mx = v
            g = math.gcd(g, abs(v))
            # subarray [mid..j]
            val = g * (s - mx)
            if val > ans:
                ans = val
            # store (mx, gcd, sum)
            right.append((mx, g, s))

        # Build left prefixes: mid..j (j decreases)
        left = []
        s = 0
        mx = -10**30
        g = 0
        for j in range(mid, l - 1, -1):
            v = a[j]
            s += v
            if v > mx:
                mx = v
            g = math.gcd(g, abs(v))
            # subarray [j..mid]
            val = g * (s - mx)
            if val > ans:
                ans = val
            left.append((mx, g, s))

        # left and right are both in non-decreasing mx order
        # because mx only increases as we extend.

        amid = a[mid]

        # Combine: case where overall MAX comes from the RIGHT side (mx_left <= mx_right)
        mp = {}  # gcd_left -> best (sum_left - a[mid])
        i = 0
        L = len(left)
        for (mxR, gR, sR) in right:
            while i < L and left[i][0] <= mxR:
                mxL, gL, sL = left[i]
                key = gL
                cand = sL - amid  # avoid counting a[mid] twice
                prev = mp.get(key)
                if prev is None or cand > prev:
                    mp[key] = cand
                i += 1

            if mp:
                for gL, best_sumL in mp.items():
                    G = math.gcd(gL, gR)
                    total_sum = best_sumL + sR
                    val = G * (total_sum - mxR)
                    if val > ans:
                        ans = val

        # Combine: case where overall MAX comes from the LEFT side
        mp = {}
        i = 0
        R = len(right)
        for (mxL, gL, sL) in left:
            while i < R and right[i][0] <= mxL:
                mxR, gR, sR = right[i]
                key = gR
                cand = sR - amid
                prev = mp.get(key)
                if prev is None or cand > prev:
                    mp[key] = cand
                i += 1

            if mp:
                for gR, best_sumR in mp.items():
                    G = math.gcd(gL, gR)
                    total_sum = (sL - amid) + best_sumR + amid  # equals (sL - amid) + sR
                    # simpler:
                    total_sum = (sL - amid) + (best_sumR + amid)  # = (sL - amid) + sR
                    val = G * (total_sum - mxL)
                    if val > ans:
                        ans = val

        # Recurse
        solve(l, mid - 1)
        solve(mid + 1, r)

    solve(0, n - 1)
    return ans


if __name__ == "__main__":
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().split()))
    print(maximumValue(a))
