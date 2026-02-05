# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

MOD = 10**9 + 7
INV2 = (MOD + 1) // 2

# -------- Fenwick: range add, point query --------
class BIT:
    __slots__ = ("n", "bit")
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, i, v):
        n = self.n
        bit = self.bit
        v %= MOD
        while i <= n:
            bit[i] = (bit[i] + v) % MOD
            i += i & -i

    def sum(self, i):
        s = 0
        bit = self.bit
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s % MOD

    def range_add(self, l, r, v):
        if l > r:
            return
        v %= MOD
        self.add(l, v)
        self.add(r + 1, -v)

    def point(self, i):
        return self.sum(i)

def solve():
    N, E, R = map(int, input().split())
    g = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        x, y = map(int, input().split())
        g[x].append(y)
        g[y].append(x)

    # -------- Root at R, build parent/depth/tin/tout with iterative DFS --------
    LOG = (N).bit_length()
    up = [[0] * (N + 1) for _ in range(LOG)]
    parent = [0] * (N + 1)
    depth = [0] * (N + 1)
    tin = [0] * (N + 1)
    tout = [0] * (N + 1)
    timer = 0

    stack = [(R, 0, 0)]  # (u, p, state) state 0 enter, 1 exit
    while stack:
        u, p, state = stack.pop()
        if state == 0:
            timer += 1
            tin[u] = timer
            parent[u] = p
            up[0][u] = p
            stack.append((u, p, 1))
            for v in g[u]:
                if v == p:
                    continue
                depth[v] = depth[u] + 1
                stack.append((v, u, 0))
        else:
            tout[u] = timer

    for k in range(1, LOG):
        prev = up[k - 1]
        cur = up[k]
        for v in range(1, N + 1):
            cur[v] = prev[prev[v]]

    def is_anc(a, b):
        return tin[a] <= tin[b] <= tout[a]

    def lca(a, b):
        if is_anc(a, b):
            return a
        if is_anc(b, a):
            return b
        x = a
        for k in range(LOG - 1, -1, -1):
            nx = up[k][x]
            if nx and not is_anc(nx, b):
                x = nx
        return parent[x]

    # 3 BITs for coefficients of depth^2, depth, constant in pref(u)
    bitA = BIT(N)
    bitB = BIT(N)
    bitC = BIT(N)

    def pref(u):
        """sum of node values on path R..u"""
        du = depth[u]
        t = tin[u]
        A = bitA.point(t)
        B = bitB.point(t)
        C = bitC.point(t)
        return (A * du % MOD * du + B * du + C) % MOD

    out = []

    for _ in range(E):
        parts = input().split()
        if parts[0] == b'U' or parts[0] == 'U':
            T = int(parts[1])
            V = int(parts[2]) % MOD
            K = int(parts[3]) % MOD
            dT = depth[T]

            # pref(u) contribution (for u in subtree(T)):
            # f = V*(diff+1) + K*diff*(diff+1)/2 where diff=depth[u]-depth[T]
            # Expands to A*du^2 + B*du + C with:
            A = K * INV2 % MOD
            B = (V + A - K * dT) % MOD
            C = (V * (1 - dT) + A * ((dT * dT - dT) % MOD)) % MOD

            l, r = tin[T], tout[T]
            bitA.range_add(l, r, A)
            bitB.range_add(l, r, B)
            bitC.range_add(l, r, C)

        else:  # 'Q'
            A = int(parts[1])
            B = int(parts[2])
            L = lca(A, B)

            pA = pref(A)
            pB = pref(B)
            pL = pref(L)
            pPL = pref(parent[L]) if parent[L] != 0 else 0
            valL = (pL - pPL) % MOD

            ans = (pA + pB - 2 * pL + valL) % MOD
            out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
