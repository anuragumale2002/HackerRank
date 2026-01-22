import sys

# Increase recursion depth for deep trees (N=10^5)
sys.setrecursionlimit(300000)

def solve():
    # Read all input data for speed
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    colors = [0] * (n + 1)
    present_colors = set()
    for i in range(1, n + 1):
        c = int(input_data[i])
        colors[i] = c
        present_colors.add(c)
        
    adj = [[] for _ in range(n + 1)]
    idx = n + 1
    for _ in range(n - 1):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        adj[u].append(v)
        adj[v].append(u)
        idx += 2
        
    # max_color helps size the global_sum array
    max_c = max(present_colors) if present_colors else 0
    global_sum = [0] * (max_c + 1)
    children_data = [[] for _ in range(n + 1)]
    
    # First DFS to compute subtree sizes and identify component boundaries
    def dfs_pre(u, p):
        c = colors[u]
        sb_u = global_sum[c]
        s_u = 1
        
        u_children = children_data[u]
        for v in adj[u]:
            if v == p:
                continue
            
            sb_v = global_sum[c]
            sz_v = dfs_pre(v, u)
            s_u += sz_v
            sa_v = global_sum[c]
            
            # m_uv is the size of the component starting at child v not containing color(u)
            m_uv = sz_v - (sa_v - sb_v)
            u_children.append((v, m_uv))
        
        global_sum[c] = sb_u + s_u
        return s_u

    dfs_pre(1, 0)
    
    # Calculate sizes of the 'top' components (nodes with no ancestor of color C)
    current_m = [0] * (max_c + 1)
    total_m_sum = 0
    num_distinct = len(present_colors)
    
    for c in present_colors:
        m_top = n - global_sum[c]
        current_m[c] = m_top
        total_m_sum += m_top
        
    results = [0] * (n + 1)
    
    # Second DFS to propagate component size sums
    def dfs_calc(u, p, curr_sum):
        c = colors[u]
        m_prev = current_m[c]
        
        # Total component sum for node u: remove the inherited component size for its own color
        g_u = curr_sum - m_prev
        results[u] = n * num_distinct - g_u
        
        # Base sum for all paths through children
        base = g_u
        
        for v, m_uv in children_data[u]:
            current_m[c] = m_uv
            dfs_calc(v, u, base + m_uv)
            
        # Backtrack state
        current_m[c] = m_prev

    dfs_calc(1, 0, total_m_sum)
    
    # Fast output
    sys.stdout.write('\n'.join(map(str, results[1:])) + '\n')

if __name__ == '__main__':
    solve()