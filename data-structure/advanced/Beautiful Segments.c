#include <stdio.h>
#include <stdlib.h>

#define TYPE_EVENT 0
#define TYPE_QUERY 1

typedef long long ll;

typedef struct {
    int type;   // 0 event, 1 query
    int R;      // time dimension
    int val;    // AND value for event, K for query
    int l1;     // event: left range start; query: L
    int l2;     // event: left range end;   query: unused
    int id;     // query id, event: -1
} Item;

/* -------- Fast Input -------- */
static inline int read_int() {
    int c = getchar_unlocked();
    while (c <= ' ' && c != EOF) c = getchar_unlocked();
    int x = 0;
    while (c > ' ') {
        x = x * 10 + (c - '0');
        c = getchar_unlocked();
    }
    return x;
}

/* -------- BIT for range add + suffix sum --------
   Uses two BITs for range add / prefix sum, plus a running total so suffix_sum(L)
   = total - prefix_sum(L-1), avoiding prefix_sum(n) per query.
*/
typedef struct {
    int n;
    ll *b1;
    ll *b2;
    ll total;
} BITRange;

static inline void bit_add(ll *bit, int n, int i, ll v) {
    while (i <= n) {
        bit[i] += v;
        i += i & -i;
    }
}

static inline ll bit_sum(ll *bit, int i) {
    ll s = 0;
    while (i > 0) {
        s += bit[i];
        i -= i & -i;
    }
    return s;
}

static inline void bit_range_add(BITRange *B, int l, int r, ll v) {
    if (l > r) return;
    B->total += v * (ll)(r - l + 1);

    int n = B->n;
    bit_add(B->b1, n, l, v);
    bit_add(B->b1, n, r + 1, -v);
    bit_add(B->b2, n, l, v * (ll)(l - 1));
    bit_add(B->b2, n, r + 1, -v * (ll)r);
}

static inline ll bit_prefix_sum(BITRange *B, int i) {
    if (i <= 0) return 0;
    ll s1 = bit_sum(B->b1, i);
    ll s2 = bit_sum(B->b2, i);
    return s1 * (ll)i - s2;
}

static inline ll bit_suffix_sum(BITRange *B, int l) {
    return B->total - bit_prefix_sum(B, l - 1);
}

/* -------- Sorting by R -------- */
static int cmp_item_R(const void *pa, const void *pb) {
    const Item *a = (const Item *)pa;
    const Item *b = (const Item *)pb;
    if (a->R < b->R) return -1;
    if (a->R > b->R) return 1;
    return a->type - b->type;
}

/* -------- CDQ (merge by val) -------- */
static Item *items;
static int *ord_idx;
static int *tmp_idx;
static int *applied;
static ll *ans;
static BITRange bitR;

static void cdq(int lo, int hi) {
    if (lo >= hi) return;
    int mid = (lo + hi) >> 1;

    cdq(lo, mid);
    cdq(mid + 1, hi);

    int i = lo, j = mid + 1, k = lo;
    int app_cnt = 0;

    while (i <= mid && j <= hi) {
        int li = ord_idx[i];
        int rj = ord_idx[j];

        if (items[li].val <= items[rj].val) {
            if (items[li].type == TYPE_EVENT) {
                bit_range_add(&bitR, items[li].l1, items[li].l2, 1);
                applied[app_cnt++] = li;
            }
            tmp_idx[k++] = li;
            i++;
        } else {
            if (items[rj].type == TYPE_QUERY) {
                ans[items[rj].id] += bit_suffix_sum(&bitR, items[rj].l1);
            }
            tmp_idx[k++] = rj;
            j++;
        }
    }

    while (i <= mid) {
        int li = ord_idx[i++];
        if (items[li].type == TYPE_EVENT) {
            bit_range_add(&bitR, items[li].l1, items[li].l2, 1);
            applied[app_cnt++] = li;
        }
        tmp_idx[k++] = li;
    }

    while (j <= hi) {
        int rj = ord_idx[j++];
        if (items[rj].type == TYPE_QUERY) {
            ans[items[rj].id] += bit_suffix_sum(&bitR, items[rj].l1);
        }
        tmp_idx[k++] = rj;
    }

    // rollback
    for (int t = 0; t < app_cnt; t++) {
        int li = applied[t];
        bit_range_add(&bitR, items[li].l1, items[li].l2, -1);
    }

    // copy back
    for (int t = lo; t <= hi; t++) ord_idx[t] = tmp_idx[t];
}

int main() {
    int n = read_int();
    int q = read_int();

    int *a = (int *)malloc((n + 1) * sizeof(int));
    for (int i = 1; i <= n; i++) a[i] = read_int();

    // Max events <= 17*n (Ai < 2^17) plus q queries
    int max_items = 17 * n + q + 5;
    items = (Item *)malloc((size_t)max_items * sizeof(Item));
    int m = 0;

    // Build events per right endpoint
    int prev_val[25], prev_min[25], prev_len = 0;
    for (int j = 1; j <= n; j++) {
        int x = a[j];
        int cur_val[25], cur_min[25], cur_len = 0;

        // start with [x, j]
        cur_val[cur_len] = x;
        cur_min[cur_len] = j;
        cur_len++;

        for (int t = 0; t < prev_len; t++) {
            int nv = prev_val[t] & x;
            if (nv == cur_val[cur_len - 1]) {
                cur_min[cur_len - 1] = prev_min[t];
            } else {
                cur_val[cur_len] = nv;
                cur_min[cur_len] = prev_min[t];
                cur_len++;
            }
        }

        int prev_l = j + 1;
        for (int t = 0; t < cur_len; t++) {
            int mn = cur_min[t];
            items[m].type = TYPE_EVENT;
            items[m].R = j;
            items[m].val = cur_val[t];
            items[m].l1 = mn;
            items[m].l2 = prev_l - 1;
            items[m].id = -1;
            m++;
            prev_l = mn;
        }

        // move cur -> prev
        prev_len = cur_len;
        for (int t = 0; t < cur_len; t++) {
            prev_val[t] = cur_val[t];
            prev_min[t] = cur_min[t];
        }
    }

    // Add queries
    ans = (ll *)calloc((size_t)q, sizeof(ll));
    for (int i = 0; i < q; i++) {
        int L = read_int();
        int R = read_int();
        int K = read_int();
        items[m].type = TYPE_QUERY;
        items[m].R = R;
        items[m].val = K;
        items[m].l1 = L;
        items[m].l2 = 0;
        items[m].id = i;
        m++;
    }

    free(a);

    // Sort items by R once
    qsort(items, (size_t)m, sizeof(Item), cmp_item_R);

    // Prepare CDQ arrays
    ord_idx = (int *)malloc((size_t)m * sizeof(int));
    tmp_idx = (int *)malloc((size_t)m * sizeof(int));
    applied = (int *)malloc((size_t)m * sizeof(int));
    for (int i = 0; i < m; i++) ord_idx[i] = i;

    // BIT init
    bitR.n = n;
    bitR.b1 = (ll *)calloc((size_t)(n + 2), sizeof(ll));
    bitR.b2 = (ll *)calloc((size_t)(n + 2), sizeof(ll));
    bitR.total = 0;

    // Run CDQ
    cdq(0, m - 1);

    // Output
    for (int i = 0; i < q; i++) {
        printf("%lld\n", ans[i]);
    }

    // Cleanup
    free(items);
    free(ord_idx);
    free(tmp_idx);
    free(applied);
    free(ans);
    free(bitR.b1);
    free(bitR.b2);

    return 0;
}
