# Enter your code here. Read input from STDIN. Print output to STDOUT
#!/usr/bin/env python3
import sys

MOD = 1_000_000_007

# ---------- fast input ----------
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
        if data[i] == 45:
            sign = -1
            i += 1
        v = 0
        while i < n and data[i] > 32:
            v = v * 10 + (data[i] - 48)
            i += 1
        yield sign * v

# ---------- iterative lazy segtree: range add (A*i + B), range sum ----------
class SegAffineSum:
    __slots__ = ("n", "size", "log", "sum", "lzA", "lzB", "sumIdx", "segLen")

    def __init__(self, n):
        self.n = n
        size = 1
        log = 0
        while size < n:
            size <<= 1
            log += 1
        self.size = size
        self.log = log

        # segment length and sum of indices per node
        self.segLen = [0] * (2 * size)
        self.sumIdx = [0] * (2 * size)

        # leaves
        for i in range(size):
            k = size + i
            if i < n:
                self.segLen[k] = 1
                self.sumIdx[k] = i  # index in base array
            else:
                self.segLen[k] = 0
                self.sumIdx[k] = 0

        # build internal
        for k in range(size - 1, 0, -1):
            self.segLen[k] = self.segLen[k << 1] + self.segLen[(k << 1) | 1]
            self.sumIdx[k] = self.sumIdx[k << 1] + self.sumIdx[(k << 1) | 1]

        self.sum = [0] * (2 * size)
        self.lzA = [0] * size
        self.lzB = [0] * size

    def _apply(self, k, A, B):
        # add (A*i + B) over this node's segment
        if self.segLen[k] == 0:
            return
        A %= MOD
        B %= MOD
        self.sum[k] = (self.sum[k] + A * (self.sumIdx[k] % MOD) + B * self.segLen[k]) % MOD
        if k < self.size:
            self.lzA[k] = (self.lzA[k] + A) % MOD
            self.lzB[k] = (self.lzB[k] + B) % MOD

    def _push(self, k):
        A = self.lzA[k]
        B = self.lzB[k]
        if (A | B) != 0:
            self._apply(k << 1, A, B)
            self._apply((k << 1) | 1, A, B)
            self.lzA[k] = 0
            self.lzB[k] = 0

    def _pull(self, k):
        self.sum[k] = (self.sum[k << 1] + self.sum[(k << 1) | 1]) % MOD

    def range_apply(self, l, r, A, B):
        # apply on [l, r) 0-indexed
        if l >= r:
            return
        size = self.size
        l += size
        r += size
        l0, r0 = l, r

        # push down along paths
        for i in range(self.log, 0, -1):
            if ((l0 >> i) << i) != l0:
                self._push(l0 >> i)
            if ((r0 >> i) << i) != r0:
                self._push((r0 - 1) >> i)

        while l < r:
            if l & 1:
                self._apply(l, A, B)
                l += 1
            if r & 1:
                r -= 1
                self._apply(r, A, B)
            l >>= 1
            r >>= 1

        # pull up
        for i in range(1, self.log + 1):
            if ((l0 >> i) << i) != l0:
                self._pull(l0 >> i)
            if ((r0 >> i) << i) != r0:
                self._pull((r0 - 1) >> i)

    def range_sum(self, l, r):
        # sum on [l, r) 0-indexed
        if l >= r:
            return 0
        size = self.size
        l += size
        r += size

        # push down along paths
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)

        resL = 0
        resR = 0
        while l < r:
            if l & 1:
                resL += self.sum[l]
                l += 1
            if r & 1:
                r -= 1
                resR += self.sum[r]
            l >>= 1
            r >>= 1
        return (resL + resR) % MOD

# ---------- HLD with ordered path segments ----------
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

    parent = [0] * n
    depth = [0] * n
    size = [0] * n
    heavy = [-1] * n

    # parent/depth/order
    parent[0] = -1
    order = [0]
    st = [0]
    while st:
        u = st.pop()
        for v in g[u]:
            if v == parent[u]:
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            st.append(v)
            order.append(v)

    # subtree sizes + heavy
    for u in reversed(order):
        s = 1
        best_sz = 0
        best_ch = -1
        for v in g[u]:
            if v == parent[u]:
                continue
            s += size[v]
            if size[v] > best_sz:
                best_sz = size[v]
                best_ch = v
        size[u] = s
        heavy[u] = best_ch

    head = [0] * n
    pos = [0] * n
    cur = 0

    stack = [(0, 0)]
    while stack:
        u, h = stack.pop()
        while u != -1:
            head[u] = h
            pos[u] = cur
            cur += 1
            hv = heavy[u]
            for v in g[u]:
                if v == parent[u] or v == hv:
                    continue
                stack.append((v, v))
            u = hv

    seg = SegAffineSum(n)

    def path_segments_ordered(u, v):
        # returns list of segments (lpos, rpos, dir)
        # dir = +1 means traverse increasing pos, dir = -1 decreasing pos
        up = []
        down = []
        while head[u] != head[v]:
            if depth[head[u]] >= depth[head[v]]:
                up.append((pos[head[u]], pos[u], -1))
                u = parent[head[u]]
            else:
                down.append((pos[head[v]], pos[v], +1))
                v = parent[head[v]]
        if depth[u] >= depth[v]:
            up.append((pos[v], pos[u], -1))
        else:
            down.append((pos[u], pos[v], +1))
        down.reverse()
        return up + down

    def update_path(u, v, x):
        x %= MOD
        if x < 0:
            x += MOD
        segs = path_segments_ordered(u, v)
        step = 1  # 1-based along path
        for l, r, d in segs:
            if l > r:
                l, r = r, l
            length = r - l + 1
            if d == 1:
                # value at position p: (step + (p-l)) * x = x*p + x*(step-l)
                A = x
                B = x * (step - l)
            else:
                # value at position p: (step + (r-p)) * x = (-x)*p + x*(step+r)
                A = -x
                B = x * (step + r)
            seg.range_apply(l, r + 1, A, B)
            step += length

    def query_path(u, v):
        res = 0
        while head[u] != head[v]:
            if depth[head[u]] < depth[head[v]]:
                u, v = v, u
            hu = head[u]
            res = (res + seg.range_sum(pos[hu], pos[u] + 1)) % MOD
            u = parent[hu]
        if depth[u] > depth[v]:
            u, v = v, u
        res = (res + seg.range_sum(pos[u], pos[v] + 1)) % MOD
        return res

    out = []
    for _ in range(q):
        t = next(it)
        if t == 1:
            u = next(it); v = next(it); x = next(it)
            update_path(u, v, x)
        else:
            u = next(it); v = next(it)
            out.append(str(query_path(u, v)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
