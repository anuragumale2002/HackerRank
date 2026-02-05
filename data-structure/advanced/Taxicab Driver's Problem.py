import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

# ---------------- Fenwick (BIT) ----------------
class Fenwick:
    __slots__ = ("n", "bit")
    def __init__(self, n):
        self.n = n
        self.bit = [0] * (n + 1)
    def add(self, i, delta):
        n = self.n
        bit = self.bit
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

# Count unordered pairs (a,b) from "points" such that:
# dx[a] + dx[b] <= H and dy[a] + dy[b] <= V.
def count_pairs(points, H, V):
    m = len(points)
    if m <= 1:
        return 0

    # coordinate compress dy
    ys = sorted({dy for _, dy in points})
    ylen = len(ys)

    pts = sorted(points)  # sort by dx
    queries = []
    self_ok = 0

    # build queries (max_dx, max_dy) for each point i
    for dx, dy in pts:
        if 2 * dx <= H and 2 * dy <= V:
            self_ok += 1
        queries.append((H - dx, V - dy))

    queries.sort(key=lambda t: t[0])  # sort by max_dx

    bit = Fenwick(ylen)
    total_ordered = 0
    p = 0  # pointer over pts to add those with dx <= current max_dx

    # helper: upper_bound on ys
    from bisect import bisect_right

    for max_dx, max_dy in queries:
        if max_dx < 0 or max_dy < 0:
            continue

        while p < m and pts[p][0] <= max_dx:
            dy = pts[p][1]
            bit.add(bisect_right(ys, dy), 1)
            p += 1

        idx = bisect_right(ys, max_dy)
        if idx > 0:
            total_ordered += bit.sum(idx)

    # unordered = (ordered - self_pairs) / 2
    return (total_ordered - self_ok) // 2

# ---------------- Centroid Decomposition ----------------
def solve():
    n, H, V = map(int, input().split())
    x = [0] * (n + 1)
    y = [0] * (n + 1)
    for i in range(1, n + 1):
        xi, yi = map(int, input().split())
        x[i] = xi
        y[i] = yi

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        a, b = map(int, input().split())
        wx = abs(x[a] - x[b])
        wy = abs(y[a] - y[b])
        g[a].append((b, wx, wy))
        g[b].append((a, wx, wy))

    removed = [False] * (n + 1)
    sub = [0] * (n + 1)

    def dfs_size(u, p):
        sub[u] = 1
        for v, wx, wy in g[u]:
            if v == p or removed[v]:
                continue
            dfs_size(v, u)
            sub[u] += sub[v]

    def dfs_centroid(u, p, tot):
        for v, wx, wy in g[u]:
            if v == p or removed[v]:
                continue
            if sub[v] > tot // 2:
                return dfs_centroid(v, u, tot)
        return u

    # collect (dx, dy) distances from start node into list, pruning if exceed H or V
    def dfs_collect(u, p, dx, dy, arr):
        if dx > H or dy > V:
            return
        arr.append((dx, dy))
        for v, wx, wy in g[u]:
            if v == p or removed[v]:
                continue
            dfs_collect(v, u, dx + wx, dy + wy, arr)

    def decompose(entry):
        dfs_size(entry, -1)
        c = dfs_centroid(entry, -1, sub[entry])
        removed[c] = True

        # all points from centroid
        all_pts = [(0, 0)]
        child_lists = []

        for v, wx, wy in g[c]:
            if removed[v]:
                continue
            arr = []
            dfs_collect(v, c, wx, wy, arr)
            if arr:
                child_lists.append(arr)
                all_pts.extend(arr)

        res = count_pairs(all_pts, H, V)
        for arr in child_lists:
            # subtract pairs entirely inside this child subtree
            res -= count_pairs(arr, H, V)

        for v, wx, wy in g[c]:
            if not removed[v]:
                res += decompose(v)

        return res

    good = decompose(1)
    total = n * (n - 1) // 2
    bad = total - good
    print(bad)

if __name__ == "__main__":
    solve()
