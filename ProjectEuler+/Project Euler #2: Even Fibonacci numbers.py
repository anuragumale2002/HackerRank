import sys

def solve():
    """
    Computes the sum of even Fibonacci numbers <= N for multiple test cases.

    ------------------------------------------------------------
    WHY THIS APPROACH?
    ------------------------------------------------------------
    Brute force generates all Fibonacci numbers up to N.
    That is unnecessary because:
        Every 3rd Fibonacci number is even.

    Instead of:
        F(n) = F(n-1) + F(n-2)

    We directly generate only EVEN Fibonacci numbers.

    ------------------------------------------------------------
    MATHEMATICAL OBSERVATION
    ------------------------------------------------------------
    Fibonacci sequence:
        1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144...

    Even terms:
        2, 8, 34, 144, ...

    These follow recurrence:
        E(n) = 4E(n-1) + E(n-2)

    Why?
    Because substituting Fibonacci relations repeatedly
    eliminates odd terms and forms this reduced recurrence.

    ------------------------------------------------------------
    HOW IT WORKS
    ------------------------------------------------------------
    1. Start with:
            E1 = 2
            E2 = 8
    2. Generate next even term using:
            next_even = 4*current + previous
    3. Stop when term exceeds N.
    4. Accumulate sum.

    Time Complexity: O(log N)
    Space Complexity: O(1)
    """

    t = int(sys.stdin.readline())

    for _ in range(t):
        n = int(sys.stdin.readline())

        # First two even Fibonacci numbers
        prev_even = 2
        curr_even = 8

        total = 0

        # Add valid even Fibonacci numbers
        while prev_even <= n:
            total += prev_even

            # Generate next even Fibonacci using:
            # E(n) = 4E(n-1) + E(n-2)
            next_even = 4 * curr_even + prev_even

            prev_even = curr_even
            curr_even = next_even

        print(total)


if __name__ == "__main__":
    solve()
