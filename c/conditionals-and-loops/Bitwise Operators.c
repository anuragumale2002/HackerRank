#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>
//Complete the following function.


void calculate_the_maximum(int n, int k) {
    int i, j, and = 0, or = 0, XOR = 0;
    for(i = 1;i < n;i++)
    {
        for(j = i + 1;j <= n;j++)
        {
            if((i&j) > and && (i&j) < k)
                and = i&j;
        }
    }
    for(i = 1;i < n;i++)
    {
        for(j = i + 1;j <= n;j++)
        {
            if((i|j) > or && (i|j) < k)
                or = i|j;
        }
    }
    for(i = 1;i < n;i++)
    {
        for(j = i + 1;j <= n;j++)
        {
            if((i^j) > XOR && (i^j) < k)
                XOR = i^j;
        }
    }
    printf("%d\n%d\n%d",and,or,XOR);
}

int main() {
    int n, k;
  
    scanf("%d %d", &n, &k);
    calculate_the_maximum(n, k);
 
    return 0;
}
