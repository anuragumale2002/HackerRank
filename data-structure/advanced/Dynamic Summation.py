# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

# ---------- L = lcm(1..101) ----------
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a // gcd(a, b) * b

MOD = 1
for i in range(1, 102):
    MOD = lcm(MOD, i)

# ---------- Fenwick for range add, range sum ----------
class Fenwick:
    __slots__ = ("n", "bit")
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 2)

    def add(self, i, delta):
        n = self.n
        bit = self.bit
        # delta already modded
        while i <= n:
            bit[i] = (bit[i] + delta) % MOD
            i += i & -i

    def sum(self, i):
        s = 0
        bit = self.bit
        while i > 0:
            s += bit[i]
            i -= i & -i
        return s % MOD

class RangeFenwick:
    __slots__ = ("n", "b1", "b2")
    def __init__(self, n):
        self.n = n
        self.b1 = Fenwick(n)
        self.b2 = Fenwick(n)

    def _add_range(self, l, r, val):
        if l > r:
            return
        val %= MOD
        # b1
        self.b1.add(l, val)
        self.b1.add(r + 1, (-val) % MOD)
        # b2
        self.b2.add(l, (val * (l - 1)) % MOD)
        self.b2.add(r + 1, (-val * r) % MOD)

    def range_add(self, l, r, val):
        self._add_range(l, r, val)

    def prefix_sum(self, x):
        if x <= 0:
            return 0
        s1 = self.b1.sum(x)
        s2 = self.b2.sum(x)
        return (s1 * x - s2) % MOD

    def range_sum(self, l, r):
        return (self.prefix_sum(r) - self.prefix_sum(l - 1)) % MOD

# ---------- Tree preprocessing (root fixed at 1) ----------
def solve():
    n = int(input().strip())
    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        x, y = map(int, input().split())
        g[x].append(y)
        g[y].append(x)

    LOG = (n).bit_length()
    up = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    timer = 0

    # iterative DFS to avoid recursion depth issues
    stack = [(1, 0, 0)]  # (u, parent, state) state 0 enter, 1 exit
    parent = [0] * (n + 1)
    parent[1] = 0
    depth[1] = 0

    while stack:
        u, p, state = stack.pop()
        if state == 0:
            timer += 1
            tin[u] = timer
            parent[u] = p
            up[0][u] = p
            stack.append((u, p, 1))
            for v in g[u]:
                if v == p:
                    continue
                depth[v] = depth[u] + 1
                stack.append((v, u, 0))
        else:
            tout[u] = timer

    for k in range(1, LOG):
        uk = up[k - 1]
        uk2 = up[k]
        for v in range(1, n + 1):
            uk2[v] = uk[uk[v]]

    def is_ancestor(u, v):
        return tin[u] <= tin[v] <= tout[u]

    def lift(u, steps):
        i = 0
        while steps:
            if steps & 1:
                u = up[i][u]
            steps >>= 1
            i += 1
        return u

    # Convert "subtree of t when rooted at r" into:
    # - either (l,r, is_complement=False)
    # - or (l,r, is_complement=True) meaning whole tree minus [l,r]
    def rooted_subtree_interval(r, t):
        if r == t:
            return 1, n, False  # whole tree
        if not is_ancestor(t, r):
            return tin[t], tout[t], False
        # t is ancestor of r: subtree(t) under root r is whole tree minus subtree(child)
        # child is the node just below t on path to r
        child = lift(r, depth[r] - depth[t] - 1)
        return tin[child], tout[child], True

    rf = RangeFenwick(n)

    q = int(input().strip())
    out = []
    for _ in range(q):
        parts = input().split()
        if parts[0] == 'U':
            r = int(parts[1]); t = int(parts[2])
            a = int(parts[3]); b = int(parts[4])

            # value = a^b + (a+1)^b + (b+1)^a  (mod L)
            val = (pow(a, b, MOD) + pow(a + 1, b, MOD) + pow(b + 1, a, MOD)) % MOD

            l, rr, comp = rooted_subtree_interval(r, t)
            if not comp:
                rf.range_add(l, rr, val)
            else:
                # whole tree +val, then subtract subtree(child)
                rf.range_add(1, n, val)
                rf.range_add(l, rr, (-val) % MOD)

        else:  # 'R'
            r = int(parts[1]); t = int(parts[2]); m = int(parts[3])
            l, rr, comp = rooted_subtree_interval(r, t)
            if not comp:
                s = rf.range_sum(l, rr)
            else:
                s = (rf.range_sum(1, n) - rf.range_sum(l, rr)) % MOD
            out.append(str(s % m))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
