import sys

input = sys.stdin.readline

CAP = 10**19  # big enough cap for comparisons

# countSumms[m] = number of "side" permutations for odd n where m = n//2
# Recurrence (matches accepted solutions):
# countSumms[1]=2
# countSumms[i] = 2*countSumms[i-1] + 2^(i-2) for i>=2
countSumms = [0, 2]
def ensure_count(m: int):
    while len(countSumms) <= m:
        i = len(countSumms)
        val = 2 * countSumms[i - 1] + (1 << (i - 2))
        if val > CAP:
            val = CAP
        countSumms.append(val)

def solveRadius(n: int, k: int, radius: int, arr: list, mn: int):
    # fills outer positions based on bits of k
    left = n - (radius << 1) - 1
    right = n - 1
    mn2 = mn + 2
    for i in range(radius):
        nxt = 1 << (radius - i - 1)
        if k < nxt:
            arr[left] = mn2 + i
            arr[left + 1] = 2 + i
            left += 2
        else:
            k -= nxt
            arr[right] = mn2 + i
            arr[right - 1] = 2 + i
            right -= 2
    arr[left] = mn2 + radius

def solveSide(arr: list, n: int, k: int, mn: int):
    # Builds permutations in the "side" region (odd n)
    cache = [False] * (n + 1)
    ix = 0

    while True:
        if k == 0:
            arr[ix] = 1
            ix += 1
            for i in range(mn + 1, 1, -1):
                if not cache[i]:
                    arr[ix] = i
                    arr[ix + 1] = i + mn
                    ix += 2
            return

        if k == 1:
            left = 1
            right = mn + 2
            end = n - 1
            while ix < end:
                while cache[left]:
                    left += 1
                while cache[right]:
                    right += 1
                arr[ix] = left
                arr[ix + 1] = right
                ix += 2
                left += 1
                right += 1
            arr[ix] = mn + 1
            return

        # skip first two cases
        k -= 2  # countSumms[1]

        nxt = 1
        i = 0
        j = 2
        while True:
            ensure_count(i + 1)
            if k < countSumms[i + 1]:
                arr[ix] = j
                arr[ix + 1] = j + mn
                ix += 2
                cache[j] = True
                cache[j + mn] = True
                break

            k -= countSumms[i + 1]

            if k < nxt:
                left = j
                right = mn + left + 1
                while True:
                    while cache[left]:
                        left += 1
                    if left == mn + 1:
                        break
                    while cache[right]:
                        right += 1
                    arr[ix] = left
                    arr[ix + 1] = right
                    ix += 2
                    left += 1
                    right += 1

                # close the chain and fill radius
                arr[ix] = left
                arr[ix + 1] = 1
                ix += 2
                solveRadius(n, k, i, arr, mn)
                return

            k -= nxt
            i += 1
            j += 1
            nxt <<= 1

def solve_one(n: int, k1: int):
    if n == 1:
        return [1] if k1 == 1 else None

    mn = n >> 1  # floor(n/2)

    # even n: exactly 2 permutations
    if (n & 1) == 0:
        if k1 == 1:
            res = []
            for i in range(mn):
                res.append(mn - i)
                res.append(n - i)
            return res
        if k1 == 2:
            res = []
            for i in range(mn):
                res.append(mn + i + 1)
                res.append(i + 1)
            return res
        return None

    # odd n:
    ensure_count(mn)
    sideCount = countSumms[mn]
    midCount = 1 << mn  # 2^mn

    k = k1 - 1  # 0-based
    flip = False
    middle = False

    if k < sideCount:
        pass
    elif k < sideCount + midCount:
        k -= sideCount
        middle = True
    elif k < (sideCount << 1) + midCount:
        # mirror region
        k = abs(k - (sideCount << 1) - midCount + 1)
        flip = True
    else:
        return None

    arr = [0] * n

    if middle:
        arr[0] = mn + 1
        arr[1] = 1
        if k >= (midCount >> 1):
            k = midCount - 1 - k
            flip = True
        solveRadius(n, k, mn - 1, arr, mn)
    else:
        solveSide(arr, n, k, mn)

    if flip:
        nn1 = n + 1
        for i in range(n):
            arr[i] = nn1 - arr[i]

    return arr

def main():
    t = int(input().strip())
    out = []
    for _ in range(t):
        n, k = map(int, input().split())
        ans = solve_one(n, k)
        if ans is None:
            out.append("-1")
        else:
            out.append(" ".join(map(str, ans)))
    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
