# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
sys.setrecursionlimit(1_000_000)

NEG_INF = -10**30

class SegTree:
    __slots__ = ("n", "mx", "lz")

    def __init__(self, n):
        self.n = n
        size = 4 * n if n > 1 else 4
        self.mx = [0] * size
        self.lz = [0] * size

    def _push(self, idx):
        lazy = self.lz[idx]
        if lazy != 0:
            li = idx << 1
            ri = li | 1
            self.mx[li] += lazy
            self.lz[li] += lazy
            self.mx[ri] += lazy
            self.lz[ri] += lazy
            self.lz[idx] = 0

    def range_add(self, ql, qr, val):
        self._range_add(1, 0, self.n - 1, ql, qr, val)

    def _range_add(self, idx, l, r, ql, qr, val):
        if ql <= l and r <= qr:
            self.mx[idx] += val
            self.lz[idx] += val
            return
        self._push(idx)
        m = (l + r) >> 1
        li = idx << 1
        if ql <= m:
            self._range_add(li, l, m, ql, qr, val)
        if qr > m:
            self._range_add(li | 1, m + 1, r, ql, qr, val)
        self.mx[idx] = self.mx[li] if self.mx[li] >= self.mx[li | 1] else self.mx[li | 1]

    def range_max(self, ql, qr):
        return self._range_max(1, 0, self.n - 1, ql, qr)

    def _range_max(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.mx[idx]
        self._push(idx)
        m = (l + r) >> 1
        li = idx << 1
        res = NEG_INF
        if ql <= m:
            v = self._range_max(li, l, m, ql, qr)
            if v > res:
                res = v
        if qr > m:
            v = self._range_max(li | 1, m + 1, r, ql, qr)
            if v > res:
                res = v
        return res

class HLD:
    __slots__ = ("n", "adj", "parent", "depth", "size", "heavy", "head", "pos", "cur")

    def __init__(self, n, adj, root=1):
        self.n = n
        self.adj = adj
        self.parent = [0] * (n + 1)
        self.depth = [0] * (n + 1)
        self.size = [0] * (n + 1)
        self.heavy = [0] * (n + 1)
        self.head = [0] * (n + 1)
        self.pos = [0] * (n + 1)
        self.cur = 0
        self._build(root)

    def _build(self, root):
        # iterative dfs to get parent/depth/order
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

        # compute subtree sizes + heavy child
        for v in reversed(order):
            sz = 1
            best_sz = 0
            hv = 0
            for to in self.adj[v]:
                if to == self.parent[v]:
                    continue
                sz += self.size[to]
                if self.size[to] > best_sz:
                    best_sz = self.size[to]
                    hv = to
            self.size[v] = sz
            self.heavy[v] = hv

        # decompose: assign head and pos using heavy-first traversal
        self.cur = 0
        stack = [(root, root)]
        while stack:
            v, h = stack.pop()
            while v:
                self.head[v] = h
                self.pos[v] = self.cur
                self.cur += 1
                hv = self.heavy[v]
                for to in self.adj[v]:
                    if to == self.parent[v] or to == hv:
                        continue
                    stack.append((to, to))
                v = hv

    def path_max(self, seg, a, b):
        res = NEG_INF
        while self.head[a] != self.head[b]:
            if self.depth[self.head[a]] < self.depth[self.head[b]]:
                a, b = b, a
            ha = self.head[a]
            v = seg.range_max(self.pos[ha], self.pos[a])
            if v > res:
                res = v
            a = self.parent[ha]
        if self.depth[a] > self.depth[b]:
            a, b = b, a
        v = seg.range_max(self.pos[a], self.pos[b])
        if v > res:
            res = v
        return res

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it)); v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    hld = HLD(n, adj, 1)
    seg = SegTree(n)

    q = int(next(it))
    out = []
    for _ in range(q):
        typ = next(it)  # b'add' or b'max'
        if typ == b'add':
            t = int(next(it))
            x = int(next(it))
            l = hld.pos[t]
            r = l + hld.size[t] - 1
            seg.range_add(l, r, x)
        else:  # b'max'
            a = int(next(it))
            b = int(next(it))
            out.append(str(hld.path_max(seg, a, b)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
