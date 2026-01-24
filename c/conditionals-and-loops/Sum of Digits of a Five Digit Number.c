#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    int n;
    scanf("%d", &n);

    // Initialize sum to 0
    int sum = 0;

    // Extract each digit and add it to sum
    sum += n % 10;  // Extract the last digit
    n /= 10;        // Remove the last digit
    sum += n % 10;  // Extract the new last digit
    n /= 10;        // Remove the last digit
    sum += n % 10;  // Continue the same process
    n /= 10;
    sum += n % 10;
    n /= 10;
    sum += n % 10;

    // Print the sum of digits
    printf("%d\n", sum);

    return 0;
}
