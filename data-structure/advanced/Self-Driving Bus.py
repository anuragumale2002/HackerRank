import sys
sys.setrecursionlimit(1_000_000)

class SegTree:
    __slots__ = ("n", "maxv", "cnt", "lazy")

    def __init__(self, n: int):
        self.n = n
        size = 4 * n
        self.maxv = [0] * size   # maximum value in segment
        self.cnt  = [0] * size   # how many positions achieve that maximum
        self.lazy = [0] * size   # lazy add

        # Build with initial array all zeros: max=0 everywhere, count = segment length
        self._build(1, 1, n)

    def _build(self, idx: int, l: int, r: int):
        if l == r:
            self.maxv[idx] = 0
            self.cnt[idx] = 1
            return
        mid = (l + r) >> 1
        self._build(idx << 1, l, mid)
        self._build(idx << 1 | 1, mid + 1, r)
        self._pull(idx)

    def _apply(self, idx: int, add: int):
        self.maxv[idx] += add
        self.lazy[idx] += add

    def _push(self, idx: int):
        add = self.lazy[idx]
        if add:
            li = idx << 1
            ri = li | 1
            self._apply(li, add)
            self._apply(ri, add)
            self.lazy[idx] = 0

    def _pull(self, idx: int):
        li = idx << 1
        ri = li | 1
        if self.maxv[li] > self.maxv[ri]:
            self.maxv[idx] = self.maxv[li]
            self.cnt[idx] = self.cnt[li]
        elif self.maxv[li] < self.maxv[ri]:
            self.maxv[idx] = self.maxv[ri]
            self.cnt[idx] = self.cnt[ri]
        else:
            self.maxv[idx] = self.maxv[li]
            self.cnt[idx] = self.cnt[li] + self.cnt[ri]

    def add_range(self, ql: int, qr: int, val: int):
        if ql > qr:
            return
        self._add_range(1, 1, self.n, ql, qr, val)

    def _add_range(self, idx: int, l: int, r: int, ql: int, qr: int, val: int):
        if ql == l and qr == r:
            self._apply(idx, val)
            return
        self._push(idx)
        mid = (l + r) >> 1
        if qr <= mid:
            self._add_range(idx << 1, l, mid, ql, qr, val)
        elif ql > mid:
            self._add_range(idx << 1 | 1, mid + 1, r, ql, qr, val)
        else:
            self._add_range(idx << 1, l, mid, ql, mid, val)
            self._add_range(idx << 1 | 1, mid + 1, r, mid + 1, qr, val)
        self._pull(idx)

    @property
    def global_max(self):
        return self.maxv[1]

    @property
    def global_max_count(self):
        return self.cnt[1]


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    n = int(next(it))

    # edges grouped by their max endpoint b (after ensuring a < b)
    edges_by_b = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it)); v = int(next(it))
        if u > v:
            u, v = v, u
        edges_by_b[v].append(u)

    st = SegTree(n)
    ans = 0

    # process r from 1..n (this matches nodes[i].nn in the C code)
    for r in range(1, n + 1):
        # activate all edges with b == r: update [1..a] by +1
        for a in edges_by_b[r]:
            st.add_range(1, a, 1)

        # "Adds the current vertex": point update at r by +r
        st.add_range(r, r, r)

        # if current maximum equals r, add how many positions achieve it
        if st.global_max == r:
            ans += st.global_max_count

    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()
