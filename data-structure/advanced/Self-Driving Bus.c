#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdlib.h>

#define fprintf(...)

struct vertex {
    struct vertex* parent;
    int rank;
    int count;
};

struct vertex* vfind(struct vertex *v) {
    if (v->parent == NULL) return v;  // this is a disconnected one.
    if (v->parent != v) {
        v->parent = vfind(v->parent);
    }
    return v->parent;
}

struct vertex* vunion(struct vertex *x, struct vertex* y) {
    struct vertex *xroot = vfind(x);
    struct vertex *yroot = vfind(y);
    if (xroot == yroot) return yroot;
    // fix any uninitialized counts.
    if (xroot->count == 0) xroot->count++;
    if (yroot->count == 0) yroot->count++;
    
    if (xroot->rank > yroot->rank) {
        struct vertex* tmp = xroot;
        xroot = yroot;
        yroot = tmp;
    }
    // xroot is now the smaller tree if they're not the same.
    if (xroot->rank == yroot->rank) {
        yroot->rank++;
    }
    xroot->parent = yroot;
    yroot->count += xroot->count;
    return yroot;
}

struct edge {
    int a, b;
};

int ecmp(const void*a_in, const void*b_in) {
    const struct edge* a = a_in;
    const struct edge* b = b_in;
    
    if (a->b < b->b) return -1;
    if (a->b > b->b) return 1;
    if (a->a < b->a) return -1;
    if (a->a > b->a) return 1;
    return 0;
}

int ecmp_a(const void*a_in, const void*b_in) {
    const struct edge* a = a_in;
    const struct edge* b = b_in;
    
    if (a->a < b->a) return -1;
    if (a->a > b->a) return 1;
    if (a->b < b->b) return -1;
    if (a->b > b->b) return 1;
    return 0;
}

// n * ack-1(n) algorithm; needs to be run n times for n^2 ack-1(n).  Not the best, but gets 50%.
int count_components1(int start, struct edge* edges, int ne, int n) {
    if (ne == 0) return 1;
    fprintf(stderr, "start: %d, ne %d, n %d\n", start, ne, n);
    int max_components = n - start + 1;
    struct vertex v[max_components];
    memset(v, 0, sizeof(v));
    int components = 1;
    struct edge* le = edges + ne;
    for (int maxv = start + 1; maxv <= n; maxv++) {
        struct vertex* join = NULL;
        while (edges < le && edges->b <= maxv) {
            if (edges->a >= start) {
                join = vunion(&v[edges->a - start], &v[edges->b - start]);
                fprintf(stderr, "Join: %d to %d, new count %d\n", edges->a, edges->b, join->count);
            }
            edges++;
        }
        if (join && join->count == maxv - start + 1) components++;
    }
    return components;
}

int count_components(int start, struct edge* edges, int ne, int n) {
    if (ne == 0) return 1;
    fprintf(stderr, "start: %d, ne %d, n %d\n", start, ne, n);
    int max_components = n - start + 1;
    struct vertex v[max_components];
    memset(v, 0, sizeof(v));
    int components = 1;
    struct edge* le = edges + ne;
    for (int maxv = start + 1; maxv <= n; maxv++) {
        struct vertex* join = NULL;
        while (edges < le && edges->b <= maxv) {
            if (edges->a >= start) {
                join = vunion(&v[edges->a - start], &v[edges->b - start]);
                fprintf(stderr, "Join: %d to %d, new count %d\n", edges->a, edges->b, join->count);
            }
            edges++;
        }
        if (join && join->count == maxv - start + 1) components++;
    }
    return components;
}

int old_main() {
    int n;
    scanf("%d\n", &n);
    struct edge edges[n-1];
    memset(edges, 0, sizeof(edges));
    for (int i = 0; i < n-1; i++) {
        int e1, e2;
        scanf("%d %d\n", &e1, &e2);
        if (e1 < e2) {
            edges[i].a = e1;
            edges[i].b = e2;
        } else {
            edges[i].a = e2;
            edges[i].b = e1;         
        }
    }
    qsort(edges, n-1, sizeof(struct edge), ecmp);
    for (int i = 0; i < n-1; i++) {
        fprintf(stderr, "Edge: %d %d\n", edges[i].a, edges[i].b);
    }
    int result = 0;
    struct edge *ep = edges;
    struct edge *lp = edges + n - 1;
    for (int i = 1; i <= n; i++) {
        while(ep < lp && ep->a < i) ep++;
        int cc = count_components(i, ep, lp - ep, n);
        fprintf(stderr, "i: %d  cc: %d\n", i, cc);
        result += cc;
    }
    printf("%d\n", result);
    return 0;
}


struct node {
    int nn;
    // indexes of forward edges in the node.
    // Edges always belong to the low node.
    int first_edge;
    int n_edges;
};

struct line {
    int start_node;
    int end_node;
};

struct segment_node {
    int lazy;
    int max_v;  // maximum value of any node below
    int num_v;  // number of nodes with that maximum value
};

#define C1(i) ((i)*2+1)
#define C2(i) ((i)*2+2)

void propagate(struct segment_node* tree, int index, int start, int end) {
    if (!tree[index].lazy) return;
    if (start == end) {
        // leaf, nothing to do;
        tree[index].lazy = 0;
        return;
    }
    fprintf(stderr, "Prop: %d v: %d\n", index, tree[index].lazy);
    tree[C1(index)].lazy += tree[index].lazy;
    tree[C2(index)].lazy += tree[index].lazy;
    tree[C1(index)].max_v += tree[index].lazy; 
    tree[C2(index)].max_v += tree[index].lazy;
    tree[index].lazy = 0;
}

// ns, ne = node start/end = recursion counter
// rs, re = input range start/end
// adds "v" to all nodes between rs and re.
// the segment tree is implicitly "complete", i.e. contains all integers in [ns, ne]
int treelim;
void update(struct segment_node* tree, int index, int ns, int ne, int rs, int re, int v) {
    if (index >= treelim) exit(-1);
    fprintf(stderr, "upd: i: %d ns,ne (%d %d) rs, re (%d %d), v %d\n", index, ns, ne, rs, re, v);
    fprintf(stderr, "   prev max_v %d num_v %d\n", tree[index].max_v, tree[index].num_v);
    propagate(tree, index, ns, ne);
    if (ns == rs && ne == re) {
        tree[index].max_v += v;
        if (ns == ne) tree[index].num_v = 1;
        tree[index].lazy += v;
        return;
    }
    int mid = (ns + ne) / 2;
    if (re <= mid) update(tree, C1(index), ns, mid, rs, re, v);
    else if (rs > mid) update(tree, C2(index), mid + 1, ne, rs, re, v);
    else {
        update(tree, C1(index), ns, mid, rs, mid, v);
        update(tree, C2(index), mid + 1, ne, mid + 1, re, v);
    }
    // now up-propagate.
    if (tree[C1(index)].max_v > tree[C2(index)].max_v) {
        fprintf(stderr, "C1\n");
        tree[index].max_v = tree[C1(index)].max_v;
        tree[index].num_v = tree[C1(index)].num_v;
    } else if (tree[C1(index)].max_v < tree[C2(index)].max_v) {
        fprintf(stderr, "C2\n");
        tree[index].max_v = tree[C2(index)].max_v;
        tree[index].num_v = tree[C2(index)].num_v;
    } else {
        fprintf(stderr, "BB\n");
        tree[index].max_v = tree[C1(index)].max_v;
        tree[index].num_v = tree[C1(index)].num_v + tree[C2(index)].num_v;
    }
    fprintf(stderr, "upd done: %d max_v %d num_v %d\n", index, tree[index].max_v, tree[index].num_v);
}

int main() {
    int n;
    scanf("%d\n", &n);

    struct node nodes[n];
    struct edge edges[n-1];
    int nl = 0;
    memset(nodes, 0, sizeof(nodes));
    memset(edges, 0, sizeof(edges));
    for (int i = 0; i < n-1; i++) {
        int e1, e2;
        scanf("%d %d\n", &e1, &e2);
        if (e1 < e2) {
            edges[i].a = e1;
            edges[i].b = e2;
        } else {
            edges[i].a = e2;
            edges[i].b = e1;         
        }
    }
    qsort(edges, n-1, sizeof(struct edge), ecmp);
    for (int i = 0; i < n; i++) {
        nodes[i].nn = i+1;
    }
    int cur_node = -1;
    for (int i = 0; i < n-1; i++) {
        fprintf(stderr, "Edge %d: %d %d\n", i, edges[i].a, edges[i].b);
        if (edges[i].b - 1 > cur_node) {
            for (int j = cur_node + 1; j < edges[i].b - 1; j++) {
                // Make the zero-edge nodes have a "first edge" that makes sense
                nodes[j].first_edge = i;
            }
            if (cur_node >= 0) {
                nodes[cur_node].n_edges = i - nodes[cur_node].first_edge;
            }
            cur_node = edges[i].b - 1;
            nodes[cur_node].first_edge = i;
        }
    }
    fprintf(stderr, "n:%d, cur_node %d %d\n", n, cur_node, nodes[cur_node].nn);
    nodes[cur_node].n_edges = n - 1 - nodes[cur_node].first_edge;
    while (++cur_node < n) {
        nodes[cur_node].first_edge = n - 1;
    }
    for (int i = 0; i < n; i++) {
        fprintf(stderr, "Node: %d edges start at %d nedges %d\n", nodes[i].nn, nodes[i].first_edge, nodes[i].n_edges);
    }
    long result = 0;
    treelim = 1<<((int)ceil(log2(n)) + 1);
    struct segment_node stree[treelim];
    memset(stree, 0, sizeof(stree));
    for (int i = 0; i < n; i++) {
        for (int j = nodes[i].first_edge; j < nodes[i].first_edge + nodes[i].n_edges; j++) {
            update(stree, 0, 1, n, 1, edges[j].a, 1);
        }
        // Adds the current vertex.
        update(stree, 0, 1, n, nodes[i].nn, nodes[i].nn, nodes[i].nn);
        fprintf(stderr, "Node %d max_v %d num_v %d\n", nodes[i].nn, stree[0].max_v, stree[0].num_v);
        if (stree[0].max_v == nodes[i].nn) result += stree[0].num_v;
    }
    printf("%ld\n", result);
    return 0;
}
