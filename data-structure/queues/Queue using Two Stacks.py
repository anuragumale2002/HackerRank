# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys

def main():
    input = sys.stdin.readline
    q = int(input().strip())

    in_stack = []   # push/enqueue here
    out_stack = []  # pop/peek from here

    for _ in range(q):
        parts = input().split()
        t = int(parts[0])

        if t == 1:
            # enqueue x
            x = int(parts[1])
            in_stack.append(x)

        else:
            # make sure out_stack has the current front
            if not out_stack:
                while in_stack:
                    out_stack.append(in_stack.pop())

            if t == 2:
                # dequeue
                out_stack.pop()
            else:  # t == 3
                # print front
                print(out_stack[-1])

if __name__ == "__main__":
    main()
