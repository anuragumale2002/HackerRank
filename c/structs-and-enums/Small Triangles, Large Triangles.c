#include <stdio.h>
#include <stdlib.h>
#include <math.h>

struct triangle
{
	int a;
	int b;
	int c;
};

typedef struct triangle triangle;

struct triangle_area {
    int index;
    double area;
};

typedef struct triangle_area triangle_area;

double calculate_area(triangle tr) {
    double p = (tr.a + tr.b + tr.c) / 2.0;
    return sqrt(p * (p - tr.a) * (p - tr.b) * (p - tr.c));
}

int compare_triangle_area(const void* a, const void* b) {
    triangle_area* tr_area_a = (triangle_area*) a;
    triangle_area* tr_area_b = (triangle_area*) b;
    return (tr_area_a->area > tr_area_b->area) - (tr_area_a->area < tr_area_b->area);
}

void sort_by_area(triangle* tr, int n) {
    triangle_area* tr_areas = malloc(n * sizeof(triangle_area));
    for (int i = 0; i < n; i++) {
        tr_areas[i].index = i;
        tr_areas[i].area = calculate_area(tr[i]);
    }

    qsort(tr_areas, n, sizeof(triangle_area), compare_triangle_area);

    triangle* sorted_tr = malloc(n * sizeof(triangle));
    for (int i = 0; i < n; i++) {
        sorted_tr[i] = tr[tr_areas[i].index];
    }

    for (int i = 0; i < n; i++) {
        tr[i] = sorted_tr[i];
    }

    free(tr_areas);
    free(sorted_tr);
}

int main()
{
	int n;
	scanf("%d", &n);
	triangle *tr = malloc(n * sizeof(triangle));
	for (int i = 0; i < n; i++) {
		scanf("%d%d%d", &tr[i].a, &tr[i].b, &tr[i].c);
	}
	sort_by_area(tr, n);
	for (int i = 0; i < n; i++) {
		printf("%d %d %d\n", tr[i].a, tr[i].b, tr[i].c);
	}
	return 0;
}