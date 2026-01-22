#!/bin/python3
import sys
import os
import math
import heapq

# Costly Intervals
# cost(l,r) = (OR-AND) - (MAX-MIN) = (OR-AND) + (MIN-MAX)

def costlyIntervals(n, k, A):
    # -------------------------
    # Sparse Table for MIN and MAX (RMQ in O(1))
    # We'll query (MIN - MAX) quickly.
    # -------------------------
    lg = [0] * (n + 1)
    for i in range(2, n + 1):
        lg[i] = lg[i // 2] + 1

    K = lg[n]
    st_min = [A[:] ]
    st_max = [A[:] ]

    j = 1
    while (1 << j) <= n:
        length = 1 << j
        half = length >> 1
        prev_min = st_min[j - 1]
        prev_max = st_max[j - 1]
        cur_min = [0] * (n - length + 1)
        cur_max = [0] * (n - length + 1)
        for i in range(0, n - length + 1):
            a1 = prev_min[i]
            a2 = prev_min[i + half]
            cur_min[i] = a1 if a1 < a2 else a2

            b1 = prev_max[i]
            b2 = prev_max[i + half]
            cur_max[i] = b1 if b1 > b2 else b2
        st_min.append(cur_min)
        st_max.append(cur_max)
        j += 1

    def min_minus_max(l, r):
        # returns MIN(l..r) - MAX(l..r)
        length = r - l + 1
        j = lg[length]
        right_start = r - (1 << j) + 1

        mn1 = st_min[j][l]
        mn2 = st_min[j][right_start]
        mn = mn1 if mn1 < mn2 else mn2

        mx1 = st_max[j][l]
        mx2 = st_max[j][right_start]
        mx = mx1 if mx1 > mx2 else mx2

        return mn - mx

    # ---------------------------------------------------------
    # For each i, maintain compressed segments of starts:
    # Each segment represents a range of start indices [l..r]
    # that yields the same (OR, AND) for subarray [start..i].
    #
    # This list stays small (<= ~30) because OR/AND change limited by bits.
    # ---------------------------------------------------------
    cur = []  # list of tuples (l, r, orv, andv)

    # intervals_by_start[s] = list of (end, length) for best interval ending at end and starting at s
    intervals_by_start = [[] for _ in range(n)]

    for i in range(n):
        ai = A[i]

        # update existing segments by including A[i]
        updated = []
        for (l, r, orv, andv) in cur:
            updated.append((l, r, orv | ai, andv & ai))
        # add the new subarray [i..i]
        updated.append((i, i, ai, ai))

        # merge adjacent segments with identical (OR, AND)
        merged = []
        for (l, r, orv, andv) in updated:
            if merged and merged[-1][2] == orv and merged[-1][3] == andv:
                # extend previous segment's r
                pl, pr, por, pand = merged[-1]
                merged[-1] = (pl, r, por, pand)
            else:
                merged.append((l, r, orv, andv))
        cur = merged

        # find the longest valid interval ending at i:
        # scan segments from smallest l upward; first segment that can satisfy
        # gives the minimal start -> maximal length.
        found_start = -1
        for (l, r, orv, andv) in cur:
            base = (orv - andv)  # OR-AND part is constant within this segment

            # check(x) = (MIN(x..i)-MAX(x..i)) + (OR-AND) >= k
            def check(x):
                return min_minus_max(x, i) + base >= k

            if check(r):
                # binary search minimal x in [l..r] that satisfies check
                lo, hi = l, r
                ans = r
                while lo <= hi:
                    mid = (lo + hi) >> 1
                    if check(mid):
                        ans = mid
                        hi = mid - 1
                    else:
                        lo = mid + 1
                found_start = ans
                length = i - ans + 1
                intervals_by_start[ans].append((i, length))
                break

    # ---------------------------------------------------------
    # Sweep line to compute answer per index t:
    # Add intervals starting at t; keep a max-heap by length, and drop expired.
    # Each interval (start, end, length) covers all indices in [start..end].
    # ---------------------------------------------------------
    ans = [-1] * n
    heap = []  # store (-length, end)

    for t in range(n):
        for (end, length) in intervals_by_start[t]:
            heapq.heappush(heap, (-length, end))

        while heap and heap[0][1] < t:
            heapq.heappop(heap)

        if heap:
            ans[t] = -heap[0][0]
        else:
            ans[t] = -1

    return ans


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n_k = sys.stdin.readline().split()
    n = int(n_k[0])
    k = int(n_k[1])

    A = list(map(int, sys.stdin.readline().split()))

    result = costlyIntervals(n, k, A)

    fptr.write('\n'.join(map(str, result)))
    fptr.write('\n')
    fptr.close()
