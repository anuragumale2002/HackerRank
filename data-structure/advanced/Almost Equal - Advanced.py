#!/usr/bin/env python3
import sys
import random

# ---------------- Fenwick (BIT) ----------------
def bit_add(bit, x, delta):
    n = len(bit) - 1
    while x <= n:
        bit[x] += delta
        x += x & -x

def bit_sum(bit, x):
    s = 0
    while x > 0:
        s += bit[x]
        x -= x & -x
    return s

# ---------------- Treap (ordered set) ----------------
class TNode:
    __slots__ = ("key", "prio", "l", "r")
    def __init__(self, key):
        self.key = key
        self.prio = random.randint(1, 1 << 30)
        self.l = None
        self.r = None

def split(root, key):
    """Split by key: left has keys < key, right has keys >= key."""
    if root is None:
        return (None, None)
    if root.key < key:
        a, b = split(root.r, key)
        root.r = a
        return (root, b)
    else:
        a, b = split(root.l, key)
        root.l = b
        return (a, root)

def merge(a, b):
    """Merge two treaps where all keys in a < all keys in b."""
    if a is None:
        return b
    if b is None:
        return a
    if a.prio > b.prio:
        a.r = merge(a.r, b)
        return a
    else:
        b.l = merge(a, b.l)
        return b

def insert(root, key):
    """Insert key (assumes unique)."""
    n = TNode(key)
    if root is None:
        return n
    a, b = split(root, key)
    return merge(merge(a, n), b)

def inorder_iter(root):
    st = []
    cur = root
    while cur or st:
        while cur:
            st.append(cur)
            cur = cur.l
        cur = st.pop()
        yield cur.key
        cur = cur.r

def iter_range(root, lo, hi):
    """
    Yield keys in [lo, hi] in ascending order, without destroying treap.
    Implemented via split/split/merge.
    """
    a, bc = split(root, lo)
    b, c = split(bc, (hi[0], hi[1] + 1))  # hi inclusive, so split at hi+epsilon using tuple trick
    # traverse b
    for key in inorder_iter(b):
        yield key
    # restore
    root = merge(a, merge(b, c))
    return root  # note: caller must capture if it wants the restored root

# Because Python generators can't "return root" in a usable way without StopIteration value,
# we implement a helper that returns (new_root, list_of_keys) for the needed loop.
def collect_range(root, lo, hi):
    a, bc = split(root, lo)
    # hi is inclusive; split at (hi_height, hi_idx+1) to include all (hi_height, hi_idx)
    b, c = split(bc, (hi[0], hi[1] + 1))
    keys = list(inorder_iter(b))
    root = merge(a, merge(b, c))
    return root, keys

# ---------------- Main logic (ported from your friend's code) ----------------
def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)

    n = int(next(it))
    k = int(next(it))
    heights = [int(next(it)) for _ in range(n)]

    q = int(next(it))
    queries = []
    for i in range(q):
        start = int(next(it))
        end = int(next(it))
        # If input is 1-based, uncomment:
        # start -= 1; end -= 1
        queries.append([i, start, end, 0])

    # sort by end
    queries.sort(key=lambda x: x[2])

    root = None
    bit = [0] * (n + 1)

    i = 0
    j = 0

    # For determinism across runs (optional)
    random.seed(123456789)

    while i < n:
        high_limit = (heights[i] + 2 * k + 1, 0)
        low_limit = (heights[i] - 2 * k, 0)

        # tree.higher_or_eq(low_limit, high_limit) >= high_limit equivalent:
        # find the smallest key >= low_limit and compare with high_limit.
        # We'll do this by splitting.
        if root is None:
            ge = None
        else:
            a, b = split(root, low_limit)
            # smallest in b is leftmost
            cur = b
            while cur and cur.l:
                cur = cur.l
            ge = cur.key if cur else None
            root = merge(a, b)

        cond = (ge is None) or (ge >= high_limit)

        if cond:
            seg_start = i
            seg_min = seg_max = heights[i]
            i += 1

            while i < n:
                hi = heights[i]
                if seg_max - hi > k or hi - seg_min > k:
                    break
                if hi > seg_max:
                    seg_max = hi
                if hi < seg_min:
                    seg_min = hi
                i += 1

            query_end = bit_sum(bit, seg_start)

            # Update BIT and treap for x in [seg_start .. i-2]
            # (the last element i-1 is inserted after answering queries, matching friend code)
            for x in range(seg_start, i - 1):
                root = insert(root, (heights[x], x))
                bit_add(bit, x + 1, i - x - 1)

            # Answer queries with end < i
            while j < q and queries[j][2] < i:
                if queries[j][1] < seg_start:
                    queries[j][3] = query_end - bit_sum(bit, queries[j][1])

                diff = queries[j][2] - max(seg_start, queries[j][1])
                queries[j][3] += diff * (diff + 1) // 2
                j += 1

            # insert last element of segment
            root = insert(root, (heights[i - 1], i - 1))

        else:
            limit = heights[i] + k
            lo = (heights[i] - k, -1)
            hi = (limit, 10**18)

            root, keys = collect_range(root, lo, hi)
            # For each (height, x) in range, do update_bit(bit, x+1, 1)
            for _h, x in keys:
                bit_add(bit, x + 1, 1)

            if j < q and queries[j][2] == i:
                query_end = bit_sum(bit, queries[j][2] + 1)
                while j < q and queries[j][2] == i:
                    queries[j][3] = query_end - bit_sum(bit, queries[j][1])
                    j += 1

            root = insert(root, (heights[i], i))
            i += 1

    queries.sort(key=lambda x: x[0])
    sys.stdout.write("\n".join(str(x[3]) for x in queries))

if __name__ == "__main__":
    solve()
