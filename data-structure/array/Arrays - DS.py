#
# Complete the 'reverseArray' function below.
#
# The function is expected to return an INTEGER_ARRAY.
# The function accepts INTEGER_ARRAY a as parameter.
#

def reverseArray(a):
    # Write your code here
    start = 0
    end = len(a) - 1
    while start < end:
        a[start], a[end] = a[end], a[start]
        start += 1
        end -= 1
    return a
