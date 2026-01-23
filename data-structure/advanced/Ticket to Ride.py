#!/bin/python3
import sys

# ---------- Fast int parser ----------
def ints_from_stdin():
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
        val = 0
        while i < n and data[i] > 32:
            val = val * 10 + (data[i] - 48)
            i += 1
        yield sign * val

# ---------- Iterative Lazy Segment Tree (range add, range max) ----------
class LazySegMaxAdd:
    __slots__ = ("n", "size", "log", "data", "lz")
    def __init__(self, n):
        self.n = n
        size = 1
        log = 0
        while size < n:
            size <<= 1
            log += 1
        self.size = size
        self.log = log
        # 1-indexed internal nodes: [1 .. size-1], leaves: [size .. 2*size-1]
        self.data = [0] * (2 * size)
        self.lz = [0] * size

    def _all_apply(self, k, f):
        self.data[k] += f
        if k < self.size:
            self.lz[k] += f

    def _push(self, k):
        f = self.lz[k]
        if f:
            self._all_apply(k * 2, f)
            self._all_apply(k * 2 + 1, f)
            self.lz[k] = 0

    def _pull(self, k):
        # children already include their own lazy; k's lazy applies to the max
        self.data[k] = (self.data[k * 2] if self.data[k * 2] >= self.data[k * 2 + 1] else self.data[k * 2 + 1]) + self.lz[k]

    # add f to [l, r)
    def add(self, l, r, f):
        if l >= r:
            return
        size = self.size
        l += size
        r += size
        l0, r0 = l, r

        # push down on the paths
        for i in range(self.log, 0, -1):
            if ((l0 >> i) << i) != l0:
                self._push(l0 >> i)
            if ((r0 >> i) << i) != r0:
                self._push((r0 - 1) >> i)

        while l < r:
            if l & 1:
                self._all_apply(l, f)
                l += 1
            if r & 1:
                r -= 1
                self._all_apply(r, f)
            l >>= 1
            r >>= 1

        # pull up
        for i in range(1, self.log + 1):
            if ((l0 >> i) << i) != l0:
                self._pull(l0 >> i)
            if ((r0 >> i) << i) != r0:
                self._pull((r0 - 1) >> i)

    # max on [l, r)
    def max(self, l, r):
        if l >= r:
            return -10**30
        size = self.size
        l += size
        r += size

        # push down on the paths
        for i in range(self.log, 0, -1):
            if ((l >> i) << i) != l:
                self._push(l >> i)
            if ((r >> i) << i) != r:
                self._push((r - 1) >> i)

        left_res = -10**30
        right_res = -10**30

        while l < r:
            if l & 1:
                if self.data[l] > left_res:
                    left_res = self.data[l]
                l += 1
            if r & 1:
                r -= 1
                if self.data[r] > right_res:
                    right_res = self.data[r]
            l >>= 1
            r >>= 1

        return left_res if left_res >= right_res else right_res

# ---------- Solution ----------
def solve():
    it = ints_from_stdin()
    try:
        N = next(it)
    except StopIteration:
        return

    adj = [[] for _ in range(N + 1)]      # road tree
    tickets = [[] for _ in range(N + 1)]  # ticket graph (mutated)

    for _ in range(N - 1):
        a = next(it); b = next(it); c = next(it)
        adj[a].append((b, c))
        adj[b].append((a, c))

    M = next(it)
    for _ in range(M):
        a = next(it); b = next(it); c = next(it)
        tickets[a].append((b, c))
        if a != b:
            tickets[b].append((a, c))

    blocked = [False] * (N + 1)
    sz = [0] * (N + 1)
    par = [0] * (N + 1)

    tin = [0] * (N + 1)
    tout = [0] * (N + 1)

    visited = [False] * (N + 1)  # per-centroid pass
    on_stack = [False] * (N + 1)
    base = [0] * (N + 1)

    comp_mark = [0] * (N + 1)
    cur_mark = 0

    def calc_size(root):
        stack = [(root, 0, 0)]
        while stack:
            u, p, st = stack.pop()
            if st == 0:
                par[u] = p
                stack.append((u, p, 1))
                for v, _w in adj[u]:
                    if v != p and not blocked[v]:
                        stack.append((v, u, 0))
            else:
                s = 1
                for v, _w in adj[u]:
                    if v != p and not blocked[v]:
                        s += sz[v]
                sz[u] = s

    def find_centroid(root, tot):
        u = root
        half = tot >> 1
        while True:
            moved = False
            pu = par[u]
            for v, _w in adj[u]:
                if blocked[v]:
                    continue
                # v is child in the rooting at `root`
                if par[v] == u:
                    part = sz[v]
                # v is parent side
                elif v == pu:
                    part = tot - sz[u]
                else:
                    continue
                if part > half:
                    u = v
                    moved = True
                    break
            if not moved:
                return u

    def init_euler(root):
        nonlocal cur_mark
        cur_mark += 1
        mark = cur_mark

        now = 0
        stack = [(root, 0, 0)]
        while stack:
            u, p, st = stack.pop()
            if st == 0:
                comp_mark[u] = mark
                visited[u] = False
                on_stack[u] = False
                tin[u] = now
                now += 1

                stack.append((u, p, 1))
                # reverse so traversal order matches recursive order on adj[u]
                for v, _w in reversed(adj[u]):
                    if v != p and not blocked[v]:
                        stack.append((v, u, 0))
            else:
                tout[u] = now
        return now, mark

    def dfs_iter(start, parent, start_cost, sroot, seg, mark):
        in_s = tin[sroot]
        out_s = tout[sroot]

        # frame: [u, p, next_idx, cost, best, p2_list]
        stack = [[start, parent, 0, start_cost, -10**30, None]]

        while stack:
            fr = stack[-1]
            u, p = fr[0], fr[1]

            if fr[5] is None:
                # enter
                visited[u] = True
                on_stack[u] = True

                bu = fr[3]
                p1 = []
                p2 = []

                for v, c in tickets[u]:
                    if comp_mark[v] != mark:
                        continue  # discard edges leaving this component
                    if on_stack[v]:
                        bu += c
                    tv = tin[v]
                    if in_s <= tv < out_s:
                        p1.append((v, c))
                    elif visited[v]:
                        p2.append((v, c))

                base[u] = bu
                tickets[u] = p1  # keep only "internal to this subtree/component" edges

                seg.add(tin[u], tin[u] + 1, bu)
                for v, c in p2:
                    seg.add(tin[v], tout[v], c)

                fr[4] = bu + seg.max(0, in_s)
                fr[5] = p2

            adj_u = adj[u]
            # advance children
            while fr[2] < len(adj_u):
                v, w = adj_u[fr[2]]
                fr[2] += 1
                if v == p or blocked[v]:
                    continue
                stack.append([v, u, 0, base[u] - w, -10**30, None])
                break
            else:
                # exit
                p2 = fr[5]
                if p2:
                    for v, c in p2:
                        seg.add(tin[v], tout[v], -c)
                on_stack[u] = False

                res = fr[4]
                stack.pop()
                if stack:
                    if res > stack[-1][4]:
                        stack[-1][4] = res
                else:
                    return res

        return -10**30

    def solve_through_centroid(c, tot):
        # Euler tour for this component rooted at centroid c
        cnt, mark = init_euler(c)
        # cnt should equal tot, but we trust tot for segtree size
        seg = LazySegMaxAdd(tot)

        # base for centroid: sum of self-loop tickets (c,c)
        bc = 0
        for v, cost in tickets[c]:
            if v == c:
                bc += cost
        base[c] = bc

        on_stack[c] = True
        best = bc  # path is just [c]

        # process centroid children in the same order as Euler DFS would
        for v, w in adj[c]:
            if blocked[v]:
                continue
            # path from centroid to nodes includes road cost (subtract w, and more along the walk)
            sub_best = dfs_iter(v, c, -w, v, seg, mark)
            val = bc + sub_best
            if val > best:
                best = val

        on_stack[c] = False
        return best

    sys.setrecursionlimit(1_000_000)
    def decompose(entry):
        calc_size(entry)
        tot = sz[entry]
        c = find_centroid(entry, tot)
        ans = solve_through_centroid(c, tot)

        blocked[c] = True
        for v, _w in adj[c]:
            if not blocked[v]:
                sub = decompose(v)
                if sub > ans:
                    ans = sub
        return ans

    ans = decompose(1)
    sys.stdout.write(str(ans) + "\n")

if __name__ == "__main__":
    solve()



# This one times out