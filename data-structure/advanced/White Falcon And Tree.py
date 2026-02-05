# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
from array import array

sys.setrecursionlimit(1_000_000)
MOD = 1_000_000_007

def affine_power_with_inv(a, b, inv_am1, k):
    # g(x) = a*x + b; return g^k = (A,B)
    if k == 0:
        return 1, 0
    A = pow(a, k, MOD)
    if a == 1:
        B = (b * k) % MOD
    else:
        # B = b * (A - 1) * inv(a - 1)
        B = (b * ((A - 1) % MOD)) % MOD
        B = (B * inv_am1) % MOD
    return A, B

class SegTree:
    __slots__ = ("n", "fA", "fB", "rA", "rB", "lzA", "lzB", "lzI", "has")

    def __init__(self, base_a, base_b):
        n = len(base_a)
        self.n = n
        size = 4 * n if n > 1 else 4

        self.fA = array("I", [1]) * size
        self.fB = array("I", [0]) * size
        self.rA = array("I", [1]) * size
        self.rB = array("I", [0]) * size

        self.lzA = array("I", [0]) * size
        self.lzB = array("I", [0]) * size
        self.lzI = array("I", [0]) * size   # inv(a-1) for lazy assignment
        self.has = bytearray(size)

        self._build(1, 0, n - 1, base_a, base_b)

    def _apply_set(self, idx, l, r, a, b, inv_am1):
        A, B = affine_power_with_inv(a, b, inv_am1, r - l + 1)
        self.fA[idx] = A
        self.fB[idx] = B
        self.rA[idx] = A
        self.rB[idx] = B
        self.lzA[idx] = a
        self.lzB[idx] = b
        self.lzI[idx] = inv_am1
        self.has[idx] = 1

    def _push(self, idx, l, r):
        if self.has[idx] == 0 or l == r:
            return
        m = (l + r) >> 1
        a = self.lzA[idx]
        b = self.lzB[idx]
        inv_am1 = self.lzI[idx]
        li = idx << 1
        ri = li | 1
        self._apply_set(li, l, m, a, b, inv_am1)
        self._apply_set(ri, m + 1, r, a, b, inv_am1)
        self.has[idx] = 0

    def _pull(self, idx):
        li = idx << 1
        ri = li | 1

        # forward = right o left
        a2 = self.fA[ri]; b2 = self.fB[ri]
        a1 = self.fA[li]; b1 = self.fB[li]
        self.fA[idx] = (a2 * a1) % MOD
        self.fB[idx] = (a2 * b1 + b2) % MOD

        # backward = left o right
        a2 = self.rA[li]; b2 = self.rB[li]
        a1 = self.rA[ri]; b1 = self.rB[ri]
        self.rA[idx] = (a2 * a1) % MOD
        self.rB[idx] = (a2 * b1 + b2) % MOD

    def _build(self, idx, l, r, A, B):
        if l == r:
            self.fA[idx] = A[l]
            self.fB[idx] = B[l]
            self.rA[idx] = A[l]
            self.rB[idx] = B[l]
            return
        m = (l + r) >> 1
        li = idx << 1
        self._build(li, l, m, A, B)
        self._build(li | 1, m + 1, r, A, B)
        self._pull(idx)

    def range_set(self, ql, qr, a, b):
        a %= MOD
        b %= MOD
        inv_am1 = 0 if a == 1 else pow((a - 1) % MOD, MOD - 2, MOD)
        self._range_set(1, 0, self.n - 1, ql, qr, a, b, inv_am1)

    def _range_set(self, idx, l, r, ql, qr, a, b, inv_am1):
        if ql <= l and r <= qr:
            self._apply_set(idx, l, r, a, b, inv_am1)
            return
        self._push(idx, l, r)
        m = (l + r) >> 1
        li = idx << 1
        if ql <= m:
            self._range_set(li, l, m, ql, qr, a, b, inv_am1)
        if qr > m:
            self._range_set(li | 1, m + 1, r, ql, qr, a, b, inv_am1)
        self._pull(idx)

    def range_query(self, ql, qr):
        return self._range_query(1, 0, self.n - 1, ql, qr)

    def _range_query(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.fA[idx], self.fB[idx], self.rA[idx], self.rB[idx]
        self._push(idx, l, r)
        m = (l + r) >> 1
        li = idx << 1
        if qr <= m:
            return self._range_query(li, l, m, ql, qr)
        if ql > m:
            return self._range_query(li | 1, m + 1, r, ql, qr)

        lfA, lfB, lbA, lbB = self._range_query(li, l, m, ql, qr)
        rfA, rfB, rbA, rbB = self._range_query(li | 1, m + 1, r, ql, qr)

        # merge forward: right o left
        fA = (rfA * lfA) % MOD
        fB = (rfA * lfB + rfB) % MOD

        # merge backward: left o right
        bA = (lbA * rbA) % MOD
        bB = (lbA * rbB + lbB) % MOD
        return fA, fB, bA, bB

class HLD:
    __slots__ = ("n", "adj", "parent", "depth", "size", "heavy", "head", "pos", "node_at")

    def __init__(self, n, adj, root=1):
        self.n = n
        self.adj = adj
        self.parent = [0] * (n + 1)
        self.depth = [0] * (n + 1)
        self.size = [0] * (n + 1)
        self.heavy = [0] * (n + 1)
        self.head = [0] * (n + 1)
        self.pos = [0] * (n + 1)
        self.node_at = [0] * n
        self._build(root)

    def _build(self, root):
        order = []
        st = [root]
        self.parent[root] = 0
        self.depth[root] = 0
        while st:
            v = st.pop()
            order.append(v)
            for to in self.adj[v]:
                if to == self.parent[v]:
                    continue
                self.parent[to] = v
                self.depth[to] = self.depth[v] + 1
                st.append(to)

        for v in reversed(order):
            sz = 1
            best = 0
            hv = 0
            for to in self.adj[v]:
                if to == self.parent[v]:
                    continue
                sz += self.size[to]
                if self.size[to] > best:
                    best = self.size[to]
                    hv = to
            self.size[v] = sz
            self.heavy[v] = hv

        cur = 0
        stack = [(root, root)]
        while stack:
            v, h = stack.pop()
            while v:
                self.head[v] = h
                self.pos[v] = cur
                self.node_at[cur] = v
                cur += 1
                hv = self.heavy[v]
                for to in self.adj[v]:
                    if to == self.parent[v] or to == hv:
                        continue
                    stack.append((to, to))
                v = hv

    def path_assign(self, seg, u, v, a, b):
        while self.head[u] != self.head[v]:
            if self.depth[self.head[u]] < self.depth[self.head[v]]:
                u, v = v, u
            hu = self.head[u]
            seg.range_set(self.pos[hu], self.pos[u], a, b)
            u = self.parent[hu]
        if self.depth[u] > self.depth[v]:
            u, v = v, u
        seg.range_set(self.pos[u], self.pos[v], a, b)

    def path_comp(self, seg, u, v):
        upA, upB = 1, 0
        down_ranges = []
        uu, vv = u, v

        while self.head[uu] != self.head[vv]:
            if self.depth[self.head[uu]] >= self.depth[self.head[vv]]:
                hu = self.head[uu]
                l = self.pos[hu]
                r = self.pos[uu]
                _, _, bA, bB = seg.range_query(l, r)
                upA = (bA * upA) % MOD
                upB = (bA * upB + bB) % MOD
                uu = self.parent[hu]
            else:
                hv = self.head[vv]
                down_ranges.append((self.pos[hv], self.pos[vv]))
                vv = self.parent[hv]

        if self.depth[uu] >= self.depth[vv]:
            l = self.pos[vv]
            r = self.pos[uu]
            _, _, bA, bB = seg.range_query(l, r)
            upA = (bA * upA) % MOD
            upB = (bA * upB + bB) % MOD
        else:
            down_ranges.append((self.pos[uu], self.pos[vv]))

        downA, downB = 1, 0
        for l, r in reversed(down_ranges):
            fA, fB, _, _ = seg.range_query(l, r)
            downA = (fA * downA) % MOD
            downB = (fA * downB + fB) % MOD

        # result = down o up
        A = (downA * upA) % MOD
        B = (downA * upB + downB) % MOD
        return A, B

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    a_node = [0] * (n + 1)
    b_node = [0] * (n + 1)
    for i in range(1, n + 1):
        a_node[i] = int(next(it)) % MOD
        b_node[i] = int(next(it)) % MOD

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    hld = HLD(n, adj, 1)

    base_a = [0] * n
    base_b = [0] * n
    for i in range(n):
        node = hld.node_at[i]
        base_a[i] = a_node[node]
        base_b[i] = b_node[node]

    seg = SegTree(base_a, base_b)

    q = int(next(it))
    out = []
    for _ in range(q):
        t = int(next(it))
        u = int(next(it))
        v = int(next(it))
        if t == 1:
            a = int(next(it))
            b = int(next(it))
            hld.path_assign(seg, u, v, a, b)
        else:
            x = int(next(it)) % MOD
            A, B = hld.path_comp(seg, u, v)
            out.append(str((A * x + B) % MOD))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
