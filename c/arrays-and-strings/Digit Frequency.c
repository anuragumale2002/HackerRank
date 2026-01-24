#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

int main() {
    char num[1000];
    scanf("%s", num);

    int digit_count[10] = {0}; // Array to store the count of each digit

    // Iterate through each character in the string
    for (int i = 0; i < strlen(num); i++) {
        if (num[i] >= '0' && num[i] <= '9') {
            digit_count[num[i] - '0']++; // Increment count of the digit
        }
    }

    // Print the frequency of each digit
    for (int i = 0; i < 10; i++) {
        printf("%d ", digit_count[i]);
    }
    printf("\n");

    return 0;
}
