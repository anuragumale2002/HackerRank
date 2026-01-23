#include <stdio.h>
#include <stdlib.h>
#include <assert.h>

typedef long long ll;

typedef struct Node Node;
struct Node {
    Node *p, *l, *r;
    int sz;
    ll v, sm;
};

static Node LAST_D;          // sentinel node storage
static Node *LAST = &LAST_D; // sentinel pointer

static inline int sz(Node *x) { return x ? x->sz : 0; }
static inline ll  sm(Node *x) { return x ? x->sm : 0; }

static inline void update(Node *x) {
    if (x == LAST) return;
    x->sz = 1 + x->l->sz + x->r->sz;
    x->sm = x->v + x->l->sm + x->r->sm;
}

static inline int pos(Node *x) {
    if (!x->p) return 0;
    if (x->p->l == x) return -1;
    if (x->p->r == x) return 1;
    return 0;
}

static void rotate(Node *x) {
    Node *p = x->p;
    Node *g = p->p;
    int ppos = pos(p);

    if (p->l == x) {
        p->l = x->r;
        x->r->p = p;
        x->r = p;
        p->p = x;
    } else {
        p->r = x->l;
        x->l->p = p;
        x->l = p;
        p->p = x;
    }

    update(p);
    update(x);

    x->p = g;
    if (!ppos) return;

    if (ppos == -1) g->l = x;
    else g->r = x;
    update(g);
}

static void splay(Node *x) {
    assert(x != LAST);
    while (pos(x)) {
        int ps = pos(x);
        int pps = pos(x->p);
        if (!pps) {
            rotate(x);
        } else if (ps == pps) {
            rotate(x->p);
            rotate(x);
        } else {
            rotate(x);
            rotate(x);
        }
    }
}

static Node* splay_k(Node *x, int k) {
    assert(x != LAST);
    assert(0 <= k && k < x->sz);

    while (1) {
        int lsz = x->l->sz;
        if (k < lsz) {
            x = x->l;
        } else if (k == lsz) {
            splay(x);
            return x;
        } else {
            k -= lsz + 1;
            x = x->r;
        }
    }
}

/* merge(l, r): all nodes in l come before all nodes in r */
static Node* merge(Node *l, Node *r) {
    if (r == LAST) return l;
    r = splay_k(r, 0);           // bring min of r to root
    assert(r->l == LAST);
    r->l = l;
    l->p = r;
    update(r);
    return r;
}

/* split(x, k): first k nodes and remaining */
static void split(Node *x, int k, Node **a, Node **b) {
    assert(0 <= k && k <= x->sz);
    if (k == x->sz) {
        *a = x;
        *b = LAST;
        return;
    }
    x = splay_k(x, k);
    Node *left = x->l;
    left->p = NULL;
    x->l = LAST;
    update(x);
    *a = left;
    *b = x;
}

/* ----------- build from array (balanced) ----------- */
static Node* new_node(ll v) {
    Node *x = (Node*)malloc(sizeof(Node));
    x->p = NULL;
    x->l = LAST;
    x->r = LAST;
    x->sz = 1;
    x->v = v;
    x->sm = v;
    return x;
}

static Node* build(int n, ll *arr) {
    if (n <= 0) return LAST;
    int mid = n / 2;
    Node *x = new_node(arr[mid]);
    x->l = build(mid, arr);
    x->l->p = x;
    x->r = build(n - (mid + 1), arr + (mid + 1));
    x->r->p = x;
    update(x);
    return x;
}

/* range sum [l, r) */
static ll range_sum(Node **root, int l, int r) {
    Node *A, *B, *C;
    split(*root, r, &B, &C);
    split(B, l, &A, &B);
    ll res = B->sm;
    *root = merge(merge(A, B), C);
    return res;
}

/* split at k returning right part; root becomes left */
static Node* cut_right(Node **root, int k) {
    Node *A, *B;
    split(*root, k, &A, &B);
    *root = A;
    return B;
}

/* append tree t2 onto t1: root1 = merge(root1, root2) */
static void merge_into(Node **root1, Node *root2) {
    *root1 = merge(*root1, root2);
}

/* ------------- main swap logic like your C++ code ------------- */
int main() {
    // init sentinel
    LAST_D.p = NULL;
    LAST_D.l = LAST;
    LAST_D.r = LAST;
    LAST_D.sz = 0;
    LAST_D.v = 0;
    LAST_D.sm = 0;

    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;

    // store parity arrays
    ll *a0 = (ll*)malloc(((n + 1) / 2) * sizeof(ll));
    ll *a1 = (ll*)malloc((n / 2) * sizeof(ll));
    int c0 = 0, c1 = 0;

    for (int i = 0; i < n; i++) {
        ll v;
        scanf("%lld", &v);
        if ((i & 1) == 0) a0[c0++] = v;
        else a1[c1++] = v;
    }

    Node *tr0 = build(c0, a0);
    Node *tr1 = build(c1, a1);

    for (int qc = 0; qc < q; qc++) {
        int t;
        ll l, r;
        scanf("%d %lld %lld", &t, &l, &r);
        l--; // now l is 0-index, r is still 1-indexed? in original code r not decremented
            // In your C++ snippet: l-- only, and uses (r+1)/2 etc => r is 1-indexed inclusive.
            // We'll keep same interpretation: l is 0-based, r is 1-based inclusive.
            // That matches their formulas.
        if (t == 1) {
            // x[1] = tr0.split((r+1)/2);
            // x[0] = tr0.split((l+1)/2);
            // y[1] = tr1.split(r/2);
            // y[0] = tr1.split(l/2);

            Node *x1 = cut_right(&tr0, (int)((r + 1) / 2));
            Node *x0 = cut_right(&tr0, (int)((l + 1) / 2));

            Node *y1 = cut_right(&tr1, (int)(r / 2));
            Node *y0 = cut_right(&tr1, (int)(l / 2));

            // tr0.merge(y0); tr0.merge(x1);
            // tr1.merge(x0); tr1.merge(y1);

            merge_into(&tr0, y0);
            merge_into(&tr0, x1);

            merge_into(&tr1, x0);
            merge_into(&tr1, y1);
        } else {
            ll ans = 0;
            ans += range_sum(&tr0, (int)((l + 1) / 2), (int)((r + 1) / 2));
            ans += range_sum(&tr1, (int)(l / 2), (int)(r / 2));
            printf("%lld\n", ans);
        }
    }

    // cleanup arrays (nodes not freed; acceptable in contest environments)
    free(a0);
    free(a1);
    return 0;
}
