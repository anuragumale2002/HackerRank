# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys

# Increase recursion for safety, though we use iterative DFS
sys.setrecursionlimit(300000)

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    q = int(input_data[1])
    MOD = 10**9 + 7
    
    adj = [[] for _ in range(n + 1)]
    ptr = 2
    for i in range(2, n + 1):
        p = int(input_data[ptr])
        adj[p].append(i)
        ptr += 1
        
    # 1. Precompute Fibonacci and Prefix Sums with safe padding
    # Needs to go up to n+1 to handle depth indexing safely
    LIMIT = n + 5
    fib = [0] * (LIMIT + 2)
    fib[1] = 1
    for i in range(2, LIMIT + 2):
        fib[i] = (fib[i-1] + fib[i-2]) % MOD
        
    sf0 = [0] * (LIMIT + 1) # Sum of F(i)
    sf1 = [0] * (LIMIT + 1) # Sum of F(i+1)
    c0, c1 = 0, 0
    for i in range(LIMIT + 1):
        c0 = (c0 + fib[i]) % MOD
        c1 = (c1 + fib[i+1]) % MOD
        sf0[i] = c0
        sf1[i] = c1

    # 2. Iterative DFS for tin, tout, and Binary Lifting table
    tin = [0] * (n + 1)
    tout = [0] * (n + 1)
    depth = [0] * (n + 1)
    LOG = n.bit_length()
    up = [[0] * LOG for _ in range(n + 1)]
    timer = 0
    
    stack = [(1, 0, 0)]
    while stack:
        u, d, p = stack.pop()
        if u > 0: # Entry
            timer += 1
            tin[u] = timer
            depth[u] = d
            up[u][0] = p
            for i in range(1, LOG):
                up[u][i] = up[up[u][i-1]][i-1]
            
            stack.append((-u, d, p)) # Mark for exit
            for v in reversed(adj[u]):
                stack.append((v, d + 1, u))
        else: # Exit
            tout[-u] = timer

    # 3. Fast Fibonacci for large K (Fast Doubling)
    memo_f = {}
    def get_fib_any(k):
        if 0 <= k < len(fib): return fib[k]
        if k < 0:
            # F(-k) = (-1)^(k+1) * F(k)
            f = get_fib_any(-k)
            return f if (-k) % 2 != 0 else (MOD - f) % MOD
        if k in memo_f: return memo_f[k]
        
        def _doubling(m):
            if m == 0: return (0, 1)
            a, b = _doubling(m >> 1)
            c = (a * (2 * b - a)) % MOD
            d = (a * a + b * b) % MOD
            if m & 1: return (d, (c + d) % MOD)
            return (c, d)
        
        res = _doubling(k)[0]
        memo_f[k] = res
        return res

    def get_lca(u, v):
        if depth[u] < depth[v]: u, v = v, u
        diff = depth[u] - depth[v]
        for i in range(LOG):
            if (diff >> i) & 1: u = up[u][i]
        if u == v: return u
        for i in range(LOG - 1, -1, -1):
            if up[u][i] != up[v][i]:
                u = up[u][i]
                v = up[v][i]
        return up[u][0]

    # 4. BIT structure for Path Sum components
    bit1 = [0] * (n + 2)
    bit2 = [0] * (n + 2)
    bit3 = [0] * (n + 2)

    def update(bit, i, val):
        while i <= n:
            bit[i] = (bit[i] + val) % MOD
            i += i & (-i)

    def query(bit, i):
        s = 0
        while i > 0:
            s = (s + bit[i]) % MOD
            i -= i & (-i)
        return s

    # 5. Process Queries
    results = []
    for _ in range(q):
        qt = input_data[ptr]
        if qt == 'U':
            x, k = int(input_data[ptr+1]), int(input_data[ptr+2])
            ptr += 3
            # Component values based on Fibonacci Identity
            c1 = get_fib_any(k - depth[x])
            c2 = get_fib_any(k - depth[x] - 1)
            offset = 0
            if depth[x] > 0:
                offset = (c1 * sf1[depth[x]-1] + c2 * sf0[depth[x]-1]) % MOD
            
            l, r = tin[x], tout[x]
            for b, v in [(bit1, c1), (bit2, c2), (bit3, offset)]:
                update(b, l, v)
                update(b, r + 1, (MOD - v) % MOD)
        else:
            u, v = int(input_data[ptr+1]), int(input_data[ptr+2])
            ptr += 3
            lca = get_lca(u, v)
            
            def path_to_root(node):
                if node == 0: return 0
                s1, s2, s3 = query(bit1, tin[node]), query(bit2, tin[node]), query(bit3, tin[node])
                return (sf1[depth[node]] * s1 + sf0[depth[node]] * s2 - s3) % MOD
            
            def node_val(node):
                s1, s2 = query(bit1, tin[node]), query(bit2, tin[node])
                return (fib[depth[node]+1] * s1 + fib[depth[node]] * s2) % MOD

            ans = (path_to_root(u) + path_to_root(v) - 2 * path_to_root(lca) + node_val(lca)) % MOD
            results.append(str(ans))

    sys.stdout.write("\n".join(results) + "\n")

if __name__ == "__main__":
    solve()