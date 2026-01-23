import sys

# -------- Fenwick for RANGE ADD + POINT QUERY via difference array --------
class Fenwick:
    __slots__ = ("n", "bit")
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        bit = self.bit
        n = self.n
        while i <= n:
            bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        bit = self.bit
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    q = int(next(it))

    # Nodes are 0..n-1 in this problem (see sample) :contentReference[oaicite:1]{index=1}
    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = int(next(it)); v = int(next(it))
        g[u].append(v)
        g[v].append(u)

    # -------- Euler tour + parent/depth via iterative DFS --------
    parent = [-1] * n
    depth = [0] * n
    tin = [0] * n
    tout = [0] * n

    root = 0
    t = 0
    stack = [(root, -1, 0)]  # (u, p, state) state=0 enter, 1 exit
    while stack:
        u, p, st = stack.pop()
        if st == 0:
            parent[u] = p
            tin[u] = t
            t += 1
            stack.append((u, p, 1))
            for v in g[u]:
                if v == p:
                    continue
                depth[v] = depth[u] + 1
                stack.append((v, u, 0))
        else:
            tout[u] = t - 1

    # -------- LCA: binary lifting --------
    LOG = (n).bit_length()
    up = [parent[:] ]  # up[0][v]
    for k in range(1, LOG):
        prev = up[k - 1]
        cur = [-1] * n
        for v in range(n):
            pv = prev[v]
            cur[v] = prev[pv] if pv != -1 else -1
        up.append(cur)

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        # lift a
        diff = depth[a] - depth[b]
        k = 0
        while diff:
            if diff & 1:
                a = up[k][a]
            diff >>= 1
            k += 1
        if a == b:
            return a
        for k in range(LOG - 1, -1, -1):
            na = up[k][a]
            nb = up[k][b]
            if na != nb:
                a = na
                b = nb
        return parent[a]

    # -------- BIT over Euler indices (1-based inside BIT) --------
    bit = Fenwick(n + 2)
    val = [0] * n

    def subtree_add(u, delta):
        # add delta to all nodes in subtree(u) in the "pref" space
        l = tin[u] + 1
        r = tout[u] + 1
        bit.add(l, delta)
        bit.add(r + 1, -delta)

    def pref(u):
        return bit.sum(tin[u] + 1)

    out = []
    for _ in range(q):
        typ = next(it).decode()
        if typ == "1":
            u = int(next(it))
            x = int(next(it))
            delta = x - val[u]
            val[u] = x
            if delta:
                subtree_add(u, delta)
        else:  # "2"
            u = int(next(it))
            v = int(next(it))
            w = lca(u, v)
            ans = pref(u) + pref(v) - 2 * pref(w) + val[w]
            out.append(str(ans))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
