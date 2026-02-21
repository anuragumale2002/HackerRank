#include <stdio.h>
#include <math.h>

void update(int *a, int *b) {
    int originalA = *a;
    int originalB = *b;
    
    // sum
    *a = originalA + originalB;
    
    // absolute difference
    *b = abs(originalA - originalB);
}


int main() {
    int a, b;
    int *pa = &a, *pb = &b;
    
    scanf("%d %d", &a, &b);
    update(pa, pb);
    printf("%d\n%d", a, b);

    return 0;
}