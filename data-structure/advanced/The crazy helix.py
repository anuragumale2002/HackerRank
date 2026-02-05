# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys, random
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

class Node:
    __slots__ = ("v", "p", "l", "r", "par", "sz", "rev")
    def __init__(self, v):
        self.v = v
        self.p = random.getrandbits(31)
        self.l = None
        self.r = None
        self.par = None
        self.sz = 1
        self.rev = False

def sz(t):
    return t.sz if t else 0

def pull(t):
    t.sz = 1 + sz(t.l) + sz(t.r)
    if t.l: t.l.par = t
    if t.r: t.r.par = t

def push(t):
    if t and t.rev:
        t.rev = False
        t.l, t.r = t.r, t.l
        if t.l: t.l.rev ^= True
        if t.r: t.r.rev ^= True

def merge(a, b):
    if not a:
        if b: b.par = None
        return b
    if not b:
        a.par = None
        return a
    push(a); push(b)
    if a.p > b.p:
        a.r = merge(a.r, b)
        if a.r: a.r.par = a
        pull(a)
        a.par = None
        return a
    else:
        b.l = merge(a, b.l)
        if b.l: b.l.par = b
        pull(b)
        b.par = None
        return b

def split(t, k):
    """first k nodes go left, rest go right"""
    if not t:
        return (None, None)
    push(t)
    if sz(t.l) >= k:
        a, b = split(t.l, k)
        t.l = b
        if t.l: t.l.par = t
        pull(t)
        if a: a.par = None
        t.par = None
        return (a, t)
    else:
        a, b = split(t.r, k - sz(t.l) - 1)
        t.r = a
        if t.r: t.r.par = t
        pull(t)
        t.par = None
        if b: b.par = None
        return (t, b)

def build_initial(n):
    # Build treap from 1..n in O(n) using a stack (Cartesian tree by priority)
    nodes = [None] + [Node(i) for i in range(1, n + 1)]
    st = []
    for i in range(1, n + 1):
        cur = nodes[i]
        last = None
        while st and st[-1].p < cur.p:
            last = st.pop()
        cur.l = last
        if last: last.par = cur
        if st:
            st[-1].r = cur
            cur.par = st[-1]
        st.append(cur)

    root = st[0] if st else None

    # fix sizes (iterative postorder)
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
                pull(u)
        root.par = None

    return root, nodes

def kth(root, k):
    t = root
    while True:
        push(t)
        ls = sz(t.l)
        if k == ls + 1:
            return t
        if k <= ls:
            t = t.l
        else:
            k -= ls + 1
            t = t.r

def expose_path_to_root(x):
    stack = []
    cur = x
    while cur:
        stack.append(cur)
        cur = cur.par
    for node in reversed(stack):
        push(node)

def index_of(node):
    # make sure all lazy reversals on the path are pushed
    expose_path_to_root(node)

    res = sz(node.l) + 1
    cur = node
    while cur.par:
        p = cur.par
        # p is already pushed by expose_path_to_root, but safe:
        # push(p)
        if cur is p.r:
            res += sz(p.l) + 1
        cur = p
    return res

def reverse_range(root, l, r):
    a, bc = split(root, l - 1)
    b, c = split(bc, r - l + 1)
    if b:
        b.rev ^= True
    root = merge(a, merge(b, c))
    return root

def solve():
    n, q = map(int, input().split())
    root, nodes = build_initial(n)

    out = []
    for _ in range(q):
        parts = input().split()
        t = int(parts[0])
        if t == 1:
            A = int(parts[1]); B = int(parts[2])
            root = reverse_range(root, A, B)
        elif t == 2:
            A = int(parts[1])
            pos = index_of(nodes[A])
            out.append(f"element {A} is at position {pos}")
        else:  # t == 3
            A = int(parts[1])
            node = kth(root, A)
            out.append(f"element at position {A} is {node.v}")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
