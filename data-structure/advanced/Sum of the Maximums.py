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
        if data[i] == 45:
            sign = -1
            i += 1
        v = 0
        while i < n and data[i] > 32:
            v = v * 10 + (data[i] - 48)
            i += 1
        yield sign * v

def solve():
    it = ints()
    try:
        n = next(it)
    except StopIteration:
        return
    q = next(it)

    # 1-indexed
    a = [0] * (n + 1)
    for i in range(1, n + 1):
        a[i] = next(it)

    queries = []
    for qi in range(q):
        l = next(it)
        r = next(it)
        queries.append((r, l, qi))
    queries.sort()

    # ----- L[i], R[i] exactly like tester -----
    L = [0] * (n + 1)
    R = [0] * (n + 1)

    st = []
    for i in range(1, n + 1):
        ai = a[i]
        while st and ai > a[st[-1]]:
            st.pop()
        L[i] = 1 if not st else st[-1] + 1
        st.append(i)

    st = []
    for i in range(n, 0, -1):
        ai = a[i]
        while st and ai >= a[st[-1]]:
            st.pop()
        R[i] = n if not st else st[-1] - 1
        st.append(i)

    # ----- Events: one bucket per x for all 4 BITs -----
    # events_in[x]  : list of (k, l, r, val) to ADD when cur==x
    # events_out[x] : list of (k, l, r, val) to REMOVE when cur==x
    events_in = [None] * (n + 2)
    events_out = [None] * (n + 2)

    def push_event(arr, x, k, l_rng, r_rng, val):
        if l_rng > r_rng:
            return
        lst = arr[x]
        if lst is None:
            arr[x] = [(k, l_rng, r_rng, val)]
        else:
            lst.append((k, l_rng, r_rng, val))

    # helper like tester's (in at start_x, out at end_x)
    def add_event(k, start_x, end_x, l_rng, r_rng, val):
        if start_x > end_x or l_rng > r_rng:
            return
        push_event(events_in, start_x, k, l_rng, r_rng, val)
        push_event(events_out, end_x, k, l_rng, r_rng, val)

    # Build events exactly like tester
    for i in range(1, n + 1):
        Li = L[i]
        Ri = R[i]
        ai = a[i]

        # 1) x <= L[i], i <= y <= R[i]
        c2 = (i - Li + 1) * ai
        c3 = (i - Li + 1) * (-i + 1) * ai
        add_event(2, i, Ri, 1, Li, c2)
        add_event(3, i, Ri, 1, Li, c3)

        # 2) x <= L[i], y > R[i]
        c3b = (i - Li + 1) * (Ri - i + 1) * ai
        if Ri + 1 <= n:
            add_event(3, Ri + 1, n, 1, Li, c3b)

        # 3) L[i] < x <= i, i <= y <= R[i]
        c0 = -ai
        c1 = (i - 1) * ai
        c2b = (i + 1) * ai
        c3c = (i + 1) * (-i + 1) * ai
        add_event(0, i, Ri, Li + 1, i, c0)
        add_event(1, i, Ri, Li + 1, i, c1)
        add_event(2, i, Ri, Li + 1, i, c2b)
        add_event(3, i, Ri, Li + 1, i, c3c)

        # 4) L[i] < x <= i, y > R[i]
        c1b = -(Ri - i + 1) * ai
        c3d = (i + 1) * (Ri - i + 1) * ai
        if Ri + 1 <= n:
            add_event(1, Ri + 1, n, Li + 1, i, c1b)
            add_event(3, Ri + 1, n, Li + 1, i, c3d)

    # ----- 4 BITs range add / point query, fully inlined -----
    # 1-indexed BIT arrays of size n
    bit0 = [0] * (n + 2)
    bit1 = [0] * (n + 2)
    bit2 = [0] * (n + 2)
    bit3 = [0] * (n + 2)
    bits = (bit0, bit1, bit2, bit3)

    def bit_add(bit, idx, val):
        while idx <= n:
            bit[idx] += val
            idx += idx & -idx

    def bit_add_range(bit, l, r, val):
        if l > r:
            return
        bit_add(bit, l, val)
        bit_add(bit, r + 1, -val)

    def bit_get(bit, idx):
        s = 0
        while idx > 0:
            s += bit[idx]
            idx -= idx & -idx
        return s

    # Sweep r from 1..n (cur is current r processed)
    res = [0] * q
    cur = 0
    qi = 0
    for r, l, idx in queries:
        while cur < r:
            # remove events at cur
            if cur >= 1:
                outlst = events_out[cur]
                if outlst is not None:
                    for k, lo, hi, val in outlst:
                        bit_add_range(bits[k], lo, hi, -val)

            cur += 1

            inlst = events_in[cur]
            if inlst is not None:
                for k, lo, hi, val in inlst:
                    bit_add_range(bits[k], lo, hi, val)

        c0 = bit_get(bit0, l)
        c1 = bit_get(bit1, l)
        c2 = bit_get(bit2, l)
        c3 = bit_get(bit3, l)
        res[idx] = c0 * l * r + c1 * l + c2 * r + c3

    sys.stdout.write("\n".join(map(str, res)))

if __name__ == "__main__":
    solve()


# Run this in PyPy3 environment