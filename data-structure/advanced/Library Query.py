# Enter your code here. Read input from STDIN. Print output to STDOUT
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

# Fenwick over blocks (1-indexed)
def bit_add(bit, idx, delta):
    n = len(bit) - 1
    while idx <= n:
        bit[idx] += delta
        idx += idx & -idx

def bit_sum(bit, idx):
    s = 0
    while idx > 0:
        s += bit[idx]
        idx -= idx & -idx
    return s

def bit_range_sum(bit, l, r):
    # 1-indexed inclusive
    if l > r:
        return 0
    return bit_sum(bit, r) - bit_sum(bit, l - 1)

def solve():
    it = ints()
    try:
        T = next(it)
    except StopIteration:
        return

    out = []
    MAXV = 1000

    for _ in range(T):
        n = next(it)
        a = [0] * n
        for i in range(n):
            a[i] = next(it)

        q = next(it)

        # block setup
        B = 100  # good for n<=1e4
        nb = (n + B - 1) // B  # number of blocks

        # bits[v] is Fenwick over blocks storing count of value v in each block
        # size nb, 1-indexed => length nb+1
        bits = [None] * (MAXV + 1)
        for v in range(1, MAXV + 1):
            bits[v] = [0] * (nb + 1)

        # build
        for i, val in enumerate(a):
            b = i // B + 1
            bit_add(bits[val], b, 1)

        # temp array for edge counts
        edge_cnt = [0] * (MAXV + 1)

        for _qq in range(q):
            typ = next(it)
            if typ == 1:
                x = next(it) - 1
                k = next(it)
                old = a[x]
                if old != k:
                    b = x // B + 1
                    bit_add(bits[old], b, -1)
                    bit_add(bits[k], b, +1)
                    a[x] = k
            else:
                x = next(it) - 1
                y = next(it) - 1
                k = next(it)

                l = x
                r = y

                bl = l // B
                br = r // B

                # clear edge_cnt only for touched values (track touched)
                touched = []

                def inc(val):
                    if edge_cnt[val] == 0:
                        touched.append(val)
                    edge_cnt[val] += 1

                if bl == br:
                    # all inside one block: just scan
                    for i in range(l, r + 1):
                        inc(a[i])
                    # find kth
                    s = 0
                    ans = 1
                    for v in range(1, MAXV + 1):
                        c = edge_cnt[v]
                        if c:
                            s += c
                            if s >= k:
                                ans = v
                                break
                    out.append(str(ans))
                else:
                    # left edge
                    endL = (bl + 1) * B - 1
                    for i in range(l, endL + 1):
                        inc(a[i])

                    # right edge
                    startR = br * B
                    for i in range(startR, r + 1):
                        inc(a[i])

                    # full blocks strictly between
                    fullL = bl + 2      # block index in Fenwick (1-indexed)
                    fullR = br          # br block in 0-index => in Fenwick is br+1, but fullR is br-1 => (br)
                    # Explanation:
                    # blocks: 0..nb-1, fenwick uses 1..nb
                    # full blocks are (bl+1) .. (br-1)
                    # fenwick indices: (bl+1)+1 .. (br-1)+1 => bl+2 .. br
                    have_full = (fullL <= fullR)

                    s = 0
                    ans = 1
                    for v in range(1, MAXV + 1):
                        c = edge_cnt[v]
                        if have_full:
                            c += bit_range_sum(bits[v], fullL, fullR)
                        if c:
                            s += c
                            if s >= k:
                                ans = v
                                break
                    out.append(str(ans))

                # reset touched edge counts
                for v in touched:
                    edge_cnt[v] = 0

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
