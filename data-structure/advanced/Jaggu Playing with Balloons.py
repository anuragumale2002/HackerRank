import sys
from array import array

input = sys.stdin.readline
N = 1_000_000

# -------- Fenwick Tree (BIT) using array('q') --------
class Fenwick:
    __slots__ = ("n", "bit")
    def __init__(self, n):
        self.n = n
        self.bit = array('q', [0]) * (n + 1)

    def add(self, i, delta):
        bit = self.bit
        n = self.n
        while i <= n:
            bit[i] += delta
            i += i & -i

    def sum(self, i):
        s = 0
        bit = self.bit
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s

    def range_sum(self, l, r):
        return self.sum(r) - self.sum(l - 1)

# -------- one "j-iteration": compute all buckets visited until exceeding N --------
# This is the exact effect of the given pseudocode, but without the slow k-loop.
# It repeatedly adds the lowest set bit, which performs the same carry-reduction behavior.
def visited_in_one_j(pos):
    adds = [pos]
    p = pos
    while True:
        p += (p & -p)          # add lowest set bit
        if p > N:
            break
        adds.append(p)
    return adds

def solve():
    Q = int(input().strip())

    # next power of two strictly greater than N (N=1e6 => 2^20)
    P = 1
    while P <= N:
        P <<= 1

    FIXED = P - N  # 48576 when N=1e6

    FIXED_ADDS = visited_in_one_j(FIXED)

    bit = Fenwick(N)

    # per-update accumulator without dict (fast + memory safe)
    delta = array('q', [0]) * (N + 1)
    vis = array('I', [0]) * (N + 1)
    stamp = 0

    out = []

    for _ in range(Q):
        parts = input().split()
        t = parts[0]

        if t == 'R':
            l = int(parts[1])
            r = int(parts[2])
            out.append(str(bit.range_sum(l, r)))
            continue

        # Update: U pos M plus
        pos0 = int(parts[1])
        M = int(parts[2])
        plus = int(parts[3])

        stamp += 1
        touched = []

        # Iterate i=1..50
        pos = pos0
        for _i in range(50):
            back = pos

            # j=1 transient from current pos
            transient = visited_in_one_j(pos)
            for a in transient:
                if vis[a] != stamp:
                    vis[a] = stamp
                    touched.append(a)
                delta[a] += M

            # j=2..1000 are fixed (999 times)
            bulk = M * 999
            for a in FIXED_ADDS:
                if vis[a] != stamp:
                    vis[a] = stamp
                    touched.append(a)
                delta[a] += bulk

            # after 1000 j-iterations, pos becomes FIXED (doesn't matter for next i)
            # next outer i uses back + plus (wrap once)
            pos = back + plus
            if pos > N:
                pos -= N

        # apply accumulated point updates to BIT
        for idx in touched:
            d = delta[idx]
            if d:
                bit.add(idx, d)
                delta[idx] = 0

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
