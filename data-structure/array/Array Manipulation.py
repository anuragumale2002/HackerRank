#
# Complete the 'arrayManipulation' function below.
#
# The function is expected to return a LONG_INTEGER.
# The function accepts following parameters:
#  1. INTEGER n
#  2. 2D_INTEGER_ARRAY queries
#

def arrayManipulation(n, queries):
    # Write your code here
    arr = [0] * (n + 1)
    
    for query in queries:
        a, b, k = query
        arr[a] += k
        if b + 1 <= n:
            arr[b + 1] -= k
    
    max_value = 0
    current_value = 0
    
    for i in range(1, n + 1):
        current_value += arr[i]
        if current_value > max_value:
            max_value = current_value
    
    return max_value