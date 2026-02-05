import sys, random, math
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

# -------------------------
# Implicit Treap (rope)
# -------------------------
class Node:
    __slots__ = ("v", "p", "sz", "l", "r", "rev")
    def __init__(self, v):
        self.v = v
        self.p = random.getrandbits(31)
        self.sz = 1
        self.l = None
        self.r = None
        self.rev = False

def _sz(t): return t.sz if t else 0

def _pull(t):
    t.sz = 1 + _sz(t.l) + _sz(t.r)

def _push(t):
    if t and t.rev:
        t.rev = False
        t.l, t.r = t.r, t.l
        if t.l: t.l.rev ^= True
        if t.r: t.r.rev ^= True

def merge(a, b):
    if not a: return b
    if not b: return a
    _push(a); _push(b)
    if a.p > b.p:
        a.r = merge(a.r, b)
        _pull(a)
        return a
    else:
        b.l = merge(a, b.l)
        _pull(b)
        return b

def split(t, k):
    """split by first k elements: returns (a,b)"""
    if not t: return (None, None)
    _push(t)
    if _sz(t.l) >= k:
        a, b = split(t.l, k)
        t.l = b
        _pull(t)
        return (a, t)
    else:
        a, b = split(t.r, k - _sz(t.l) - 1)
        t.r = a
        _pull(t)
        return (t, b)

def build_treap(arr):
    # O(n) Cartesian build by random priorities
    st = []
    nodes = [Node(v) for v in arr]
    for nd in nodes:
        last = None
        while st and st[-1].p < nd.p:
            last = st.pop()
        if st:
            st[-1].r = nd
        nd.l = last
        st.append(nd)
    root = st[0] if st else None
    # fix sizes
    if root:
        stack = [(root, 0)]
        while stack:
            u, state = stack.pop()
            if not u: continue
            if state == 0:
                stack.append((u, 1))
                stack.append((u.r, 0))
                stack.append((u.l, 0))
            else:
                _pull(u)
    return root

def inorder_collect(t, out):
    stack = []
    cur = t
    while cur or stack:
        while cur:
            _push(cur)
            stack.append(cur)
            cur = cur.l
        cur = stack.pop()
        out.append(cur.v)
        cur = cur.r

# -------------------------
# Minimum Enclosing Circle
# -------------------------
EPS = 1e-10

def is_in_circle(c, p):
    cx, cy, r = c
    dx = p[0] - cx
    dy = p[1] - cy
    return dx*dx + dy*dy <= r*r + 1e-9

def circle_from_1(p):
    return (p[0], p[1], 0.0)

def circle_from_2(a, b):
    cx = (a[0] + b[0]) / 2.0
    cy = (a[1] + b[1]) / 2.0
    r = math.hypot(a[0] - b[0], a[1] - b[1]) / 2.0
    return (cx, cy, r)

def circle_from_3(a, b, c):
    ax, ay = a
    bx, by = b
    cx, cy = c
    d = 2.0 * (ax*(by-cy) + bx*(cy-ay) + cx*(ay-by))
    if abs(d) < EPS:
        return None
    ax2ay2 = ax*ax + ay*ay
    bx2by2 = bx*bx + by*by
    cx2cy2 = cx*cx + cy*cy
    ux = (ax2ay2*(by-cy) + bx2by2*(cy-ay) + cx2cy2*(ay-by)) / d
    uy = (ax2ay2*(cx-bx) + bx2by2*(ax-cx) + cx2cy2*(bx-ax)) / d
    r = math.hypot(ux-ax, uy-ay)
    return (ux, uy, r)

def min_enclosing_circle(points):
    pts = points[:]
    random.shuffle(pts)

    c = None
    for i, p in enumerate(pts):
        if c is not None and is_in_circle(c, p):
            continue
        c = circle_from_1(p)
        for j in range(i):
            q = pts[j]
            if is_in_circle(c, q):
                continue
            c = circle_from_2(p, q)
            for k in range(j):
                r = pts[k]
                if is_in_circle(c, r):
                    continue
                cc = circle_from_3(p, q, r)
                if cc is None:
                    # collinear: smallest circle from farthest pair
                    cands = [circle_from_2(p, q), circle_from_2(p, r), circle_from_2(q, r)]
                    best = None
                    for cand in cands:
                        if is_in_circle(cand, p) and is_in_circle(cand, q) and is_in_circle(cand, r):
                            if best is None or cand[2] < best[2]:
                                best = cand
                    c = best
                else:
                    c = cc
    return c

# -------------------------
# Operations
# -------------------------
def reverse_range(root, l, r):
    a, bc = split(root, l-1)
    b, c = split(bc, r-l+1)
    if b: b.rev ^= True
    return merge(a, merge(b, c))

def swap_segments_same_array(root, l1, r1, l2, r2):
    # Swap two disjoint segments in the SAME array (can have a gap)
    if l1 > l2:
        l1, l2 = l2, l1
        r1, r2 = r2, r1
    # assume disjoint: r1 < l2
    pre, rest = split(root, l1 - 1)
    seg1, rest = split(rest, r1 - l1 + 1)
    mid, rest = split(rest, l2 - r1 - 1)   # gap between seg1 and seg2 (could be empty)
    seg2, suf = split(rest, r2 - l2 + 1)
    return merge(pre, merge(seg2, merge(mid, merge(seg1, suf))))

def swap_between(a_root, b_root, l, r):
    a1, a_mid_suf = split(a_root, l-1)
    a_mid, a3 = split(a_mid_suf, r-l+1)
    b1, b_mid_suf = split(b_root, l-1)
    b_mid, b3 = split(b_mid_suf, r-l+1)
    a_root = merge(a1, merge(b_mid, a3))
    b_root = merge(b1, merge(a_mid, b3))
    return a_root, b_root

def extract_segment(root, l, r):
    pre, mid_suf = split(root, l-1)
    mid, suf = split(mid_suf, r-l+1)
    arr = []
    inorder_collect(mid, arr)
    root = merge(pre, merge(mid, suf))
    return root, arr

# -------------------------
# Main
# -------------------------
def main():
    n, q = map(int, input().split())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))

    a_root = build_treap(A)
    b_root = build_treap(B)

    out = []
    for _ in range(q):
        parts = list(map(int, input().split()))
        t = parts[0]

        if t == 1:
            # 1 p l r : reverse in array p (0=A, 1=B)
            p, l, r = parts[1], parts[2], parts[3]
            if p == 0:
                a_root = reverse_range(a_root, l, r)
            else:
                b_root = reverse_range(b_root, l, r)

        elif t == 2:
            # 2 p l1 r1 l2 r2 : swap two disjoint fragments (NOT necessarily consecutive)
            p, l1, r1, l2, r2 = parts[1], parts[2], parts[3], parts[4], parts[5]
            if p == 0:
                a_root = swap_segments_same_array(a_root, l1, r1, l2, r2)
            else:
                b_root = swap_segments_same_array(b_root, l1, r1, l2, r2)

        elif t == 3:
            # 3 l r : swap A[l..r] with B[l..r]
            l, r = parts[1], parts[2]
            a_root, b_root = swap_between(a_root, b_root, l, r)

        else:
            # 4 l r : MEC radius of points (A[i], B[i])
            l, r = parts[1], parts[2]
            a_root, xs = extract_segment(a_root, l, r)
            b_root, ys = extract_segment(b_root, l, r)
            pts = list(zip(xs, ys))
            if len(pts) <= 1:
                out.append("0.00")
            else:
                c = min_enclosing_circle(pts)
                out.append(f"{c[2]:.2f}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()


# Timedout 