# Enter your code here. Read input from STDIN. Print output to STDOUT
#!/usr/bin/env python3
import sys

MOD = 1000003

# -------- Segment Tree with lazy range-add on p_i ----------
class SegTree:
    __slots__ = ("n", "sumP", "prodPow", "prodD", "lazy")

    def __init__(self, d, p):
        self.n = len(d)
        size = 4 * self.n
        self.sumP = [0] * size          # big int (Python int)
        self.prodPow = [1] * size       # mod MOD
        self.prodD = [1] * size         # mod MOD (static)
        self.lazy = [0] * size          # pending add to p_i
        self._build(1, 0, self.n - 1, d, p)

    def _build(self, idx, l, r, d, p):
        if l == r:
            di = d[l] % MOD
            pi = p[l]
            self.sumP[idx] = pi
            self.prodD[idx] = di
            self.prodPow[idx] = pow(di, pi, MOD)  # handles pi=0 too
            return
        mid = (l + r) // 2
        self._build(idx * 2, l, mid, d, p)
        self._build(idx * 2 + 1, mid + 1, r, d, p)
        self._pull(idx)

    def _pull(self, idx):
        lc, rc = idx * 2, idx * 2 + 1
        self.sumP[idx] = self.sumP[lc] + self.sumP[rc]
        self.prodD[idx] = (self.prodD[lc] * self.prodD[rc]) % MOD
        self.prodPow[idx] = (self.prodPow[lc] * self.prodPow[rc]) % MOD

    def _apply_add(self, idx, l, r, addv):
        if addv == 0:
            return
        length = r - l + 1
        self.sumP[idx] += addv * length
        # multiply by (prodD^addv)
        self.prodPow[idx] = (self.prodPow[idx] * pow(self.prodD[idx], addv, MOD)) % MOD
        self.lazy[idx] += addv

    def _push(self, idx, l, r):
        addv = self.lazy[idx]
        if addv == 0 or l == r:
            return
        mid = (l + r) // 2
        self._apply_add(idx * 2, l, mid, addv)
        self._apply_add(idx * 2 + 1, mid + 1, r, addv)
        self.lazy[idx] = 0

    def range_add(self, ql, qr, addv):
        self._range_add(1, 0, self.n - 1, ql, qr, addv)

    def _range_add(self, idx, l, r, ql, qr, addv):
        if ql <= l and r <= qr:
            self._apply_add(idx, l, r, addv)
            return
        self._push(idx, l, r)
        mid = (l + r) // 2
        if ql <= mid:
            self._range_add(idx * 2, l, mid, ql, qr, addv)
        if qr > mid:
            self._range_add(idx * 2 + 1, mid + 1, r, ql, qr, addv)
        self._pull(idx)

    def range_query(self, ql, qr):
        return self._range_query(1, 0, self.n - 1, ql, qr)

    def _range_query(self, idx, l, r, ql, qr):
        if ql <= l and r <= qr:
            return self.sumP[idx], self.prodPow[idx]
        self._push(idx, l, r)
        mid = (l + r) // 2
        if qr <= mid:
            return self._range_query(idx * 2, l, mid, ql, qr)
        if ql > mid:
            return self._range_query(idx * 2 + 1, mid + 1, r, ql, qr)
        s1, p1 = self._range_query(idx * 2, l, mid, ql, qr)
        s2, p2 = self._range_query(idx * 2 + 1, mid + 1, r, ql, qr)
        return s1 + s2, (p1 * p2) % MOD


def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)

    n = int(next(it))
    d = [0] * n
    p = [0] * n

    # input lines: a_i d_i p_i  (a_i not needed for the answer)
    for i in range(n):
        _ai = int(next(it))
        di = int(next(it))
        pi = int(next(it))
        d[i] = di
        p[i] = pi

    # factorials mod MOD up to MOD-1
    fact = [1] * MOD
    for i in range(1, MOD):
        fact[i] = (fact[i - 1] * i) % MOD

    st = SegTree(d, p)

    q = int(next(it))
    out = []

    for _ in range(q):
        typ = int(next(it))
        l = int(next(it)) - 1
        r = int(next(it)) - 1
        if typ == 0:
            K, prodPow = st.range_query(l, r)
            if K >= MOD:
                const = 0
            else:
                const = (prodPow * fact[K]) % MOD
            out.append(f"{K} {const}")
        else:
            v = int(next(it))
            st.range_add(l, r, v)

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
