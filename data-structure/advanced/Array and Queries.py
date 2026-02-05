import sys

MOD = 1_000_000_007

def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    it = iter(data)

    n = next(it)
    a = [next(it) for _ in range(n)]

    # frequency map
    cnt = {}
    for v in a:
        cnt[v] = cnt.get(v, 0) + 1

    def g(x: int) -> int:
        cx = cnt.get(x, 0)
        cy = cnt.get(x + 1, 0)
        return cx - cy if cx > cy else 0

    # initial F = sum over existing keys of max(0, cnt[x] - cnt[x+1])
    # (keys suffice because if cnt[x]=0 then term is 0)
    F = 0
    for x in cnt.keys():
        cx = cnt[x]
        cy = cnt.get(x + 1, 0)
        if cx > cy:
            F += cx - cy

    q = next(it)
    ans = 0

    for i in range(1, q + 1):
        idx = next(it) - 1
        newv = next(it)
        oldv = a[idx]

        if oldv != newv:
            affected = {oldv - 1, oldv, newv - 1, newv}

            before = 0
            for x in affected:
                before += g(x)

            # apply update oldv -> newv
            c = cnt.get(oldv, 0) - 1
            if c == 0:
                cnt.pop(oldv, None)
            else:
                cnt[oldv] = c

            cnt[newv] = cnt.get(newv, 0) + 1
            a[idx] = newv

            after = 0
            for x in affected:
                after += g(x)

            F += after - before

        ans = (ans + (i * (F % MOD)) ) % MOD

    print(ans % MOD)

if __name__ == "__main__":
    solve()
