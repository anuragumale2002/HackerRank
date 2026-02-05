import sys

# ---------------- Fast int reader ----------------
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
        num = 0
        while i < n and data[i] > 32:
            num = num * 10 + (data[i] - 48)
            i += 1
        yield sign * num

INF = 10**30

# ---------------- Segment Tree ----------------
class SegTree:
    __slots__ = ("n", "size", "sumv", "minv", "maxv", "add", "has_set", "setv")

    def __init__(self, arr):
        n = len(arr)
        size = 1
        while size < n:
            size <<= 1
        self.n = n
        self.size = size
        m = 2 * size

        sumv = [0] * m
        minv = [INF] * m
        maxv = [-INF] * m

        # lazy
        add = [0] * m
        has_set = [0] * m   # 0/1 faster than bool list
        setv = [0] * m

        base = size
        for i, v in enumerate(arr):
            idx = base + i
            sumv[idx] = v
            minv[idx] = v
            maxv[idx] = v

        # padding leaves: keep min=INF max=-INF so they don't affect
        for i in range(base - 1, 0, -1):
            lc = i << 1
            rc = lc | 1
            sumv[i] = sumv[lc] + sumv[rc]
            a = minv[lc]; b = minv[rc]
            minv[i] = a if a < b else b
            a = maxv[lc]; b = maxv[rc]
            maxv[i] = a if a > b else b

        self.sumv = sumv
        self.minv = minv
        self.maxv = maxv
        self.add = add
        self.has_set = has_set
        self.setv = setv

    # apply set to node
    @staticmethod
    def _apply_set(idx, val, length, sumv, minv, maxv, add, has_set, setv):
        has_set[idx] = 1
        setv[idx] = val
        add[idx] = 0
        sumv[idx] = val * length
        minv[idx] = val
        maxv[idx] = val

    # apply add to node
    @staticmethod
    def _apply_add(idx, val, length, sumv, minv, maxv, add, has_set, setv):
        if has_set[idx]:
            setv[idx] += val
        else:
            add[idx] += val
        sumv[idx] += val * length
        minv[idx] += val
        maxv[idx] += val

    # push tags down
    @staticmethod
    def _push(idx, left_len, right_len, sumv, minv, maxv, add, has_set, setv):
        if has_set[idx]:
            v = setv[idx]
            lc = idx << 1
            rc = lc | 1
            SegTree._apply_set(lc, v, left_len,  sumv, minv, maxv, add, has_set, setv)
            SegTree._apply_set(rc, v, right_len, sumv, minv, maxv, add, has_set, setv)
            has_set[idx] = 0

        av = add[idx]
        if av:
            lc = idx << 1
            rc = lc | 1
            SegTree._apply_add(lc, av, left_len,  sumv, minv, maxv, add, has_set, setv)
            SegTree._apply_add(rc, av, right_len, sumv, minv, maxv, add, has_set, setv)
            add[idx] = 0

    # pull up after children updated
    @staticmethod
    def _pull(idx, sumv, minv, maxv):
        lc = idx << 1
        rc = lc | 1
        sumv[idx] = sumv[lc] + sumv[rc]
        a = minv[lc]; b = minv[rc]
        minv[idx] = a if a < b else b
        a = maxv[lc]; b = maxv[rc]
        maxv[idx] = a if a > b else b

    # ------- range add (recursive but fast) -------
    def range_add(self, L, R, c):
        size = self.size
        sumv = self.sumv; minv = self.minv; maxv = self.maxv
        add = self.add; has_set = self.has_set; setv = self.setv

        def rec(idx, s, e):
            if R < s or e < L:
                return
            if L <= s and e <= R:
                SegTree._apply_add(idx, c, e - s + 1, sumv, minv, maxv, add, has_set, setv)
                return
            mid = (s + e) >> 1
            SegTree._push(idx, mid - s + 1, e - mid, sumv, minv, maxv, add, has_set, setv)
            rec(idx << 1, s, mid)
            rec(idx << 1 | 1, mid + 1, e)
            SegTree._pull(idx, sumv, minv, maxv)

        rec(1, 0, size - 1)

    # ------- range div (ITERATIVE stack: big speedup) -------
    def range_div(self, L, R, d):
        if d == 1:
            return
        size = self.size
        n = self.n
        sumv = self.sumv; minv = self.minv; maxv = self.maxv
        add = self.add; has_set = self.has_set; setv = self.setv

        stack = [(1, 0, size - 1, 0)]  # (idx,s,e,state) state 0=go down, 1=pull
        while stack:
            idx, s, e, st = stack.pop()
            if R < s or e < L:
                continue

            if st == 1:
                SegTree._pull(idx, sumv, minv, maxv)
                continue

            mn = minv[idx]
            if mn == INF:
                continue
            mx = maxv[idx]

            # fully covered -> try prune
            if L <= s and e <= R:
                if mn == mx:
                    q = mn // d
                    SegTree._apply_set(idx, q, e - s + 1, sumv, minv, maxv, add, has_set, setv)
                    continue
                qmn = mn // d
                qmx = mx // d
                if qmn == qmx:
                    SegTree._apply_set(idx, qmn, e - s + 1, sumv, minv, maxv, add, has_set, setv)
                    continue

            if s == e:
                if s < n:
                    v = sumv[idx] // d
                    sumv[idx] = v
                    minv[idx] = v
                    maxv[idx] = v
                continue

            mid = (s + e) >> 1
            SegTree._push(idx, mid - s + 1, e - mid, sumv, minv, maxv, add, has_set, setv)

            # post-order pull
            stack.append((idx, s, e, 1))
            stack.append((idx << 1 | 1, mid + 1, e, 0))
            stack.append((idx << 1, s, mid, 0))

    # ------- queries (recursive; cheap) -------
    def range_min(self, L, R):
        size = self.size
        sumv = self.sumv; minv = self.minv; maxv = self.maxv
        add = self.add; has_set = self.has_set; setv = self.setv

        def rec(idx, s, e):
            if R < s or e < L:
                return INF
            if L <= s and e <= R:
                return minv[idx]
            mid = (s + e) >> 1
            SegTree._push(idx, mid - s + 1, e - mid, sumv, minv, maxv, add, has_set, setv)
            a = rec(idx << 1, s, mid)
            b = rec(idx << 1 | 1, mid + 1, e)
            return a if a < b else b

        return rec(1, 0, size - 1)

    def range_sum(self, L, R):
        size = self.size
        sumv = self.sumv; minv = self.minv; maxv = self.maxv
        add = self.add; has_set = self.has_set; setv = self.setv

        def rec(idx, s, e):
            if R < s or e < L:
                return 0
            if L <= s and e <= R:
                return sumv[idx]
            mid = (s + e) >> 1
            SegTree._push(idx, mid - s + 1, e - mid, sumv, minv, maxv, add, has_set, setv)
            return rec(idx << 1, s, mid) + rec(idx << 1 | 1, mid + 1, e)

        return rec(1, 0, size - 1)


def main():
    it = ints()
    n = next(it); q = next(it)
    arr = [next(it) for _ in range(n)]
    st = SegTree(arr)

    out = []
    for _ in range(q):
        t = next(it)
        l = next(it); r = next(it)
        if t == 1:
            c = next(it)
            st.range_add(l, r, c)
        elif t == 2:
            d = next(it)
            st.range_div(l, r, d)
        elif t == 3:
            out.append(str(st.range_min(l, r)))
        else:
            out.append(str(st.range_sum(l, r)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()


# Time limit exceeds