# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
from collections import defaultdict

MOD = 10**9 + 7

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))
        self.size = [1] * (n + 1)

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])

    dsu = DSU(n)

    idx = 1
    for _ in range(n - 1):
        u = int(data[idx]); v = int(data[idx + 1]); c = data[idx + 2].decode()
        idx += 3
        if c == 'b':  # union only black edges
            dsu.union(u, v)

    comp_sizes = defaultdict(int)
    for node in range(1, n + 1):
        comp_sizes[dsu.find(node)] += 1

    # Count sum_{i<j<k} s_i*s_j*s_k in O(k)
    prefix = 0      # sum of previous sizes
    prefix2 = 0     # sum of products of pairs among previous sizes
    ans = 0

    for s in comp_sizes.values():
        s %= MOD
        ans = (ans + s * prefix2) % MOD
        prefix2 = (prefix2 + s * prefix) % MOD
        prefix = (prefix + s) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    main()
