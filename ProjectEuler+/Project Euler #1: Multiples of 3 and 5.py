# Project Euler #1
# Time Complexity: O(1) per test case
# Space Complexity: O(1)

import sys

def sum_of_multiples(n, d):
    """
    Returns sum of all multiples of d below n.

    Derivation:
    Multiples of d below n:
        d, 2d, 3d, ..., kd

    where:
        k = floor((n-1) / d)

    This is an Arithmetic Progression:
        Sum = d * (1 + 2 + ... + k)

    We know:
        1 + 2 + ... + k = k(k+1)/2

    Therefore:
        Sum = d * k(k+1)/2
    """
    k = (n - 1) // d   # number of multiples below n
    return d * k * (k + 1) // 2

def solve():
    t = int(sys.stdin.readline().strip())
    
    for _ in range(t):
        n = int(sys.stdin.readline().strip())
        
        # Inclusion-Exclusion Principle
        result = (
            sum_of_multiples(n, 3)
            + sum_of_multiples(n, 5)
            - sum_of_multiples(n, 15)
        )
        
        print(result)

if __name__ == "__main__":
    solve()
