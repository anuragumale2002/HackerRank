#
# Complete the 'hourglassSum' function below.
#
# The function is expected to return an INTEGER.
# The function accepts 2D_INTEGER_ARRAY arr as parameter.
#

def hourglassSum(arr):
    # Write your code here
    max_sum = float("-inf")
    for r in range(4):        # 0..3
        for c in range(4):    # 0..3
            hg = (
                arr[r][c] + arr[r][c+1] + arr[r][c+2]
                + arr[r+1][c+1]
                + arr[r+2][c] + arr[r+2][c+1] + arr[r+2][c+2]
            )
            max_sum = max(max_sum, hg)
    return max_sum