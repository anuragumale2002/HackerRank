# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
sys.setrecursionlimit(1_000_000)
MOD = 10**9 + 7

def solve():
    input = sys.stdin.readline
    n, q = map(int, input().split())

    g = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u, v = map(int, input().split())
        g[u].append(v)
        g[v].append(u)

    LOG = (n).bit_length()
    up = [[0] * (n + 1) for _ in range(LOG)]
    depth = [0] * (n + 1)
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)

    # ---------- iterative DFS for tin/tout + up[0] + depth ----------
    timer = 0
    stack = [(1, 1, 0)]  # (u, parent, state) state=0 enter, 1 exit
    while stack:
        u, p, state = stack.pop()
        if state == 0:
            timer += 1
            tin[u] = timer
            up[0][u] = p
            stack.append((u, p, 1))
            for v in g[u]:
                if v == p:
                    continue
                depth[v] = depth[u] + 1
                stack.append((v, u, 0))
        else:
            timer += 1
            tout[u] = timer

    for j in range(1, LOG):
        uj = up[j]
        ujm1 = up[j - 1]
        for v in range(1, n + 1):
            uj[v] = ujm1[ujm1[v]]

    def is_anc(a, b):
        return tin[a] <= tin[b] and tout[a] >= tout[b]

    def lca(a, b):
        if is_anc(a, b):
            return a
        if is_anc(b, a):
            return b
        x = a
        for j in range(LOG - 1, -1, -1):
            nx = up[j][x]
            if nx and not is_anc(nx, b):
                x = nx
        return up[0][x]

    def dist(a, b):
        w = lca(a, b)
        return depth[a] + depth[b] - 2 * depth[w]

    out = []

    for _ in range(q):
        k = int(input().strip())
        nodes = list(map(int, input().split()))
        nodes.sort(key=lambda x: tin[x])

        # add LCAs of consecutive nodes
        extra = [lca(nodes[i], nodes[i + 1]) for i in range(k - 1)]
        all_nodes = nodes + extra
        all_nodes.sort(key=lambda x: tin[x])

        # unique
        V = []
        last = -1
        for v in all_nodes:
            if v != last:
                V.append(v)
                last = v

        # ----- build virtual tree (standard, cycle-free) -----
        vt_children = {v: [] for v in V}
        st = [V[0]]

        for v in V[1:]:
            w = lca(v, st[-1])

            while len(st) >= 2 and depth[st[-2]] >= depth[w]:
                child = st.pop()
                vt_children[st[-1]].append(child)

            if st[-1] != w:
                child = st.pop()
                vt_children[w].append(child)
                if not st or st[-1] != w:
                    st.append(w)

            st.append(v)

        while len(st) > 1:
            child = st.pop()
            vt_children[st[-1]].append(child)

        root = st[0]

        # ----- DP on virtual tree without building a big 'order' list -----
        in_query = set(nodes)
        total = sum(nodes) % MOD

        subsum = {v: (v % MOD) if v in in_query else 0 for v in V}
        ans = 0

        stack2 = [(root, 0)]
        while stack2:
            u, state = stack2.pop()
            if state == 0:
                stack2.append((u, 1))
                for ch in vt_children.get(u, []):
                    stack2.append((ch, 0))
            else:
                for ch in vt_children.get(u, []):
                    w = subsum[ch] % MOD
                    d = dist(u, ch) % MOD
                    ans = (ans + d * w % MOD * ((total - w) % MOD)) % MOD
                    subsum[u] = (subsum[u] + w) % MOD

        out.append(str(ans))

    print("\n".join(out))

if __name__ == "__main__":
    solve()
