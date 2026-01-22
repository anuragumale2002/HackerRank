# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys
import heapq

def main():
    input = sys.stdin.readline

    q = int(input().strip())
    heap = []
    deleted = set()
    out = []

    for _ in range(q):
        parts = input().split()
        t = int(parts[0])

        if t == 1:
            v = int(parts[1])
            heapq.heappush(heap, v)

        elif t == 2:
            v = int(parts[1])
            deleted.add(v)

        else:  # t == 3
            while heap and heap[0] in deleted:
                deleted.remove(heap[0])
                heapq.heappop(heap)
            out.append(str(heap[0]))

    sys.stdout.write("\n".join(out))

if __name__ == "__main__":
    main()
