# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys

def main():
    input = sys.stdin.readline

    n, q = map(int, input().split())
    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        # union by size
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    out = []
    for _ in range(q):
        parts = input().split()
        if parts[0] == 'M':
            union(int(parts[1]), int(parts[2]))
        else:  # 'Q'
            out.append(str(size[find(int(parts[1]))]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
