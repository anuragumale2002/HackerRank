import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

MOD = 1_000_000_007

def modinv(a):
    return pow(a, MOD - 2, MOD)

# ---------- Segment Tree supporting adds of (p0+p1*i+p2*i^2)*q^i ----------
class SegTree:
    __slots__ = ("n", "sum", "lr0", "lr1", "lr2", "li0", "li1", "li2",
                 "S0R","S1R","S2R","S0I","S1I","S2I","powR","powI")
    def __init__(self, n, R):
        self.n = n
        size = 4 * n + 5
        self.sum = [0] * size

        # lazy for base q=R
        self.lr0 = [0] * size
        self.lr1 = [0] * size
        self.lr2 = [0] * size
        # lazy for base q=invR
        self.li0 = [0] * size
        self.li1 = [0] * size
        self.li2 = [0] * size

        invR = modinv(R)

        # precompute powers up to n (max segment length)
        self.powR = [1] * (n + 1)
        self.powI = [1] * (n + 1)
        for i in range(1, n + 1):
            self.powR[i] = (self.powR[i-1] * R) % MOD
            self.powI[i] = (self.powI[i-1] * invR) % MOD

        # precompute S0,S1,S2 for q=R and q=invR:
        # S0[len]=sum q^i, S1[len]=sum i q^i, S2[len]=sum i^2 q^i for i=0..len-1
        def build_S(powq):
            S0 = [0] * (n + 1)
            S1 = [0] * (n + 1)
            S2 = [0] * (n + 1)
            for i in range(n):
                qi = powq[i]
                S0[i+1] = (S0[i] + qi) % MOD
                S1[i+1] = (S1[i] + i * qi) % MOD
                S2[i+1] = (S2[i] + (i*i % MOD) * qi) % MOD
            return S0, S1, S2

        self.S0R, self.S1R, self.S2R = build_S(self.powR)
        self.S0I, self.S1I, self.S2I = build_S(self.powI)

    def _add_to_node(self, idx, p0, p1, p2, useR, length):
        # add sum of (p0+p1*i+p2*i^2)*q^i over i=0..length-1
        if useR:
            S0, S1, S2 = self.S0R, self.S1R, self.S2R
            self.lr0[idx] = (self.lr0[idx] + p0) % MOD
            self.lr1[idx] = (self.lr1[idx] + p1) % MOD
            self.lr2[idx] = (self.lr2[idx] + p2) % MOD
        else:
            S0, S1, S2 = self.S0I, self.S1I, self.S2I
            self.li0[idx] = (self.li0[idx] + p0) % MOD
            self.li1[idx] = (self.li1[idx] + p1) % MOD
            self.li2[idx] = (self.li2[idx] + p2) % MOD

        add = (p0 * S0[length] + p1 * S1[length] + p2 * S2[length]) % MOD
        self.sum[idx] = (self.sum[idx] + add) % MOD

    @staticmethod
    def _shift_poly(p0, p1, p2, off):
        # poly(i+off) = p0' + p1'*i + p2*i^2
        offm = off % MOD
        off2 = (offm * offm) % MOD
        np0 = (p0 + p1 * offm + p2 * off2) % MOD
        np1 = (p1 + (2 * p2 % MOD) * offm) % MOD
        return np0, np1, p2

    def _push(self, idx, l, r):
        if l == r:
            # clear lazies
            self.lr0[idx]=self.lr1[idx]=self.lr2[idx]=0
            self.li0[idx]=self.li1[idx]=self.li2[idx]=0
            return
        mid = (l + r) >> 1
        left_len = mid - l + 1
        right_len = r - mid

        # push q=R lazy
        p0, p1, p2 = self.lr0[idx], self.lr1[idx], self.lr2[idx]
        if p0 or p1 or p2:
            # left child: same
            self._add_to_node(idx<<1, p0, p1, p2, True, left_len)
            # right child: shift by left_len and multiply by R^left_len
            sp0, sp1, sp2 = self._shift_poly(p0, p1, p2, left_len)
            mul = self.powR[left_len]
            sp0 = sp0 * mul % MOD
            sp1 = sp1 * mul % MOD
            sp2 = sp2 * mul % MOD
            self._add_to_node(idx<<1|1, sp0, sp1, sp2, True, right_len)
            self.lr0[idx]=self.lr1[idx]=self.lr2[idx]=0

        # push q=invR lazy
        p0, p1, p2 = self.li0[idx], self.li1[idx], self.li2[idx]
        if p0 or p1 or p2:
            self._add_to_node(idx<<1, p0, p1, p2, False, left_len)
            sp0, sp1, sp2 = self._shift_poly(p0, p1, p2, left_len)
            mul = self.powI[left_len]
            sp0 = sp0 * mul % MOD
            sp1 = sp1 * mul % MOD
            sp2 = sp2 * mul % MOD
            self._add_to_node(idx<<1|1, sp0, sp1, sp2, False, right_len)
            self.li0[idx]=self.li1[idx]=self.li2[idx]=0

    def range_add_seq(self, q_is_R, L, R, p0, p1, p2):
        # add (p0+p1*i+p2*i^2)*q^i on interval positions L..R, where i counts from 0 at L
        def rec(idx, l, r):
            if R < l or r < L:
                return
            if L <= l and r <= R:
                # need to shift by (l-L) because local i starts at 0 for node segment
                off = l - L
                sp0, sp1, sp2 = self._shift_poly(p0, p1, p2, off)
                mul = (self.powR[off] if q_is_R else self.powI[off])
                sp0 = sp0 * mul % MOD
                sp1 = sp1 * mul % MOD
                sp2 = sp2 * mul % MOD
                self._add_to_node(idx, sp0, sp1, sp2, q_is_R, r - l + 1)
                return
            self._push(idx, l, r)
            mid = (l + r) >> 1
            rec(idx<<1, l, mid)
            rec(idx<<1|1, mid+1, r)
            self.sum[idx] = (self.sum[idx<<1] + self.sum[idx<<1|1]) % MOD
        rec(1, 1, self.n)

    def range_sum(self, L, R):
        def rec(idx, l, r):
            if R < l or r < L:
                return 0
            if L <= l and r <= R:
                return self.sum[idx]
            self._push(idx, l, r)
            mid = (l + r) >> 1
            return (rec(idx<<1, l, mid) + rec(idx<<1|1, mid+1, r)) % MOD
        return rec(1, 1, self.n)

# ---------- HLD ----------
def solve():
    N, Rbase = map(int, input().split())
    g = [[] for _ in range(N+1)]
    for _ in range(N-1):
        x, y = map(int, input().split())
        g[x].append(y)
        g[y].append(x)

    parent = [0]*(N+1)
    depth  = [0]*(N+1)
    heavy  = [0]*(N+1)
    size   = [0]*(N+1)

    # iterative DFS for parent/depth/order
    order = [1]
    parent[1] = 0
    depth[1] = 0
    st = [1]
    while st:
        u = st.pop()
        order.append(u)
        for v in g[u]:
            if v == parent[u]: 
                continue
            parent[v] = u
            depth[v] = depth[u] + 1
            st.append(v)

    # compute subtree sizes & heavy child
    for u in reversed(order[1:]):
        size[u] = 1
        mx = 0
        for v in g[u]:
            if v == parent[u]: 
                continue
            size[u] += size[v]
            if size[v] > mx:
                mx = size[v]
                heavy[u] = v

    head = [0]*(N+1)
    pos  = [0]*(N+1)
    inv  = [0]*(N+1)
    cur = 0

    # decompose
    stack = [(1, 1)]  # (u, h)
    while stack:
        u, h = stack.pop()
        # walk heavy path
        x = u
        while x:
            head[x] = h
            cur += 1
            pos[x] = cur
            inv[cur] = x
            # push light children
            for v in g[x]:
                if v == parent[x] or v == heavy[x]:
                    continue
                stack.append((v, v))
            x = heavy[x]

    # LCA with binary lifting
    LOG = (N).bit_length()
    up = [[0]*(N+1) for _ in range(LOG)]
    for i in range(1, N+1):
        up[0][i] = parent[i]
    for k in range(1, LOG):
        prev = up[k-1]
        curu = up[k]
        for i in range(1, N+1):
            curu[i] = prev[prev[i]]

    def lca(a, b):
        if depth[a] < depth[b]:
            a, b = b, a
        diff = depth[a] - depth[b]
        bit = 0
        while diff:
            if diff & 1:
                a = up[bit][a]
            diff >>= 1
            bit += 1
        if a == b:
            return a
        for k in range(LOG-1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        return parent[a]

    seg = SegTree(N, Rbase)
    invR = modinv(Rbase)

    U, Q = map(int, input().split())

    updates = [tuple(map(int, input().split())) for _ in range(U)]
    queries = [tuple(map(int, input().split())) for _ in range(Q)]

    # quadratic in z:
    # (a1+z d1)(a2+z d2) = c0 + c1 z + c2 z^2
    # c2=d1*d2, c1=a1*d2+a2*d1, c0=a1*a2

    def apply_segment(q_is_R, Lpos, Rpos, d0, c0, c1, c2):
        # We need value at step i:
        # z = d0 + i (if q_is_R) OR z = d0 - i (if q_is_inv)
        # value = (c0 + c1 z + c2 z^2) * R^z
        # factor R^d0 and represent as (p0+p1*i+p2*i^2)*q^i
        d0m = d0 % MOD
        d02 = d0m * d0m % MOD

        base = pow(Rbase, d0, MOD)

        if q_is_R:
            # z=d0+i
            P2 = c2 % MOD
            P1 = (c1 + 2*c2*d0m) % MOD
            P0 = (c0 + c1*d0m + c2*d02) % MOD
            # multiply by R^d0
            p0 = P0 * base % MOD
            p1 = P1 * base % MOD
            p2 = P2 * base % MOD
            seg.range_add_seq(True, Lpos, Rpos, p0, p1, p2)
        else:
            # z=d0-i, exponent R^{d0}*(invR)^i
            P2 = c2 % MOD
            P1 = (-c1 - 2*c2*d0m) % MOD
            P0 = (c0 + c1*d0m + c2*d02) % MOD
            p0 = P0 * base % MOD
            p1 = P1 * base % MOD
            p2 = P2 * base % MOD
            seg.range_add_seq(False, Lpos, Rpos, p0, p1, p2)

    def path_update(A, B, a1, d1, a2, d2):
        A0 = a1 % MOD; D1 = d1 % MOD
        A2 = a2 % MOD; D2 = d2 % MOD
        c2 = D1 * D2 % MOD
        c1 = (A0 * D2 + A2 * D1) % MOD
        c0 = A0 * A2 % MOD

        L = lca(A, B)
        distAL = depth[A] - depth[L]

        # ---- A -> L part (includes L): z = depth[A]-depth[x] (decreasing along depth)
        u = A
        while head[u] != head[L]:
            h = head[u]
            Lpos = pos[h]
            Rpos = pos[u]
            d0 = depth[A] - depth[h]  # z at node h (left)
            apply_segment(False, Lpos, Rpos, d0, c0, c1, c2)  # base invR
            u = parent[h]
        # same head
        Lpos = pos[L]
        Rpos = pos[u]
        d0 = depth[A] - depth[L]
        apply_segment(False, Lpos, Rpos, d0, c0, c1, c2)

        # ---- L -> B part (exclude L): z = distAL + (depth[x]-depth[L]) increasing
        v = B
        segs = []
        while head[v] != head[L]:
            h = head[v]
            segs.append((pos[h], pos[v]))  # top->bottom in dfn
            v = parent[h]
        # same head: from L+1 to v if exists
        if v != L:
            segs.append((pos[L] + 1, pos[v]))

        # each segment is top->bottom increasing
        for lpos, rpos in segs:
            topnode = inv[lpos]
            d0 = distAL + (depth[topnode] - depth[L])
            apply_segment(True, lpos, rpos, d0, c0, c1, c2)

    def path_sum(u, v):
        res = 0
        while head[u] != head[v]:
            if depth[head[u]] < depth[head[v]]:
                u, v = v, u
            res = (res + seg.range_sum(pos[head[u]], pos[u])) % MOD
            u = parent[head[u]]
        if depth[u] > depth[v]:
            u, v = v, u
        res = (res + seg.range_sum(pos[u], pos[v])) % MOD
        return res

    # apply all updates
    for a1, d1, a2, d2, A, B in updates:
        path_update(A, B, a1, d1, a2, d2)

    # answer queries
    out = []
    for i, j in queries:
        out.append(str(path_sum(i, j) % MOD))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()


# timesout