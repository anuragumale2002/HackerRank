import sys

MOD = 100711433

# ---------- Fast input ----------
def ints():
    data = sys.stdin.buffer.read().split()
    return list(map(int, data))

# ---------- Segment Tree supporting GP range add (ratio R) and (ratio invR) ----------
class SegTreeGP:
    __slots__ = ("n", "sum", "lazyF", "lazyB", "powR", "powInvR", "gpSumR", "gpSumInv")

    def __init__(self, n, powR, powInvR, gpSumR, gpSumInv):
        self.n = n
        size = 4 * n
        self.sum = [0] * size
        self.lazyF = [0] * size  # pending GP with ratio R, stored as start term at segment's L
        self.lazyB = [0] * size  # pending GP with ratio invR, stored as start term at segment's L
        self.powR = powR
        self.powInvR = powInvR
        self.gpSumR = gpSumR
        self.gpSumInv = gpSumInv

    def _applyF(self, idx, L, R, aL):
        # add aL * R^0 + ... across [L,R]
        length = R - L + 1
        self.sum[idx] = (self.sum[idx] + aL * self.gpSumR[length]) % MOD
        self.lazyF[idx] = (self.lazyF[idx] + aL) % MOD

    def _applyB(self, idx, L, R, aL):
        # add aL * invR^0 + ... across [L,R]
        length = R - L + 1
        self.sum[idx] = (self.sum[idx] + aL * self.gpSumInv[length]) % MOD
        self.lazyB[idx] = (self.lazyB[idx] + aL) % MOD

    def _push(self, idx, L, R):
        lf = self.lazyF[idx]
        lb = self.lazyB[idx]
        if lf == 0 and lb == 0:
            return
        if L == R:
            self.lazyF[idx] = 0
            self.lazyB[idx] = 0
            return
        mid = (L + R) >> 1
        left = idx << 1
        right = left | 1
        left_len = mid - L + 1

        if lf:
            # left child gets same start at L
            self._applyF(left, L, mid, lf)
            # right child start term = lf * R^(left_len)
            self._applyF(right, mid + 1, R, (lf * self.powR[left_len]) % MOD)

        if lb:
            self._applyB(left, L, mid, lb)
            self._applyB(right, mid + 1, R, (lb * self.powInvR[left_len]) % MOD)

        self.lazyF[idx] = 0
        self.lazyB[idx] = 0

    def update_forward(self, ql, qr, a_at_ql):
        # add GP with ratio R on [ql,qr], first term at ql is a_at_ql
        self._updateF(1, 0, self.n - 1, ql, qr, a_at_ql)

    def _updateF(self, idx, L, R, ql, qr, a_at_ql):
        if ql <= L and R <= qr:
            # start term at L is a_at_ql * R^(L-ql)
            start = (a_at_ql * self.powR[L - ql]) % MOD
            self._applyF(idx, L, R, start)
            return
        self._push(idx, L, R)
        mid = (L + R) >> 1
        if ql <= mid:
            self._updateF(idx << 1, L, mid, ql, qr, a_at_ql)
        if qr > mid:
            self._updateF((idx << 1) | 1, mid + 1, R, ql, qr, a_at_ql)
        self.sum[idx] = (self.sum[idx << 1] + self.sum[(idx << 1) | 1]) % MOD

    def update_backward(self, ql, qr, a_at_ql):
        # add GP with ratio invR on [ql,qr], first term at ql is a_at_ql
        self._updateB(1, 0, self.n - 1, ql, qr, a_at_ql)

    def _updateB(self, idx, L, R, ql, qr, a_at_ql):
        if ql <= L and R <= qr:
            start = (a_at_ql * self.powInvR[L - ql]) % MOD
            self._applyB(idx, L, R, start)
            return
        self._push(idx, L, R)
        mid = (L + R) >> 1
        if ql <= mid:
            self._updateB(idx << 1, L, mid, ql, qr, a_at_ql)
        if qr > mid:
            self._updateB((idx << 1) | 1, mid + 1, R, ql, qr, a_at_ql)
        self.sum[idx] = (self.sum[idx << 1] + self.sum[(idx << 1) | 1]) % MOD

    def query(self, ql, qr):
        return self._query(1, 0, self.n - 1, ql, qr)

    def _query(self, idx, L, R, ql, qr):
        if ql <= L and R <= qr:
            return self.sum[idx]
        self._push(idx, L, R)
        mid = (L + R) >> 1
        res = 0
        if ql <= mid:
            res += self._query(idx << 1, L, mid, ql, qr)
        if qr > mid:
            res += self._query((idx << 1) | 1, mid + 1, R, ql, qr)
        return res % MOD


# ---------- HLD + LCA ----------
def solve():
    arr = ints()
    it = iter(arr)
    n = next(it)
    R_input = next(it)
    Rm = R_input % MOD

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a = next(it); b = next(it)
        g[a].append(b)
        g[b].append(a)

    U = next(it); Q = next(it)

    # Root tree at 1, iterative DFS
    parent = [0] * (n + 1)
    depth = [0] * (n + 1)
    order = []
    stack = [1]
    parent[1] = 0
    depth[1] = 0
    while stack:
        v = stack.pop()
        order.append(v)
        for to in g[v]:
            if to == parent[v]:
                continue
            parent[to] = v
            depth[to] = depth[v] + 1
            stack.append(to)

    # binary lifting for LCA
    LOG = (n).bit_length()
    up = [[0] * (n + 1) for _ in range(LOG)]
    up[0] = parent[:]
    for k in range(1, LOG):
        upk = up[k]
        upkm1 = up[k - 1]
        for v in range(1, n + 1):
            upk[v] = upkm1[upkm1[v]]

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
        for k in range(LOG - 1, -1, -1):
            if up[k][a] != up[k][b]:
                a = up[k][a]
                b = up[k][b]
        return parent[a]

    # sizes + heavy child
    size = [1] * (n + 1)
    heavy = [0] * (n + 1)
    for v in reversed(order):
        maxsz = 0
        for to in g[v]:
            if to == parent[v]:
                continue
            size[v] += size[to]
            if size[to] > maxsz:
                maxsz = size[to]
                heavy[v] = to

    # decompose
    head = [0] * (n + 1)
    pos = [0] * (n + 1)
    invpos = [0] * n
    cur = 0
    st = [(1, 1)]  # (node, head)
    while st:
        v, h = st.pop()
        # walk down heavy path
        x = v
        while x:
            head[x] = h
            pos[x] = cur
            invpos[cur] = x
            cur += 1
            # push light children
            for to in g[x]:
                if to == parent[x] or to == heavy[x]:
                    continue
                st.append((to, to))
            x = heavy[x]

    # Special safe case: Rm == 0 means only the start node gets X (since next terms are 0)
    # (This avoids needing invR)
    if Rm == 0:
        # point updates, then answer path sums via segtree sums (simple range add point)
        # We'll still use a simple BIT over HLD positions for point updates + range sums.
        bit = [0] * (n + 2)

        def bit_add(i, val):
            i += 1
            while i <= n + 1:
                bit[i] = (bit[i] + val) % MOD
                i += i & -i

        def bit_sum(i):
            i += 1
            s = 0
            while i > 0:
                s += bit[i]
                i -= i & -i
            return s % MOD

        def range_sum(l, r):
            return (bit_sum(r) - (bit_sum(l - 1) if l > 0 else 0)) % MOD

        for _ in range(U):
            u = next(it); v = next(it); X = next(it)
            bit_add(pos[u], X % MOD)  # only u gets X

        out = []
        for _ in range(Q):
            a = next(it); b = next(it)
            res = 0
            while head[a] != head[b]:
                if depth[head[a]] < depth[head[b]]:
                    a, b = b, a
                res = (res + range_sum(pos[head[a]], pos[a])) % MOD
                a = parent[head[a]]
            if depth[a] > depth[b]:
                a, b = b, a
            res = (res + range_sum(pos[a], pos[b])) % MOD
            out.append(str(res))
        sys.stdout.write("\n".join(out))
        return

    # Precompute powers and GP prefix sums
    invR = pow(Rm, MOD - 2, MOD)  # MOD is prime in this challenge setting
    powR = [1] * (n + 2)
    powInvR = [1] * (n + 2)
    for i in range(1, n + 2):
        powR[i] = (powR[i - 1] * Rm) % MOD
        powInvR[i] = (powInvR[i - 1] * invR) % MOD

    inv_R_minus_1 = pow((Rm - 1) % MOD, MOD - 2, MOD)
    inv_invR_minus_1 = pow((invR - 1) % MOD, MOD - 2, MOD)

    gpSumR = [0] * (n + 2)      # sum_{t=0..len-1} R^t
    gpSumInv = [0] * (n + 2)    # sum_{t=0..len-1} invR^t
    for length in range(1, n + 2):
        gpSumR[length] = ((powR[length] - 1) % MOD) * inv_R_minus_1 % MOD
        gpSumInv[length] = ((powInvR[length] - 1) % MOD) * inv_invR_minus_1 % MOD

    seg = SegTreeGP(n, powR, powInvR, gpSumR, gpSumInv)

    # Update path with GP starting at u
    def path_update(u, v, X):
        l = lca(u, v)
        du_l = depth[u] - depth[l]

        # ---- Up part: u -> l (inclusive), in base order it's [l..u] with ratio invR
        uu = u
        while head[uu] != head[l]:
            h = head[uu]
            # update [h..uu] in base order (h is ancestor)
            # term at h = X * R^(depth[u] - depth[h])
            a_h = (X * powR[depth[u] - depth[h]]) % MOD
            seg.update_backward(pos[h], pos[uu], a_h)
            uu = parent[h]
        # final segment within same chain [l..uu]
        a_l = (X * powR[depth[u] - depth[l]]) % MOD
        seg.update_backward(pos[l], pos[uu], a_l)

        # ---- Down part: l -> v (exclude l), ratio R in base order
        if v == l:
            return
        segments = []
        vv = v
        while head[vv] != head[l]:
            segments.append((head[vv], vv))
            vv = parent[head[vv]]
        # now same chain as l
        if vv != l:
            top = invpos[pos[l] + 1]  # node just below l in this chain
            segments.append((top, vv))

        # process from near-l to v
        segments.reverse()
        for top, bottom in segments:
            dist_u_top = du_l + (depth[top] - depth[l])  # LCA(u, top) = l
            a_top = (X * powR[dist_u_top]) % MOD
            seg.update_forward(pos[top], pos[bottom], a_top)

    # Apply all updates
    for _ in range(U):
        u = next(it); v = next(it); X = next(it)
        path_update(u, v, X % MOD)

    # Answer queries (static path sums)
    out = []
    for _ in range(Q):
        a = next(it); b = next(it)
        res = 0
        while head[a] != head[b]:
            if depth[head[a]] < depth[head[b]]:
                a, b = b, a
            res = (res + seg.query(pos[head[a]], pos[a])) % MOD
            a = parent[head[a]]
        if depth[a] > depth[b]:
            a, b = b, a
        res = (res + seg.query(pos[a], pos[b])) % MOD
        out.append(str(res % MOD))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()
