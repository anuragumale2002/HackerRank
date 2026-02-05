import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

# ----------------------------
# Build BST as a Cartesian tree
# ----------------------------
def build_cartesian_tree(n, perm):
    # pr[v] = insertion time (smaller => earlier => higher in tree)
    pr = [0] * (n + 1)
    for i, v in enumerate(perm):
        pr[v] = i

    left = [0] * (n + 1)
    right = [0] * (n + 1)

    st = []
    for v in range(1, n + 1):
        last = 0
        pv = pr[v]
        while st and pr[st[-1]] > pv:
            last = st.pop()
        if st:
            right[st[-1]] = v
        if last:
            left[v] = last
        st.append(v)

    root = st[0]  # bottom of stack
    # Build undirected adjacency
    g = [[] for _ in range(n + 1)]
    for v in range(1, n + 1):
        if left[v]:
            g[v].append(left[v])
            g[left[v]].append(v)
        if right[v]:
            g[v].append(right[v])
            g[right[v]].append(v)
    return g

# ----------------------------
# Centroid Decomposition helpers
# ----------------------------
def centroid_decomposition(g):
    n = len(g) - 1
    removed = [False] * (n + 1)
    parent = [-1] * (n + 1)
    sub = [0] * (n + 1)

    path_cent = [[] for _ in range(n + 1)]
    path_dist = [[] for _ in range(n + 1)]

    def collect_nodes(start):
        # iterative DFS to collect component nodes + parent-in-dfs tree + order
        stack = [(start, -1)]
        order = []
        par = {start: -1}
        nodes = []
        while stack:
            u, p = stack.pop()
            if removed[u]:
                continue
            nodes.append(u)
            order.append(u)
            for v in g[u]:
                if removed[v] or v == p:
                    continue
                par[v] = u
                stack.append((v, u))
        # compute subtree sizes (rooted at start in this traversal tree)
        for u in reversed(order):
            s = 1
            for v in g[u]:
                if removed[v]:
                    continue
                if par.get(v, None) == u:
                    s += sub[v]
            sub[u] = s
        return nodes, par, sub[start]

    def find_centroid(start):
        nodes, par, total = collect_nodes(start)
        best = total + 1
        cent = start
        for u in nodes:
            mx = total - sub[u]
            for v in g[u]:
                if removed[v]:
                    continue
                if par.get(v, None) == u:
                    if sub[v] > mx:
                        mx = sub[v]
            if mx < best:
                best = mx
                cent = u
        return cent

    def add_paths_from_centroid(c):
        # add (c, dist) to every node in its current component (centroid not removed yet)
        path_cent[c].append(c)
        path_dist[c].append(0)
        for nb in g[c]:
            if removed[nb]:
                continue
            st = [(nb, c, 1)]
            while st:
                u, p, d = st.pop()
                if removed[u]:
                    continue
                path_cent[u].append(c)
                path_dist[u].append(d)
                for v in g[u]:
                    if removed[v] or v == p:
                        continue
                    st.append((v, u, d + 1))

    def decompose(start, pcent):
        c = find_centroid(start)
        add_paths_from_centroid(c)
        removed[c] = True
        parent[c] = pcent
        for nb in g[c]:
            if not removed[nb]:
                decompose(nb, c)

    decompose(1, -1)

    # reverse to make order: closest centroid first, then up to root
    for u in range(1, n + 1):
        path_cent[u].reverse()
        path_dist[u].reverse()

    return parent, path_cent, path_dist

# ----------------------------
# Dynamic distance-sum maintenance
# ----------------------------
def solve():
    n = int(input().strip())
    perm = list(map(int, input().split()))

    g = build_cartesian_tree(n, perm)

    cd_parent, path_cent, path_dist = centroid_decomposition(g)

    cnt = [0] * (n + 1)
    sd = [0] * (n + 1)        # sum of dist(node, centroid) for active nodes
    sub_cnt = [0] * (n + 1)   # stored on child-centroid: counts to exclude at parent
    sub_sd = [0] * (n + 1)    # stored on child-centroid: sum of dist(active, parent-centroid)

    def query_sum_to_active(x):
        # sum of distances from x to all active nodes
        res = 0
        cent_list = path_cent[x]
        dist_list = path_dist[x]
        prev = -1
        for c, d in zip(cent_list, dist_list):
            res += sd[c] + cnt[c] * d
            if prev != -1:
                res -= sub_sd[prev] + sub_cnt[prev] * d
            prev = c
        return res

    def activate(x):
        # add x as active
        cent_list = path_cent[x]
        dist_list = path_dist[x]
        prev = -1
        for c, d in zip(cent_list, dist_list):
            cnt[c] += 1
            sd[c] += d
            if prev != -1:
                sub_cnt[prev] += 1
                sub_sd[prev] += d
            prev = c

    total = 0
    out = []
    for x in perm:
        inc = query_sum_to_active(x)
        total += inc
        out.append(str(total))
        activate(x)

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
