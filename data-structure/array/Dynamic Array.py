#
# Complete the 'dynamicArray' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts following parameters:
#  1. INTEGER n
#  2. 2D_INTEGER_ARRAY queries
#

def dynamicArray(n, queries):
    # Write your code here
    seqList = [[] for _ in range(n)]
    lastAnswer = 0
    answers = []

    for q in queries:
        t, x, y = q
        idx = (x ^ lastAnswer) % n

        if t == 1:
            seqList[idx].append(y)
        else:  # t == 2
            seq = seqList[idx]
            lastAnswer = seq[y % len(seq)]
            answers.append(lastAnswer)

    return answers