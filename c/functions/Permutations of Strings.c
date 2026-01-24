#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Function to compare strings for qsort
int compare_strings(const void *a, const void *b) {
    return strcmp(*(const char **)a, *(const char **)b);
}

// Function to swap strings
void swap_strings(char **a, char **b) {
    char *temp = *a;
    *a = *b;
    *b = temp;
}

// Function to find the next permutation
int next_permutation(int n, char **arr) {
    // Step 1: Find the largest index k such that arr[k] < arr[k + 1]
    int k;
    for (k = n - 2; k >= 0; k--) {
        if (strcmp(arr[k], arr[k + 1]) < 0) {
            break;
        }
    }
    // If no such index exists, the permutation is the last permutation
    if (k < 0) {
        return 0;
    }

    // Step 2: Find the largest index l greater than k such that arr[k] < arr[l]
    int l;
    for (l = n - 1; l > k; l--) {
        if (strcmp(arr[k], arr[l]) < 0) {
            break;
        }
    }

    // Step 3: Swap arr[k] and arr[l]
    swap_strings(&arr[k], &arr[l]);

    // Step 4: Reverse the sequence from arr[k + 1] up to and including the final element arr[n-1]
    for (int i = k + 1, j = n - 1; i < j; i++, j--) {
        swap_strings(&arr[i], &arr[j]);
    }

    return 1;
}




int main()
{
	char **s;
	int n;
	scanf("%d", &n);
	s = calloc(n, sizeof(char*));
	for (int i = 0; i < n; i++)
	{
		s[i] = calloc(11, sizeof(char));
		scanf("%s", s[i]);
	}
	do
	{
		for (int i = 0; i < n; i++)
			printf("%s%c", s[i], i == n - 1 ? '\n' : ' ');
	} while (next_permutation(n, s));
	for (int i = 0; i < n; i++)
		free(s[i]);
	free(s);
	return 0;
}