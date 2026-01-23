import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:]))

    # Prefix sums and prefix sums of squares
    P = [0] * (n + 1)
    Q = [0] * (n + 1)
    for i, v in enumerate(a, 1):
        P[i] = P[i - 1] + v
        Q[i] = Q[i - 1] + v * v

    # We only ever query at x = P[i], so Li Chao can run on a discrete set of x's
    xs = sorted(set(P))

    def f(line, x):
        m, b = line
        return m * x + b

    class LiChao:
        __slots__ = ("xs", "seg")
        def __init__(self, xs):
            self.xs = xs
            self.seg = [None] * (4 * len(xs))

        def add_line(self, new_line):
            xs = self.xs
            seg = self.seg

            def rec(idx, l, r, line):
                if seg[idx] is None:
                    seg[idx] = line
                    return

                mid = (l + r) >> 1
                xL, xM, xR = xs[l], xs[mid], xs[r]

                cur = seg[idx]

                # keep the better line at mid
                if f(line, xM) > f(cur, xM):
                    seg[idx], line = line, cur
                    cur = seg[idx]

                if l == r:
                    return

                # Now 'line' is worse at mid; it can only help on a side if it beats 'cur' at that endpoint.
                if f(line, xL) > f(cur, xL):
                    rec(idx << 1, l, mid, line)
                elif f(line, xR) > f(cur, xR):
                    rec(idx << 1 | 1, mid + 1, r, line)
                # else: worse everywhere on this segment -> discard

            rec(1, 0, len(xs) - 1, new_line)

        def query(self, x):
            xs = self.xs
            seg = self.seg
            res = -10**100  # safe for constraints

            def rec(idx, l, r):
                nonlocal res
                if seg[idx] is not None:
                    res = max(res, f(seg[idx], x))
                if l == r:
                    return
                mid = (l + r) >> 1
                if x <= xs[mid]:
                    rec(idx << 1, l, mid)
                else:
                    rec(idx << 1 | 1, mid + 1, r)

            rec(1, 0, len(xs) - 1)
            return res

    # Value(subarray) = sum_{i<j} ai*aj = ((sum)^2 - sumsq) / 2
    # For fixed r, maximize:
    # (P[r]-P[k])^2 - (Q[r]-Q[k]) = (P[r]^2 - Q[r]) + max_k [(-2P[k]) * P[r] + (P[k]^2 + Q[k])]
    lc = LiChao(xs)
    lc.add_line((0, 0))  # k = 0

    best_num = 0  # length-1 subarray has value 0, so answer >= 0

    for r in range(1, n + 1):
        x = P[r]
        best_num = max(best_num, x * x - Q[r] + lc.query(x))
        lc.add_line((-2 * x, x * x + Q[r]))

    print(best_num // 2)

if __name__ == "__main__":
    solve()
