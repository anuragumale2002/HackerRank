#include <stdio.h>
#include <stdlib.h>
#include <string.h>


int lexicographic_sort(const char* a, const char* b) {
    return strcmp(a, b);
}

int lexicographic_sort_reverse(const char* a, const char* b) {
    return strcmp(b, a);
}

int number_of_distinct_characters(const char* s) {
    int count[26] = {0}, distinct = 0;
    while (*s) {
        if (!count[*s - 'a']) distinct++;
        count[*s++ - 'a']++;
    }
    return distinct;
}

int sort_by_number_of_distinct_characters(const char* a, const char* b) {
    int distinct_a = number_of_distinct_characters(a);
    int distinct_b = number_of_distinct_characters(b);
    return (distinct_a != distinct_b) ? (distinct_a - distinct_b) : strcmp(a, b);
}

int sort_by_length(const char* a, const char* b) {
    return (strlen(a) != strlen(b)) ? (strlen(a) - strlen(b)) : strcmp(a, b);
}

void string_sort(char** arr, int cnt, int (*cmp_func)(const char*, const char*)) {
    for (int i = 0; i < cnt - 1; i++) {
        for (int j = i + 1; j < cnt; j++) {
            if (cmp_func(arr[i], arr[j]) > 0) {
                char* temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }
    }
}

int main() 
{
    int n;
    scanf("%d", &n);
  
    char** arr;
	arr = (char**)malloc(n * sizeof(char*));
  
    for(int i = 0; i < n; i++){
        *(arr + i) = malloc(1024 * sizeof(char));
        scanf("%s", *(arr + i));
        *(arr + i) = realloc(*(arr + i), strlen(*(arr + i)) + 1);
    }
  
    string_sort(arr, n, lexicographic_sort);
    for(int i = 0; i < n; i++)
        printf("%s\n", arr[i]);
    printf("\n");

    string_sort(arr, n, lexicographic_sort_reverse);
    for(int i = 0; i < n; i++)
        printf("%s\n", arr[i]); 
    printf("\n");

    string_sort(arr, n, sort_by_length);
    for(int i = 0; i < n; i++)
        printf("%s\n", arr[i]);    
    printf("\n");

    string_sort(arr, n, sort_by_number_of_distinct_characters);
    for(int i = 0; i < n; i++)
        printf("%s\n", arr[i]); 
    printf("\n");
}