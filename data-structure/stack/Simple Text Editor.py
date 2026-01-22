# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys

def main():
    input = sys.stdin.readline

    Q = int(input().strip())
    s = []              # current text as list of chars
    undo = []           # stack of actions to undo

    for _ in range(Q):
        parts = input().split()
        t = parts[0]

        if t == "1":
            w = parts[1]
            s.extend(w)
            undo.append(("del", len(w)))  # undo append by deleting len(w)

        elif t == "2":
            k = int(parts[1])
            # save deleted part to undo later
            deleted = ''.join(s[-k:]) if k > 0 else ""
            del s[-k:]
            undo.append(("add", deleted))  # undo delete by adding back deleted string

        elif t == "3":
            k = int(parts[1])
            sys.stdout.write(s[k - 1] + "\n")

        else:  # t == "4" undo
            action, val = undo.pop()
            if action == "del":
                del s[-val:]
            else:  # "add"
                s.extend(val)

if __name__ == "__main__":
    main()
