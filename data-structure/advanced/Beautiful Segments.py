import sys
sys.setrecursionlimit(1_000_000)

TYPE_EVENT = 0
TYPE_QUERY = 1

class BITRange:
    # Range add, prefix sum using 2 BITs, plus a running total for suffix queries.
    __slots__ = ("n", "b1", "b2", "total")
    def __init__(self, n):
        self.n = n
        self.b1 = [0] * (n + 2)
        self.b2 = [0] * (n + 2)
        self.total = 0

    def _add(self, bit, i, v):
        n = self.n
        while i <= n:
            bit[i] += v
            i += i & -i

    def range_add(self, l, r, v):
        if l > r:
            return
        self.total += v * (r - l + 1)
        b1 = self.b1
        b2 = self.b2
        n = self.n

        i = l
        while i <= n:
            b1[i] += v
            b2[i] += v * (l - 1)
            i += i & -i

        i = r + 1
        nv = -v
        while i <= n:
            b1[i] += nv
            b2[i] += nv * r
            i += i & -i

    def prefix_sum(self, i):
        if i <= 0:
            return 0
        b1 = self.b1
        b2 = self.b2
        s1 = 0
        s2 = 0
        x = i
        while x > 0:
            s1 += b1[x]
            s2 += b2[x]
            x -= x & -x
        return s1 * i - s2

    def suffix_sum(self, l):
        return self.total - self.prefix_sum(l - 1)


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    it = iter(data)
    n = next(it)
    q = next(it)
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = next(it)

    # Parallel arrays for items to reduce overhead
    typ = []
    Rv  = []
    val = []
    l1  = []
    l2  = []
    qid = []

    # Build events: <= 17 distinct ANDs per right endpoint (Ai < 2^17)
    prev = []
    for j in range(1, n + 1):
        x = a[j]
        cur = [(x, j)]
        for v, mn in prev:
            nv = v & x
            if nv == cur[-1][0]:
                cur[-1] = (nv, mn)
            else:
                cur.append((nv, mn))

        prev_l = j + 1
        for v, mn in cur:
            typ.append(TYPE_EVENT)
            Rv.append(j)
            val.append(v)
            l1.append(mn)
            l2.append(prev_l - 1)
            qid.append(-1)
            prev_l = mn
        prev = cur

    ans = [0] * q
    for qi in range(q):
        L = next(it)
        R = next(it)
        K = next(it)
        typ.append(TYPE_QUERY)
        Rv.append(R)
        val.append(K)
        l1.append(L)   # store L here
        l2.append(0)
        qid.append(qi)

    m = len(typ)

    # Sort by R once
    idx = list(range(m))
    idx.sort(key=lambda i: Rv[i])

    typ2 = [0] * m
    R2   = [0] * m
    val2 = [0] * m
    l12  = [0] * m
    l22  = [0] * m
    qid2 = [0] * m
    for k, i in enumerate(idx):
        typ2[k] = typ[i]
        R2[k]   = Rv[i]
        val2[k] = val[i]
        l12[k]  = l1[i]
        l22[k]  = l2[i]
        qid2[k] = qid[i]
    typ, Rv, val, l1, l2, qid = typ2, R2, val2, l12, l22, qid2

    # CDQ merge sort by val on ord_idx
    ord_idx = list(range(m))
    tmp = [0] * m
    bit = BITRange(n)

    def cdq(lo, hi):
        if lo >= hi:
            return
        mid = (lo + hi) >> 1
        cdq(lo, mid)
        cdq(mid + 1, hi)

        i = lo
        j = mid + 1
        k = lo

        applied_l1 = []
        applied_l2 = []

        while i <= mid and j <= hi:
            li = ord_idx[i]
            rj = ord_idx[j]
            if val[li] <= val[rj]:
                if typ[li] == TYPE_EVENT:
                    ll = l1[li]
                    rr = l2[li]
                    bit.range_add(ll, rr, 1)
                    applied_l1.append(ll)
                    applied_l2.append(rr)
                tmp[k] = li
                i += 1
            else:
                if typ[rj] == TYPE_QUERY:
                    ans[qid[rj]] += bit.suffix_sum(l1[rj])
                tmp[k] = rj
                j += 1
            k += 1

        while i <= mid:
            li = ord_idx[i]
            if typ[li] == TYPE_EVENT:
                ll = l1[li]
                rr = l2[li]
                bit.range_add(ll, rr, 1)
                applied_l1.append(ll)
                applied_l2.append(rr)
            tmp[k] = li
            i += 1
            k += 1

        while j <= hi:
            rj = ord_idx[j]
            if typ[rj] == TYPE_QUERY:
                ans[qid[rj]] += bit.suffix_sum(l1[rj])
            tmp[k] = rj
            j += 1
            k += 1

        # rollback
        for t in range(len(applied_l1)):
            bit.range_add(applied_l1[t], applied_l2[t], -1)

        ord_idx[lo:hi + 1] = tmp[lo:hi + 1]

    cdq(0, m - 1)

    sys.stdout.write("\n".join(map(str, ans)))

if __name__ == "__main__":
    solve()


# Code times out