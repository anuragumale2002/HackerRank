#!/usr/bin/env python3
import sys

MOD = 1000000009  # 1e9+9

def precompute_catalan(nmax: int):
    # catalan[0..nmax]
    cat = [0] * (nmax + 1)
    cat[0] = 1
    # Use recurrence: Cn = C(n-1) * (4n-2)/(n+1) mod MOD
    inv = [0] * (nmax + 2)
    inv[1] = 1
    for i in range(2, nmax + 2):
        inv[i] = MOD - (MOD // i) * inv[MOD % i] % MOD

    for n in range(1, nmax + 1):
        cat[n] = cat[n - 1] * (4 * n - 2) % MOD
        cat[n] = cat[n] * inv[n + 1] % MOD
    return cat

def solve_case(arr, alpha, beta, catalan):
    arr.sort()
    n = len(arr)
    a = [x % MOD for x in arr]
    alpha %= MOD
    beta %= MOD

    # f[i][j] = total sum of values at even depth over all BSTs formed from a[i..j] (root depth=0 even)
    # g[i][j] = total sum of values at odd  depth over all BSTs formed from a[i..j]
    f = [[0] * n for _ in range(n)]
    g = [[0] * n for _ in range(n)]

    for i in range(n):
        f[i][i] = a[i]  # single node is at even level
        g[i][i] = 0

    for length in range(2, n + 1):
        for i in range(0, n - length + 1):
            j = i + length - 1
            fe = 0
            go = 0
            for k in range(i, j + 1):
                left_size = k - i
                right_size = j - k
                cntL = catalan[left_size]
                cntR = catalan[right_size]

                # sums for left interval
                if k > i:
                    le = f[i][k - 1]
                    lo = g[i][k - 1]
                else:
                    le = lo = 0

                # sums for right interval
                if k < j:
                    re = f[k + 1][j]
                    ro = g[k + 1][j]
                else:
                    re = ro = 0

                # combine:
                # even = root + (odd of children-subtrees) because child depth flips parity
                fe = (fe + a[k] * cntL % MOD * cntR) % MOD
                fe = (fe + lo * cntR) % MOD
                fe = (fe + ro * cntL) % MOD

                # odd = (even of children-subtrees) after parity flip
                go = (go + le * cntR) % MOD
                go = (go + re * cntL) % MOD

            f[i][j] = fe
            g[i][j] = go

    ans = (alpha * f[0][n - 1] - beta * g[0][n - 1]) % MOD
    return ans

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    t = int(data[0])
    idx = 1

    # n is up to ~150 in accepted solutions; precompute a safe maximum from input.
    ns = []
    tmp_idx = idx
    for _ in range(t):
        n = int(data[tmp_idx]); tmp_idx += 1
        ns.append(n)
        tmp_idx += 2  # alpha beta
        tmp_idx += n  # array
    maxn = max(ns) if ns else 0
    catalan = precompute_catalan(maxn)

    out_lines = []
    for _ in range(t):
        n = int(data[idx]); idx += 1
        alpha = int(data[idx]); beta = int(data[idx + 1]); idx += 2
        arr = list(map(int, data[idx:idx + n])); idx += n
        out_lines.append(str(solve_case(arr, alpha, beta, catalan)))

    sys.stdout.write("\n".join(out_lines))

if __name__ == "__main__":
    main()
