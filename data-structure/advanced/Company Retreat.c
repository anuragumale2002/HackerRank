#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>

typedef long long ll;
static const ll MOD = 1000000007LL;
static const ll INF = (ll)4e18;

/* ---------- Adjacency list (tree) ---------- */
typedef struct {
    int to;
    int next;
} Edge;

static int *head;
static Edge *edges;
static int ecnt = 0;

static void add_edge(int u, int v) {
    edges[ecnt].to = v;
    edges[ecnt].next = head[u];
    head[u] = ecnt++;
}

/* ---------- Segment tree: range min, point update ---------- */
typedef struct {
    int n, size;
    ll *seg;
} SegMin;

static void seg_init(SegMin *st, int n) {
    st->n = n;
    int size = 1;
    while (size < n) size <<= 1;
    st->size = size;
    st->seg = (ll*)malloc(sizeof(ll) * (2 * size));
    for (int i = 0; i < 2 * size; i++) st->seg[i] = INF;
}

static void seg_update(SegMin *st, int pos1, ll val) {
    // pos1 is 1-indexed
    int i = st->size + (pos1 - 1);
    st->seg[i] = val;
    i >>= 1;
    while (i) {
        ll a = st->seg[i << 1];
        ll b = st->seg[(i << 1) | 1];
        st->seg[i] = (a < b) ? a : b;
        i >>= 1;
    }
}

static ll seg_query(SegMin *st, int l1, int r1) {
    // inclusive, 1-indexed
    int l = st->size + (l1 - 1);
    int r = st->size + (r1 - 1);
    ll res = INF;
    while (l <= r) {
        if (l & 1) { if (st->seg[l] < res) res = st->seg[l]; l++; }
        if (!(r & 1)) { if (st->seg[r] < res) res = st->seg[r]; r--; }
        l >>= 1; r >>= 1;
    }
    return res;
}

/* ---------- Max-heap by depth ---------- */
typedef struct {
    int depth;
    int node;
} HeapItem;

typedef struct {
    HeapItem *a;
    int sz;
    int cap;
} MaxHeap;

static void heap_init(MaxHeap *h, int cap) {
    h->a = (HeapItem*)malloc(sizeof(HeapItem) * (cap + 5));
    h->sz = 0;
    h->cap = cap + 5;
}

static void heap_push(MaxHeap *h, int depth, int node) {
    if (h->sz + 1 >= h->cap) {
        h->cap *= 2;
        h->a = (HeapItem*)realloc(h->a, sizeof(HeapItem) * h->cap);
    }
    int i = ++h->sz;
    while (i > 1) {
        int p = i >> 1;
        if (h->a[p].depth >= depth) break;
        h->a[i] = h->a[p];
        i = p;
    }
    h->a[i].depth = depth;
    h->a[i].node = node;
}

static int heap_empty(MaxHeap *h) { return h->sz == 0; }

static HeapItem heap_pop(MaxHeap *h) {
    HeapItem top = h->a[1];
    HeapItem x = h->a[h->sz--];
    int i = 1;
    while (1) {
        int l = i << 1, r = l | 1;
        if (l > h->sz) break;
        int mx = l;
        if (r <= h->sz && h->a[r].depth > h->a[l].depth) mx = r;
        if (h->a[mx].depth <= x.depth) break;
        h->a[i] = h->a[mx];
        i = mx;
    }
    h->a[i] = x;
    return top;
}

/* ---------- Binary lifting jump ---------- */
static int *up;     // flat: up[j*(n+1) + u]
static int LOGN;
static int N;

static inline int UP(int u, int k) {
    int j = 0;
    while (k && u) {
        if (k & 1) u = up[j*(N+1) + u];
        k >>= 1;
        j++;
    }
    return u;
}

int main(void) {
    int n, d;
    if (scanf("%d %d", &n, &d) != 2) return 0;
    N = n;

    head = (int*)malloc(sizeof(int) * (n + 1));
    for (int i = 0; i <= n; i++) head[i] = -1;

    edges = (Edge*)malloc(sizeof(Edge) * (2 * n + 5));

    int *parent = (int*)malloc(sizeof(int) * (n + 1));
    parent[1] = 0;
    for (int i = 2; i <= n; i++) {
        int p; scanf("%d", &p);
        parent[i] = p;
        add_edge(p, i);
    }

    /* Euler tour + depth + postorder (iterative) */
    int *tin = (int*)malloc(sizeof(int) * (n + 1));
    int *tout = (int*)malloc(sizeof(int) * (n + 1));
    int *depth = (int*)malloc(sizeof(int) * (n + 1));
    int *post = (int*)malloc(sizeof(int) * (n + 1));
    int post_sz = 0;

    // stack for DFS: node, iterator edge index
    int *st_node = (int*)malloc(sizeof(int) * (n + 5));
    int *st_it   = (int*)malloc(sizeof(int) * (n + 5));
    int top = 0, timer = 0;

    depth[1] = 1;
    st_node[top] = 1;
    st_it[top] = head[1];
    timer++;
    tin[1] = timer;

    while (top >= 0) {
        int u = st_node[top];
        int ei = st_it[top];

        if (ei == -1) {
            tout[u] = timer;
            post[post_sz++] = u;
            top--;
            continue;
        }

        // advance iterator
        st_it[top] = edges[ei].next;
        int v = edges[ei].to;

        depth[v] = depth[u] + 1;
        top++;
        st_node[top] = v;
        st_it[top] = head[v];
        timer++;
        tin[v] = timer;
    }

    /* Binary lifting table */
    LOGN = 0;
    while ((1 << LOGN) <= n) LOGN++;
    up = (int*)malloc(sizeof(int) * (LOGN * (n + 1)));
    for (int u = 1; u <= n; u++) up[0*(n+1) + u] = parent[u];
    for (int j = 1; j < LOGN; j++) {
        int *prev = up + (j-1)*(n+1);
        int *cur  = up + j*(n+1);
        cur[0] = 0;
        for (int u = 1; u <= n; u++) cur[u] = prev[ prev[u] ];
    }

    /* dist[u] = distance to nearest leaf in subtree (bottom-up) */
    int *dist = (int*)malloc(sizeof(int) * (n + 1));
    int *cnt = (int*)calloc(n + 2, sizeof(int));

    for (int i = 0; i < post_sz; i++) {
        int u = post[i];
        if (head[u] == -1) {
            dist[u] = 0;
        } else {
            int mn = INT_MAX;
            for (int e = head[u]; e != -1; e = edges[e].next) {
                int v = edges[e].to;
                int dv = dist[v] + 1;
                if (dv < mn) mn = dv;
            }
            dist[u] = mn;
        }
        if (dist[u] <= n) cnt[dist[u]]++;
    }

    /* bucket nodes by dist value using counting + prefix sums */
    int *off = (int*)malloc(sizeof(int) * (n + 3));
    off[0] = 0;
    for (int i = 0; i <= n; i++) off[i+1] = off[i] + cnt[i];

    int *bucket_nodes = (int*)malloc(sizeof(int) * (n + 1));
    int *ptr = (int*)malloc(sizeof(int) * (n + 2));
    for (int i = 0; i <= n; i++) ptr[i] = off[i];

    for (int u = 1; u <= n; u++) {
        int du = dist[u];
        if (du <= n) bucket_nodes[ ptr[du]++ ] = u;
    }

    /* Segment tree: leaves active initially */
    SegMin seg;
    seg_init(&seg, n);

    int leaf_count = 0;
    for (int u = 1; u <= n; u++) {
        if (dist[u] == 0) {
            seg_update(&seg, tin[u], (ll)depth[u]);
            leaf_count++;
        }
    }

    /* Precompute groups[k] for k=1..n */
    int *groups = (int*)malloc(sizeof(int) * (n + 1));
    groups[1] = n;

    MaxHeap heap;
    heap_init(&heap, n + 5);

    int *activated = (int*)malloc(sizeof(int) * (n + 5)); // nodes activated for this k
    for (int k = 2; k <= n; k++) {
        int total = leaf_count;

        // push nodes with dist == k into heap (by depth)
        for (int idx = off[k]; idx < off[k+1]; idx++) {
            int u = bucket_nodes[idx];
            heap_push(&heap, depth[u], u);
        }

        int act_sz = 0;

        while (!heap_empty(&heap)) {
            HeapItem it = heap_pop(&heap);
            int u = it.node;

            ll mnDepth = seg_query(&seg, tin[u], tout[u]);
            if (mnDepth - (ll)depth[u] < (ll)k) {
                continue; // too close to an active node in subtree
            }

            // activate u
            seg_update(&seg, tin[u], (ll)depth[u]);
            total++;
            activated[act_sz++] = u;

            // push ancestor k steps up
            int a = UP(u, k);
            if (a) heap_push(&heap, depth[a], a);
        }

        groups[k] = total;

        // rollback activated nodes (keep leaves active permanently)
        for (int i = 0; i < act_sz; i++) {
            int u = activated[i];
            seg_update(&seg, tin[u], INF);
        }
    }

    /* Answer queries */
    ll ans = 0;
    for (int i = 0; i < d; i++) {
        ll c; int k;
        scanf("%lld %d", &c, &k);
        if (k > n) k = n;
        ans = (ans + (c % MOD) * (groups[k] % MOD)) % MOD;
    }
    printf("%lld\n", ans);

    return 0;
}
