import sys
from functools import cmp_to_key

MOD = 1_000_000_007
B = 100001

# ---------- Suffix Array (O(n log n)) with radix/counting sort ----------
def build_sa(s: str):
    n = len(s)
    if n == 0:
        return [], [], []

    # initial ranks by character (lowercase)
    rk = [ord(c) - 97 for c in s]
    sa = list(range(n))
    tmp = [0] * n

    k = 1
    maxv = max(rk) + 1

    def counting_sort(key, max_key):
        cnt = [0] * (max_key + 1)
        for i in range(n):
            cnt[key[i]] += 1
        ssum = 0
        for i in range(max_key + 1):
            cnt[i], ssum = ssum, ssum + cnt[i]
        out = [0] * n
        for idx in sa:
            out[cnt[key[idx]]] = idx
            cnt[key[idx]] += 1
        return out

    while True:
        # second key: rank[i+k] else -1 -> shift by +1 to make non-negative
        key2 = [rk[i + k] + 1 if i + k < n else 0 for i in range(n)]
        sa = counting_sort(key2, maxv)  # maxv is enough because key2 in [0..maxv]
        # first key: rank[i] in [0..maxv-1]
        key1 = rk
        sa = counting_sort(key1, maxv - 1)

        tmp[sa[0]] = 0
        classes = 1
        for i in range(1, n):
            a, b = sa[i - 1], sa[i]
            prev = (rk[a], rk[a + k] if a + k < n else -1)
            curr = (rk[b], rk[b + k] if b + k < n else -1)
            if curr != prev:
                classes += 1
            tmp[b] = classes - 1
        rk, tmp = tmp, rk
        if classes == n:
            break
        maxv = classes
        k <<= 1

    inv = [0] * n
    for i, p in enumerate(sa):
        inv[p] = i

    # Kasai LCP: lcp[i] = LCP(sa[i], sa[i+1])
    lcp = [0] * (n - 1)
    h = 0
    for i in range(n):
        r = inv[i]
        if r == n - 1:
            h = 0
            continue
        j = sa[r + 1]
        while i + h < n and j + h < n and s[i + h] == s[j + h]:
            h += 1
        lcp[r] = h
        if h:
            h -= 1

    return sa, inv, lcp

# ---------- RMQ Sparse Table for LCP ----------
class RMQ:
    __slots__ = ("st", "lg")
    def __init__(self, arr):
        n = len(arr)
        self.lg = [0] * (n + 1)
        for i in range(2, n + 1):
            self.lg[i] = self.lg[i >> 1] + 1
        if n == 0:
            self.st = []
            return
        k = self.lg[n] + 1
        st = [arr[:]]
        j = 1
        while (1 << j) <= n:
            prev = st[j - 1]
            span = 1 << (j - 1)
            cur = [0] * (n - (1 << j) + 1)
            for i in range(len(cur)):
                a = prev[i]
                b = prev[i + span]
                cur[i] = a if a < b else b
            st.append(cur)
            j += 1
        self.st = st

    def query(self, l, r):
        # min on [l, r] inclusive
        if l > r:
            return 10**9
        j = self.lg[r - l + 1]
        a = self.st[j][l]
        b = self.st[j][r - (1 << j) + 1]
        return a if a < b else b

# ---------- Eertree (Palindromic Tree) ----------
def eertree_build(s: str):
    n = len(s)
    # node 0: len=-1, node 1: len=0
    nxt = [[-1]*26, [-1]*26]
    link = [0, 0]
    length = [-1, 0]
    occ = [0, 0]
    endpos = [-1, -1]
    suff = 1

    for i, ch in enumerate(s):
        c = ord(ch) - 97
        cur = suff
        while True:
            L = length[cur]
            if i - 1 - L >= 0 and s[i] == s[i - 1 - L]:
                break
            cur = link[cur]

        if nxt[cur][c] != -1:
            suff = nxt[cur][c]
            occ[suff] += 1
            continue

        # create new node
        new = len(length)
        length.append(length[cur] + 2)
        link.append(0)
        occ.append(1)
        endpos.append(i)
        nxt.append([-1]*26)

        nxt[cur][c] = new

        if length[new] == 1:
            link[new] = 1
            suff = new
            continue

        cand = link[cur]
        while True:
            L = length[cand]
            if i - 1 - L >= 0 and s[i] == s[i - 1 - L]:
                break
            cand = link[cand]
        link[new] = nxt[cand][c]
        suff = new

    # propagate occurrence counts by decreasing length
    nodes = list(range(2, len(length)))
    nodes.sort(key=lambda x: length[x], reverse=True)
    for v in nodes:
        occ[link[v]] += occ[v]

    return length, link, occ, endpos, nxt

# ---------- Main solve ----------
def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    q = int(data[1])
    s = data[2].decode()
    queries = list(map(int, data[3:]))

    # Precompute powB, invpowB, prefix hash H[i] = sum ord(s[j]) * B^j for j < i
    powB = [1] * (n + 1)
    for i in range(1, n + 1):
        powB[i] = (powB[i - 1] * B) % MOD
    invB = pow(B, MOD - 2, MOD)
    invpowB = [1] * (n + 1)
    for i in range(1, n + 1):
        invpowB[i] = (invpowB[i - 1] * invB) % MOD

    H = [0] * (n + 1)
    for i, ch in enumerate(s):
        H[i + 1] = (H[i] + ord(ch) * powB[i]) % MOD

    def substring_f(l, r):
        # f(s[l..r]) = sum ord(s[l+t]) * B^t
        raw = (H[r + 1] - H[l]) % MOD
        return (raw * invpowB[l]) % MOD

    # Build structures
    sa, inv, lcp = build_sa(s)
    rmq = RMQ(lcp)

    length, link, occ, endpos, nxt = eertree_build(s)

    # Collect distinct palindromes (excluding two roots)
    pals = []
    for v in range(2, len(length)):
        L = length[v]
        r = endpos[v]
        l = r - L + 1
        pals.append((l, L, occ[v]))  # start, len, frequency

    # Comparator using SA+LCP
    s_local = s
    inv_local = inv
    rmq_local = rmq

    def cmp_pal(a, b):
        i1, l1, _c1 = a
        i2, l2, _c2 = b
        if i1 == i2:
            return -1 if l1 < l2 else (1 if l1 > l2 else 0)

        r1 = inv_local[i1]
        r2 = inv_local[i2]
        swapped = False
        if r1 > r2:
            r1, r2 = r2, r1
            i1, i2 = i2, i1
            l1, l2 = l2, l1
            swapped = True

        # LCP of suffixes at ranks r1 and r2:
        common = rmq_local.query(r1, r2 - 1)
        mlen = l1 if l1 < l2 else l2
        if common >= mlen:
            # shorter substring is smaller
            res = -1 if l1 < l2 else (1 if l1 > l2 else 0)
        else:
            c1 = s_local[i1 + common]
            c2 = s_local[i2 + common]
            res = -1 if c1 < c2 else (1 if c1 > c2 else 0)

        return -res if swapped else res

    pals.sort(key=cmp_to_key(cmp_pal))

    # Prefix counts over multiplicities
    pref = [0] * (len(pals) + 1)
    for i, (_, _, c) in enumerate(pals, 1):
        pref[i] = pref[i - 1] + c
    total = pref[-1]

    out = []
    for k in queries:
        if k > total:
            out.append("-1")
            continue
        # find smallest idx with pref[idx] >= k
        lo, hi = 1, len(pals)
        while lo < hi:
            mid = (lo + hi) >> 1
            if pref[mid] >= k:
                hi = mid
            else:
                lo = mid + 1
        l, L, _c = pals[lo - 1]
        out.append(str(substring_f(l, l + L - 1)))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    solve()
