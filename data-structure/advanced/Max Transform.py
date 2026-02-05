import sys

P = 1_000_000_007

def solve() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return
    n = data[0]
    arr = data[1:1+n]

    # Group positions by value (1-indexed positions)
    pos = {}
    ma = 0
    for i, v in enumerate(arr, 1):
        if v > ma:
            ma = v
        pos.setdefault(v, []).append(i)

    # Precompute f[i] for i=1..n
    inv2 = (P + 1) // 2
    inv6 = pow(6, P - 2, P)

    f = [0] * (n + 2)
    for i in range(1, n + 1):
        ii = i % P
        ip1 = (i + 1) % P
        # S2 = i(i+1)(2i+1)/6 mod P
        s2 = ii * ip1 % P
        s2 = s2 * ((2 * i + 1) % P) % P
        s2 = s2 * inv6 % P
        # S1 = i(i+1)/2 mod P
        s1 = ii * ip1 % P
        s1 = s1 * inv2 % P
        # f = (S2 + S1)/2 mod P
        f[i] = (s2 + s1) % P
        f[i] = f[i] * inv2 % P

    # T = t*(t+1)/2 where t = n(n+1)/2
    t = (n % P) * ((n + 1) % P) % P
    t = t * inv2 % P
    T = t * ((t + 1) % P) % P
    T = T * inv2 % P

    # DSU arrays (1..n), plus sentinels 0 and n+1
    used = bytearray(n + 2)
    fa = list(range(n + 2))
    sz = [0] * (n + 2)

    # Iterative find with path compression
    def find(x: int) -> int:
        while fa[x] != x:
            fa[x] = fa[fa[x]]
            x = fa[x]
        return x

    def merge(x: int, y: int) -> int:
        rx = find(x)
        ry = find(y)
        if rx == ry:
            return rx
        # attach ry -> rx (same as C++ code)
        sz[rx] += sz[ry]
        fa[ry] = rx
        return rx

    now = 0
    cc = 0
    ans = 0

    # add() exactly mirrors the C++ function
    def add(x: int) -> None:
        nonlocal now, cc
        used[x] = 1
        sz[x] = 1
        fa[x] = x  # ensure it's its own parent when first activated

        if used[x - 1]:
            r = find(x - 1)
            now = (now - f[sz[r]]) % P
            merge(x, x - 1)

        if used[x + 1]:
            r = find(x + 1)
            now = (now - f[sz[r]]) % P
            merge(x, x + 1)

        r = find(x)
        now = (now + f[sz[r]]) % P

        L = sz[find(1)]
        R = sz[find(n)]

        x0 = R if R < (L - 1) else (L - 1)  # min(R, L-1)
        if x0 <= 0:
            cc = now
            return

        # cc = now + x*L*(R+1) - x(x+1)/2*(L+R+1) + x(x+1)(2x+1)/6  (all mod P)
        x = x0
        cc_val = now
        cc_val = (cc_val + (x * L) % P * ((R + 1) % P)) % P

        tri = (x * (x + 1) // 2) % P
        cc_val = (cc_val - tri * ((L + R + 1) % P)) % P

        sqsum = (x * (x + 1) * (2 * x + 1) // 6) % P
        cc_val = (cc_val + sqsum) % P

        cc = cc_val

    # Main loop: i = 0..ma-1 (same as C++)
    for i in range(ma):
        lst = pos.get(i)
        if lst:
            for idx in lst:
                add(idx)
        ans = (ans + T - cc) % P

    print(ans % P)

if __name__ == "__main__":
    solve()
