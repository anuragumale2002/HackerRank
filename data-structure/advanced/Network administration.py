import sys
sys.setrecursionlimit(1_000_000)
input = sys.stdin.readline

# ----------------------------
# Link-Cut Tree (Splay-based)
# ----------------------------
class LCTNode:
    __slots__ = ("l", "r", "p", "rev", "val", "sm")
    def __init__(self, val=0):
        self.l = None
        self.r = None
        self.p = None
        self.rev = False
        self.val = val
        self.sm = val

def _sm(x):
    return x.sm if x else 0

def _pull(x):
    x.sm = x.val + _sm(x.l) + _sm(x.r)

def _push(x):
    if x and x.rev:
        x.rev = False
        x.l, x.r = x.r, x.l
        if x.l: x.l.rev ^= True
        if x.r: x.r.rev ^= True

def _is_root(x):
    p = x.p
    return (p is None) or (p.l is not x and p.r is not x)

def _rotate(x):
    p = x.p
    g = p.p
    _push(p); _push(x)
    if p.l is x:
        b = x.r
        x.r = p
        p.l = b
        if b: b.p = p
    else:
        b = x.l
        x.l = p
        p.r = b
        if b: b.p = p
    p.p = x
    x.p = g
    if g:
        if g.l is p:
            g.l = x
        elif g.r is p:
            g.r = x
    _pull(p)
    _pull(x)

def _splay(x):
    _push(x)
    while not _is_root(x):
        p = x.p
        g = p.p
        if not _is_root(p):
            if (g.l is p) == (p.l is x):
                _rotate(p)
            else:
                _rotate(x)
        _rotate(x)

def access(x):
    last = None
    y = x
    while y:
        _splay(y)
        y.r = last
        _pull(y)
        last = y
        y = y.p
    _splay(x)

def makeroot(x):
    access(x)
    x.rev ^= True
    _push(x)

def findroot(x):
    access(x)
    while True:
        _push(x)
        if not x.l:
            break
        x = x.l
    _splay(x)
    return x

def connected(x, y):
    if x is y:
        return True
    return findroot(x) is findroot(y)

def link(x, y):
    makeroot(x)
    # assumes x and y are in different trees
    x.p = y

def cut(x, y):
    makeroot(x)
    access(y)
    # now x should be y.l if edge exists directly in represented tree
    if y.l is x:
        y.l.p = None
        y.l = None
        _pull(y)

def path_sum(x, y):
    makeroot(x)
    access(y)
    return y.sm

# ----------------------------
# Problem handling
# ----------------------------
class EdgeRec:
    __slots__ = ("u", "v", "admin", "node")
    def __init__(self, u, v, admin, node):
        self.u = u
        self.v = v
        self.admin = admin
        self.node = node  # LCTNode for this physical link (stores devices)

def solve():
    n, l, m, t = map(int, input().split())

    # physical edges map: (min(u,v), max(u,v)) -> EdgeRec
    edges = {}

    # nodes for (admin, server): sparse created as needed
    # key = (admin << 20) + server (since n up to big; 20 bits enough for 1e6; still safe)
    # if you worry about n > 1e6, switch key to tuple.
    def key(a, u):
        return (a << 20) ^ u

    node_map = {}  # key -> LCTNode(server with val=0)
    deg = {}       # key -> degree under that admin (0..2)

    def get_server_node(a, u):
        k = key(a, u)
        nd = node_map.get(k)
        if nd is None:
            nd = LCTNode(0)
            node_map[k] = nd
            # deg default 0
        return nd

    def get_deg(a, u):
        return deg.get(key(a, u), 0)

    def inc_deg(a, u, delta):
        k = key(a, u)
        deg[k] = deg.get(k, 0) + delta
        if deg[k] == 0:
            # optional cleanup
            del deg[k]

    # read initial links
    for _ in range(l):
        u, v, a = map(int, input().split())
        if u > v:
            u, v = v, u
        e_node = LCTNode(0)  # stores devices on this link
        rec = EdgeRec(u, v, a, e_node)
        edges[(u, v)] = rec

        su = get_server_node(a, u)
        sv = get_server_node(a, v)
        # link su - e - sv
        link(su, e_node)
        link(e_node, sv)
        inc_deg(a, u, 1)
        inc_deg(a, v, 1)

    out = []

    for _ in range(t):
        parts = input().split()
        typ = int(parts[0])

        if typ == 1:
            # 1 X Y A : reassign edge (X,Y) to administrator A
            x = int(parts[1]); y = int(parts[2]); a_new = int(parts[3])
            u, v = (x, y) if x < y else (y, x)
            rec = edges.get((u, v))
            if rec is None:
                out.append("Wrong link")
                continue
            if rec.admin == a_new:
                out.append("Already controlled link")
                continue

            # overload check
            if get_deg(a_new, u) >= 2 or get_deg(a_new, v) >= 2:
                out.append("Server overload")
                continue

            # redundancy check (cycle) in new admin forest
            # if u or v node doesn't exist yet for this admin => can't be connected
            ku = key(a_new, u)
            kv = key(a_new, v)
            if ku in node_map and kv in node_map:
                if connected(node_map[ku], node_map[kv]):
                    out.append("Network redundancy")
                    continue

            # perform reassignment: cut from old admin
            a_old = rec.admin
            e_node = rec.node

            su_old = get_server_node(a_old, u)
            sv_old = get_server_node(a_old, v)
            cut(su_old, e_node)
            cut(e_node, sv_old)
            inc_deg(a_old, u, -1)
            inc_deg(a_old, v, -1)

            # link into new admin
            su_new = get_server_node(a_new, u)
            sv_new = get_server_node(a_new, v)
            link(su_new, e_node)
            link(e_node, sv_new)
            inc_deg(a_new, u, 1)
            inc_deg(a_new, v, 1)

            rec.admin = a_new
            out.append("Assignment done")

        elif typ == 2:
            # 2 X Y D : set devices on link (X,Y) to D (link always exists per statement)
            x = int(parts[1]); y = int(parts[2]); d = int(parts[3])
            u, v = (x, y) if x < y else (y, x)
            rec = edges.get((u, v))
            # statement says it will always exist, but stay safe
            if rec is None:
                continue
            e_node = rec.node
            access(e_node)
            e_node.val = d
            _pull(e_node)

        else:
            # 3 X Y A : query devices along path between X and Y using only admin A links
            x = int(parts[1]); y = int(parts[2]); a = int(parts[3])
            if x == y:
                out.append("0 security devices placed")
                continue
            kx = key(a, x)
            ky = key(a, y)
            if kx not in node_map or ky not in node_map:
                out.append("No connection")
                continue
            nx = node_map[kx]
            ny = node_map[ky]
            if not connected(nx, ny):
                out.append("No connection")
            else:
                s = path_sum(nx, ny)  # includes server nodes (0) + edge nodes (devices)
                out.append(f"{s} security devices placed")

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
