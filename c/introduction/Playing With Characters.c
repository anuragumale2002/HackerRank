#include <stdio.h>

#define MAX_LEN 100

int main() {
    char ch;
    char str[MAX_LEN];
    char snt[MAX_LEN];

    // Read a character
    scanf("%c", &ch);

    // Read a string
    scanf("%s", str);

    // Clear the input buffer
    while(getchar() != '\n');

    // Read a sentence
    scanf("%[^\n]%*c", snt);

    // Print the outputs
    printf("%c\n", ch);
    printf("%s\n", str);
    printf("%s\n", snt);

    return 0;
}
