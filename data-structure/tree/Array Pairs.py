#!/bin/python3
import os
import sys
import bisect

def solve(arr):
    # arr is 0-based input; convert to 1-based like setter
    N = len(arr)
    A = [0] + arr[:]  # A[1..N]

    # ---- build L[i], R[i] with monotonic stack ----
    L = [0] * (N + 1)
    R = [0] * (N + 1)

    window = []  # (value, index) decreasing by value
    for i in range(1, N + 1):
        ai = A[i]
        while window and window[-1][0] < ai:
            window.pop()
        L[i] = 1 if not window else window[-1][1] + 1
        window.append((ai, i))

    window.clear()
    for i in range(N, 0, -1):
        ai = A[i]
        while window and window[-1][0] <= ai:
            window.pop()
        R[i] = N if not window else window[-1][1] - 1
        window.append((ai, i))

    # ---- coordinate compress values of A (like set S + unordered_map M) ----
    V = sorted(set(arr))  # sorted unique values
    # map value -> 1..len(V)
    M = {v: i + 1 for i, v in enumerate(V)}
    maxn = len(V) + 2

    # ---- Fenwick tree ----
    bt = [0] * (maxn + 5)

    def update(ind, val):
        while ind <= maxn:
            bt[ind] += val
            ind += ind & -ind

    def query(ind):
        s = 0
        while ind > 0:
            s += bt[ind]
            ind -= ind & -ind
        return s

    # find_ind like setter: r = upper_bound(V, x) (1-based count)
    # if V[-1] <= x => return len(V)
    def find_ind(x):
        # x >= 0
        if V[-1] <= x:
            return len(V)
        # bisect_right gives insertion point in 0..len(V)-1, so count is that
        return bisect.bisect_right(V, x)

    # ---- g array of events, indexed 0..N ----
    # setter uses g[0..1e6], and pushes into:
    # g[i-1], g[i], g[L[i]-1], g[R[i]]
    g = [[] for _ in range(N + 1)]

    # ---- build events exactly like setter ----
    for i in range(1, N + 1):
        li = L[i]
        ri = R[i]
        ai = A[i]

        if i - li <= ri - i:
            # iterate left side
            for j in range(li, i):
                q = ai // A[j]
                g[i - 1].append(-q)
                g[ri].append(q)
            g[i].append(-1)
            g[ri].append(1)
        else:
            # iterate right side
            for j in range(i + 1, ri + 1):
                q = ai // A[j]
                g[li - 1].append(-q)
                g[i].append(q)
            g[li - 1].append(-1)
            g[i - 1].append(1)

    # ---- sweep i=1..N updating BIT and applying events ----
    ans = 0
    for i in range(1, N + 1):
        update(M[A[i]], 1)  # add this value occurrence
        for val in g[i]:
            r = find_ind(abs(val))
            if val < 0:
                ans -= query(r)
            else:
                ans += query(r)

    return ans


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')
    n = int(sys.stdin.readline().strip())
    arr = list(map(int, sys.stdin.readline().split()))
    result = solve(arr)
    fptr.write(str(result) + '\n')
    fptr.close()
