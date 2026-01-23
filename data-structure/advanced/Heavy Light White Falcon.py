#!/usr/bin/env python3
import sys

# ---------- Fast input ----------
def ints():
    data = sys.stdin.buffer.read()
    n = len(data)
    i = 0
    while i < n:
        while i < n and data[i] <= 32:
            i += 1
        if i >= n:
            break
        sign = 1
        if data[i] == 45:  # '-'
            sign = -1
            i += 1
        v = 0
        while i < n and data[i] > 32:
            v = v * 10 + (data[i] - 48)
            i += 1
        yield sign * v

# ---------- Iterative segment tree for max ----------
class SegMax:
    __slots__ = ("n", "size", "seg")
    def __init__(self, n):
        self.n = n
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.seg = [0] * (2 * size)

    def set_point(self, idx, val):
        i = idx + self.size
        self.seg[i] = val
        i >>= 1
        while i:
            left = self.seg[i << 1]
            right = self.seg[(i << 1) | 1]
            self.seg[i] = left if left >= right else right
            i >>= 1

    def range_max(self, l, r):
        # max on [l, r)
        res = -10**30
        l += self.size
        r += self.size
        seg = self.seg
        while l < r:
            if l & 1:
                if seg[l] > res: res = seg[l]
                l += 1
            if r & 1:
                r -= 1
                if seg[r] > res: res = seg[r]
            l >>= 1
            r >>= 1
        return res

def solve():
    it = ints()
    try:
        n = next(it); q = next(it)
    except StopIteration:
        return

    g = [[] for _ in range(n)]
    for _ in range(n - 1):
        u = next(it); v = next(it)
        g[u].append(v)
        g[v].append(u)

    parent = [-1] * n
    depth = [0] * n
    heavy = [-1] * n
    size = [0] * n

    # ----- 1) parent/depth/order via iterative DFS -----
    order = []
    stack = [0]
    parent[0] = 0
    while stack:
        u = stack.pop()
        order.append(u)
        for v in g[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            stack.append(v)

    # ----- 2) subtree sizes + heavy child (postorder) -----
    for u in reversed(order):
        s = 1
        best_sz = 0
        best_child = -1
        for v in g[u]:
            if v == parent[u]:
                continue
            s += size[v]
            if size[v] > best_sz:
                best_sz = size[v]
                best_child = v
        size[u] = s
        heavy[u] = best_child

    # ----- 3) decompose into heads + positions -----
    head = [0] * n
    pos = [0] * n
    cur = 0

    stack = [(0, 0, 0)]  # (u, head_u, state) state 0=enter
    # We'll do an iterative "walk heavy first" decomposition:
    while stack:
        u, h, _ = stack.pop()
        # walk down heavy path starting at u
        while True:
            head[u] = h
            pos[u] = cur
            cur += 1

            # push light children to process later (each starts a new head)
            hv = heavy[u]
            for v in g[u]:
                if v == parent[u] or v == hv:
                    continue
                stack.append((v, v, 0))

            if hv == -1:
                break
            u = hv

    seg = SegMax(n)  # values start at 0

    def path_max(a, b):
        res = -10**30
        while head[a] != head[b]:
            if depth[head[a]] < depth[head[b]]:
                a, b = b, a
            ha = head[a]
            # segment [pos[ha], pos[a]] inclusive => [pos[ha], pos[a]+1)
            val = seg.range_max(pos[ha], pos[a] + 1)
            if val > res: res = val
            a = parent[ha]
        # same head
        if depth[a] > depth[b]:
            a, b = b, a
        val = seg.range_max(pos[a], pos[b] + 1)
        if val > res: res = val
        return res

    out = []
    for _ in range(q):
        typ = next(it)
        if typ == 1:
            u = next(it); x = next(it)
            seg.set_point(pos[u], x)
        else:
            u = next(it); v = next(it)
            out.append(str(path_max(u, v)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
