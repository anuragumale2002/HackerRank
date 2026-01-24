#include <stdio.h>

int main() {
    int n, i, j, min;
    
    // Read the input
    scanf("%d", &n);

    // The total size of the pattern is 2n-1
    int size = 2 * n - 1;

    // Nested loop to print the pattern
    for (i = 0; i < size; i++) {
        for (j = 0; j < size; j++) {
            // Find the minimum distance from current position to the border
            min = i < j ? i : j;
            min = min < size - i ? min : size - i - 1;
            min = min < size - j ? min : size - j - 1;

            // Print the number corresponding to the calculated minimum distance
            printf("%d ", n - min);
        }
        printf("\n");
    }

    return 0;
}
