#!/usr/bin/env python3
import sys

# -------- fast input (ints) --------
def ints():
    data = sys.stdin.buffer.read()
    n = len(data)
    i = 0
    while i < n:
        while i < n and data[i] <= 32:
            i += 1
        if i >= n:
            break
        v = 0
        while i < n and data[i] > 32:
            v = v * 10 + (data[i] - 48)
            i += 1
        yield v

def solve():
    it = ints()
    try:
        n = next(it)
    except StopIteration:
        return

    a = [0] * n
    for i in range(n):
        a[i] = next(it)

    # nextSmaller: first index j>i with a[j] < a[i], else n
    ns = [n] * n
    st = []
    for i in range(n):
        ai = a[i]
        while st and a[st[-1]] > ai:
            ns[st.pop()] = i
        st.append(i)

    # prevGreater: last index j<i with a[j] > a[i], else -1
    pg = [-1] * n
    st = []
    for i in range(n):
        ai = a[i]
        while st and a[st[-1]] < ai:
            st.pop()
        pg[i] = st[-1] if st else -1
        st.append(i)

    # Build expiration buckets using linked-list arrays (memory efficient for n=1e6)
    head = [-1] * (n + 1)   # head[t] = first l that expires at time t
    nxt  = [-1] * n
    for l in range(n):
        t = ns[l]
        nxt[l] = head[t]
        head[t] = l

    # Fenwick tree for active l positions (1-indexed)
    bit = [0] * (n + 1)

    def bit_add(i, delta):
        # i is 1..n
        while i <= n:
            bit[i] += delta
            i += i & -i

    def bit_sum(i):
        s = 0
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    ans = 0
    bit_add_local = bit_add
    bit_sum_local = bit_sum
    head_local = head
    nxt_local = nxt
    pg_local = pg

    for r in range(n):
        # expire l with ns[l] == r (they stop being valid when r reaches ns[l])
        x = head_local[r]
        while x != -1:
            bit_add_local(x + 1, -1)
            x = nxt_local[x]

        # activate l = r
        bit_add_local(r + 1, 1)

        # count active l in (pg[r], r] = [pg[r]+1 .. r]
        # using 1-indexed BIT: positions 1..n correspond to l=0..n-1
        left = pg_local[r] + 1  # l index lower bound
        ans += bit_sum_local(r + 1) - bit_sum_local(left)

    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()
