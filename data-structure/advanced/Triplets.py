import sys

class BIT:
    __slots__ = ("n", "bit")
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)

    def add(self, i, v):
        n = self.n
        while i <= n:
            self.bit[i] += v
            i += i & -i

    def sum(self, i):
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    a = data[1:1 + n]

    # Coordinate compress values to 1..m
    vals = sorted(set(a))
    m = len(vals)
    idx = {v: i + 1 for i, v in enumerate(vals)}
    comp = [idx[v] for v in a]

    # L[j] = number of distinct values < a[j] seen before j
    bit = BIT(m)
    seen = [0] * (m + 1)
    L = [0] * n
    for j in range(n):
        x = comp[j]
        L[j] = bit.sum(x - 1)
        if seen[x] == 0:
            seen[x] = 1
            bit.add(x, 1)

    # R[j] = number of distinct values > a[j] seen after j
    bit = BIT(m)
    seen = [0] * (m + 1)
    R = [0] * n
    total = 0
    for j in range(n - 1, -1, -1):
        x = comp[j]
        # distinct greater = total distinct in suffix - distinct <= x
        R[j] = total - bit.sum(x)
        if seen[x] == 0:
            seen[x] = 1
            bit.add(x, 1)
            total += 1

    # Collect positions per value (compressed)
    pos = [[] for _ in range(m + 1)]
    for i, x in enumerate(comp):
        pos[x].append(i)

    ans = 0
    for y in range(1, m + 1):
        p = pos[y]
        if len(p) == 1:
            i = p[0]
            ans += L[i] * R[i]
        else:
            i1, i2 = p[0], p[1]
            A = L[i1]
            B = L[i2]
            C = R[i1]
            D = R[i2]
            ans += A * (C - D) + B * D

    sys.stdout.write(str(ans))

if __name__ == "__main__":
    solve()
