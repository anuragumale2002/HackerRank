from collections import Counter
from bisect import bisect_left
import sys
input = sys.stdin.readline
inf = 10**18


def read(dtype=int):
    return list(map(dtype, input().split()))


p, q = read()
P = p
a = list(map(int, input().strip()))
n = len(a)


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x, y = egcd(b % a, a)
    return g, y - b//a*x, x


def modularInverse(a, m):
    # find x such that a * x % m == 1
    g, x, _ = egcd(a, m)
    if g ^ 1:
        print("No solution")
        return -1
    return x % m

cum = [0]
cnt_2 = cnt_5 = 0

while p % 2 == 0:
    cnt_2 += 1
    p //= 2

while p % 5 == 0:
    cnt_5 += 1
    p //= 5

if p == 1:
    inv_10 = 0
else:
    inv_10 = modularInverse(10,p)

curr = inv_10 


num = 0
for i, j in enumerate(a, 1):
    num = (num * 10 + j) % p
    cum.append(num * curr % p)
    curr = curr * inv_10 % p

notify = [[] for _ in range(n+1)]

ask = []

B = 8
magic = (1 << B) - 1
res = [0] * q

zip = sorted(set(cum))


for i, j in enumerate(cum):
    cum[i] = bisect_left(zip, j)

dp = [[0] * (1 << B) for _ in range(n+1)]

for i in range(n+1):
    curr = 0
    for k in range(1, 1<<B):
        if i + k > n:
            break
        curr = (curr * 10 + a[i+k-1]) % P
        dp[i][k] = dp[i][k-1] + (curr == 0)


L = max(cnt_2, cnt_5) + 1

cum_L = [0] * (n+2)

for i in range(n+1):
    cum_L[i] = cum_L[i-1] + dp[i][L]

ask = [None] * q

def brute(l,r):
    res = 0
    cnt = Counter()
    for i in range(l,r+1):
        res += cnt[cum[i]]
        cnt[cum[i]] += 1
    # print(cnt)
    return res

for idx in range(q):
    l, r = read()
    if (l-1) >> B == r >> B:
        for i in range(l, r+1):
            res[idx] += dp[i-1][r-i+1]
    else:
        for j in range(r, l-1, -1):
            if r - j + 1 < L:
                res[idx] += dp[j-1][r-j+1]
            else:
                res[idx] += cum_L[j-1] - cum_L[l-2]
                break

        ask[idx] = l-1,r
        notify[l-1].append(idx)

for x in notify:
    x.sort(key=lambda i : ask[i][1])

K = len(zip)

good = [0] * (n+1)

trailling = 2 ** cnt_2 * 5 ** cnt_5

for i in range(n-L+1):
    curr = 0
    for j in range(i, i+L):
        curr = (curr * 10 + a[j]) % trailling
    good[i+L] = curr == 0

cnt = [0] * K
tmp = [0] * K



L += 1
for i in range(n >> B << B, -1, -(1<<B)):
    add = 0 
    for j in range(K):
        cnt[j] = tmp[j] = 0
    for j in range(i, -1, -1):
        if j + L <= i and good[j+L]:
            tmp[cum[j+L]] += 1
        add += tmp[cum[j]]
        cnt[cum[j]] += 1
        while notify[j] and ask[notify[j][-1]][1] >= i:
            restore = []
            it = notify[j].pop()
            l, r = ask[it]
            res[it] += add
            for k in range(L):
                if i - k < j:
                    break
                cnt[cum[i-k]] -= 1
                restore.append((cum[i-k], 1))
            for k in range(i+1, r+1):
                if k - L >= j:
                    cnt[cum[k-L]] += 1
                    restore.append((cum[k-L], -1))
                if good[k]:
                    res[it] += cnt[cum[k]]
            for u, v in restore:
                cnt[u] += v


print(*res, sep="\n")



# Workes in pypy envireonment