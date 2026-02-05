#!/usr/bin/env python3
import sys
import heapq

MOD = 10**9 + 7
INF = 10**18

# ---------- Iterative segment tree: point update, range min query ----------
class SegMin:
    __slots__ = ("n", "size", "seg")
    def __init__(self, n: int):
        self.n = n
        size = 1
        while size < n:
            size <<= 1
        self.size = size
        self.seg = [INF] * (2 * size)

    def update(self, pos: int, val: int) -> None:
        # pos is 1-indexed
        i = self.size + pos - 1
        seg = self.seg
        seg[i] = val
        i >>= 1
        while i:
            left = seg[i << 1]
            right = seg[(i << 1) | 1]
            seg[i] = left if left < right else right
            i >>= 1

    def query(self, l: int, r: int) -> int:
        # inclusive, l/r are 1-indexed
        seg = self.seg
        l = l + self.size - 1
        r = r + self.size - 1
        res = INF
        while l <= r:
            if (l & 1) == 1:
                v = seg[l]
                if v < res: res = v
                l += 1
            if (r & 1) == 0:
                v = seg[r]
                if v < res: res = v
                r -= 1
            l >>= 1
            r >>= 1
        return res


def main():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    par_in = list(map(int, input().split()))

    children = [[] for _ in range(n + 1)]
    parent = [0] * (n + 1)
    parent[1] = 0
    for i in range(2, n + 1):
        p = par_in[i - 2]
        parent[i] = p
        children[p].append(i)

    # ---- Euler tour + depth + postorder ----
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    depth = [0] * (n + 1)
    post = []

    t = 0
    stack = [(1, 0)]  # (node, state) state 0=enter, 1=exit
    depth[1] = 1
    while stack:
        u, st = stack.pop()
        if st == 0:
            t += 1
            tin[u] = t
            stack.append((u, 1))
            # push children in reverse so original order doesn't matter
            for v in reversed(children[u]):
                depth[v] = depth[u] + 1
                stack.append((v, 0))
        else:
            tout[u] = t
            post.append(u)

    # ---- Binary lifting table for UP(u, k) ----
    LOG = (n).bit_length()
    up = [parent[:] ]  # up[0][u]
    for j in range(1, LOG):
        prev = up[j - 1]
        cur = [0] * (n + 1)
        for u in range(1, n + 1):
            cur[u] = prev[prev[u]]
        up.append(cur)

    def jump(u: int, k: int) -> int:
        j = 0
        while k and u:
            if k & 1:
                u = up[j][u]
            k >>= 1
            j += 1
        return u

    # ---- dist to nearest leaf in subtree (bottom-up) ----
    dist = [0] * (n + 1)
    # bucket nodes by dist
    buckets = [[] for _ in range(n + 2)]
    for u in post:
        if not children[u]:
            dist[u] = 0
        else:
            mn = INF
            for v in children[u]:
                dv = dist[v] + 1
                if dv < mn:
                    mn = dv
            dist[u] = mn
        if dist[u] <= n:
            buckets[dist[u]].append(u)

    # ---- Segment tree stores depth at tin[u] if u is "active", else INF ----
    seg = SegMin(n)
    leaf_count = 0
    for u in range(1, n + 1):
        if dist[u] == 0:  # leaf
            seg.update(tin[u], depth[u])
            leaf_count += 1

    # ---- Precompute ans[k] for k=1..n ----
    ans = [0] * (n + 1)
    ans[1] = n

    heap = []  # max-heap by depth => store (-depth, node)

    for k in range(2, n + 1):
        total = leaf_count
        for u in buckets[k]:
            heapq.heappush(heap, (-depth[u], u))

        activated = []
        while heap:
            _, u = heapq.heappop(heap)

            # if there's already an active node within distance < k below u, skip
            mn_depth_in_sub = seg.query(tin[u], tout[u])
            if mn_depth_in_sub - depth[u] < k:
                continue

            # activate u
            seg.update(tin[u], depth[u])
            total += 1
            activated.append(u)

            # push ancestor k steps up (if exists)
            a = jump(u, k)
            if a:
                heapq.heappush(heap, (-depth[a], a))

        ans[k] = total

        # rollback activations for next k (only leaves remain permanently active)
        for u in activated:
            seg.update(tin[u], INF)

    # ---- Answer queries ----
    out = 0
    for _ in range(m):
        c, k = map(int, input().split())
        if k > n:
            k = n
        out = (out + (c % MOD) * (ans[k] % MOD)) % MOD

    print(out)

if __name__ == "__main__":
    main()
