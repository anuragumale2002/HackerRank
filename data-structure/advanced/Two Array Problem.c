#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <string.h>

#define EPS 1e-12

// -------------------------
// Fast RNG (xorshift32)
// -------------------------
static uint32_t rng_state = 123456789u;
static inline uint32_t rng_u32() {
    uint32_t x = rng_state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    rng_state = x;
    return x;
}
static inline int rng_int(int n) { // 0..n-1
    return (int)(rng_u32() % (uint32_t)n);
}

// -------------------------
// Implicit Treap
// -------------------------
typedef struct Node {
    int v;
    uint32_t pri;
    int sz;
    unsigned char rev;
    struct Node *l, *r;
} Node;

static inline int sz(Node *t) { return t ? t->sz : 0; }

static inline void pull(Node *t) {
    t->sz = 1 + sz(t->l) + sz(t->r);
}

static inline void push(Node *t) {
    if (t && t->rev) {
        t->rev = 0;
        Node *tmp = t->l;
        t->l = t->r;
        t->r = tmp;
        if (t->l) t->l->rev ^= 1;
        if (t->r) t->r->rev ^= 1;
    }
}

static Node* new_node(int v) {
    Node *n = (Node*)malloc(sizeof(Node));
    n->v = v;
    n->pri = rng_u32();
    n->sz = 1;
    n->rev = 0;
    n->l = n->r = NULL;
    return n;
}

static Node* merge(Node *a, Node *b) {
    if (!a) return b;
    if (!b) return a;
    push(a); push(b);
    if (a->pri > b->pri) {
        a->r = merge(a->r, b);
        pull(a);
        return a;
    } else {
        b->l = merge(a, b->l);
        pull(b);
        return b;
    }
}

// split by first k elements: left has k, right has rest
static void split(Node *t, int k, Node **a, Node **b) {
    if (!t) { *a = NULL; *b = NULL; return; }
    push(t);
    if (sz(t->l) >= k) {
        split(t->l, k, a, &t->l);
        pull(t);
        *b = t;
    } else {
        split(t->r, k - sz(t->l) - 1, &t->r, b);
        pull(t);
        *a = t;
    }
}

// Build treap in O(n) using a stack (Cartesian by priority)
static Node* build_treap(int *arr, int n) {
    Node **st = (Node**)malloc(sizeof(Node*) * n);
    int top = 0;
    for (int i = 0; i < n; i++) {
        Node *nd = new_node(arr[i]);
        Node *last = NULL;
        while (top > 0 && st[top-1]->pri < nd->pri) {
            last = st[--top];
        }
        if (top > 0) st[top-1]->r = nd;
        nd->l = last;
        st[top++] = nd;
    }
    Node *root = (top > 0) ? st[0] : NULL;

    // fix sizes with iterative postorder
    if (root) {
        Node **stack = (Node**)malloc(sizeof(Node*) * n * 2);
        unsigned char *state = (unsigned char*)malloc(sizeof(unsigned char) * n * 2);
        int sp = 0;
        stack[sp] = root; state[sp] = 0; sp++;
        while (sp) {
            Node *u = stack[sp-1];
            unsigned char s = state[sp-1];
            sp--;
            if (!u) continue;
            if (s == 0) {
                stack[sp] = u; state[sp] = 1; sp++;
                stack[sp] = u->r; state[sp] = 0; sp++;
                stack[sp] = u->l; state[sp] = 0; sp++;
            } else {
                pull(u);
            }
        }
        free(stack); free(state);
    }

    free(st);
    return root;
}

// inorder collect segment values into out[] (iterative), respecting lazy rev
static void inorder_collect(Node *t, int *out, int *idx) {
    Node **stack = (Node**)malloc(sizeof(Node*) * (t ? t->sz : 1));
    int sp = 0;
    Node *cur = t;
    while (cur || sp) {
        while (cur) {
            push(cur);
            stack[sp++] = cur;
            cur = cur->l;
        }
        cur = stack[--sp];
        out[(*idx)++] = cur->v;
        cur = cur->r;
    }
    free(stack);
}

// -------------------------
// Query ops
// -------------------------
static Node* reverse_range(Node *root, int l, int r) {
    Node *a, *bc, *b, *c;
    split(root, l-1, &a, &bc);
    split(bc, r-l+1, &b, &c);
    if (b) b->rev ^= 1;
    return merge(a, merge(b, c));
}

// swap two disjoint segments in same array (can have a gap). assumes non-overlap.
static Node* swap_segments(Node *root, int l1, int r1, int l2, int r2) {
    if (l1 > l2) { int tl=l1; l1=l2; l2=tl; int tr=r1; r1=r2; r2=tr; }
    // assume r1 < l2
    Node *pre, *rest, *seg1, *mid, *seg2, *suf;

    split(root, l1-1, &pre, &rest);
    split(rest, r1-l1+1, &seg1, &rest);
    split(rest, l2-r1-1, &mid, &rest);         // gap (maybe empty)
    split(rest, r2-l2+1, &seg2, &suf);

    return merge(pre, merge(seg2, merge(mid, merge(seg1, suf))));
}

static void swap_between(Node **A, Node **B, int l, int r) {
    Node *a1, *a2, *a3;
    Node *b1, *b2, *b3;
    split(*A, l-1, &a1, &a2);
    split(a2, r-l+1, &a2, &a3);

    split(*B, l-1, &b1, &b2);
    split(b2, r-l+1, &b2, &b3);

    *A = merge(a1, merge(b2, a3));
    *B = merge(b1, merge(a2, b3));
}

// extract values of segment [l..r] without changing treap
static void extract_segment(Node **root, int l, int r, int *out) {
    Node *pre, *mid_suf, *mid, *suf;
    split(*root, l-1, &pre, &mid_suf);
    split(mid_suf, r-l+1, &mid, &suf);
    int idx = 0;
    inorder_collect(mid, out, &idx);
    *root = merge(pre, merge(mid, suf));
}

// -------------------------
// Minimum Enclosing Circle
// -------------------------
typedef struct { double x, y; } Pt;
typedef struct { double x, y, r; } Circ;

static inline double dist2(Pt a, Pt b) {
    double dx = a.x - b.x, dy = a.y - b.y;
    return dx*dx + dy*dy;
}

static inline int in_circle(Circ c, Pt p) {
    double dx = p.x - c.x, dy = p.y - c.y;
    return dx*dx + dy*dy <= c.r*c.r + 1e-9;
}

static Circ circle1(Pt a) {
    Circ c; c.x = a.x; c.y = a.y; c.r = 0.0; return c;
}

static Circ circle2(Pt a, Pt b) {
    Circ c;
    c.x = (a.x + b.x) * 0.5;
    c.y = (a.y + b.y) * 0.5;
    c.r = sqrt(dist2(a, b)) * 0.5;
    return c;
}

static int circle3(Pt a, Pt b, Pt cpt, Circ *out) {
    double ax=a.x, ay=a.y, bx=b.x, by=b.y, cx=cpt.x, cy=cpt.y;
    double d = 2.0 * (ax*(by-cy) + bx*(cy-ay) + cx*(ay-by));
    if (fabs(d) < EPS) return 0;
    double ax2ay2 = ax*ax + ay*ay;
    double bx2by2 = bx*bx + by*by;
    double cx2cy2 = cx*cx + cy*cy;
    double ux = (ax2ay2*(by-cy) + bx2by2*(cy-ay) + cx2cy2*(ay-by)) / d;
    double uy = (ax2ay2*(cx-bx) + bx2by2*(ax-cx) + cx2cy2*(bx-ax)) / d;
    out->x = ux;
    out->y = uy;
    out->r = sqrt((ux-ax)*(ux-ax) + (uy-ay)*(uy-ay));
    return 1;
}

static void shuffle_pts(Pt *p, int n) {
    for (int i = n-1; i > 0; i--) {
        int j = rng_int(i+1);
        Pt tmp = p[i]; p[i] = p[j]; p[j] = tmp;
    }
}

static Circ min_enclosing_circle(Pt *pts, int n) {
    shuffle_pts(pts, n);
    Circ c = circle1(pts[0]);

    for (int i = 0; i < n; i++) {
        if (in_circle(c, pts[i])) continue;
        c = circle1(pts[i]);
        for (int j = 0; j < i; j++) {
            if (in_circle(c, pts[j])) continue;
            c = circle2(pts[i], pts[j]);
            for (int k = 0; k < j; k++) {
                if (in_circle(c, pts[k])) continue;
                Circ cc;
                if (circle3(pts[i], pts[j], pts[k], &cc)) {
                    c = cc;
                } else {
                    // collinear: pick smallest circle from pairs that covers all 3
                    Circ c1 = circle2(pts[i], pts[j]);
                    Circ c2 = circle2(pts[i], pts[k]);
                    Circ c3c = circle2(pts[j], pts[k]);
                    Circ best = c1;
                    if ((!in_circle(best, pts[i]) || !in_circle(best, pts[j]) || !in_circle(best, pts[k])) ||
                        (c2.r < best.r && in_circle(c2, pts[i]) && in_circle(c2, pts[j]) && in_circle(c2, pts[k])))
                        best = c2;
                    if (c3c.r < best.r && in_circle(c3c, pts[i]) && in_circle(c3c, pts[j]) && in_circle(c3c, pts[k]))
                        best = c3c;
                    c = best;
                }
            }
        }
    }
    return c;
}

// -------------------------
// Main
// -------------------------
int main() {
    int n, q;
    if (scanf("%d %d", &n, &q) != 2) return 0;

    int *A = (int*)malloc(sizeof(int) * n);
    int *B = (int*)malloc(sizeof(int) * n);
    for (int i = 0; i < n; i++) scanf("%d", &A[i]);
    for (int i = 0; i < n; i++) scanf("%d", &B[i]);

    Node *a_root = build_treap(A, n);
    Node *b_root = build_treap(B, n);

    free(A); free(B);

    // buffers for extraction
    int *xs = (int*)malloc(sizeof(int) * n);
    int *ys = (int*)malloc(sizeof(int) * n);
    Pt  *pts = (Pt*)malloc(sizeof(Pt) * n);

    for (int qi = 0; qi < q; qi++) {
        int t;
        scanf("%d", &t);
        if (t == 1) {
            int p, l, r;
            scanf("%d %d %d", &p, &l, &r);
            if (p == 0) a_root = reverse_range(a_root, l, r);
            else        b_root = reverse_range(b_root, l, r);
        } else if (t == 2) {
            int p, l1, r1, l2, r2;
            scanf("%d %d %d %d %d", &p, &l1, &r1, &l2, &r2);
            if (p == 0) a_root = swap_segments(a_root, l1, r1, l2, r2);
            else        b_root = swap_segments(b_root, l1, r1, l2, r2);
        } else if (t == 3) {
            int l, r;
            scanf("%d %d", &l, &r);
            swap_between(&a_root, &b_root, l, r);
        } else { // t == 4
            int l, r;
            scanf("%d %d", &l, &r);
            int len = r - l + 1;

            extract_segment(&a_root, l, r, xs);
            extract_segment(&b_root, l, r, ys);

            if (len <= 1) {
                printf("0.00\n");
                continue;
            }

            for (int i = 0; i < len; i++) {
                pts[i].x = (double)xs[i];
                pts[i].y = (double)ys[i];
            }

            Circ c = min_enclosing_circle(pts, len);
            printf("%.2f\n", c.r + 1e-9);
        }
    }

    free(xs);
    free(ys);
    free(pts);
    return 0;
}
