#include <stdio.h>
#include <stdlib.h>
#include <limits.h>
#include <stdint.h>

typedef long long ll;

/* Fast input */
static const int IN_BUF = 1 << 20;
static unsigned char ibuf[1 << 20];
static int ipos = 0, ilen = 0;

static inline int read_byte(void) {
    if (ipos >= ilen) {
        ilen = (int)fread(ibuf, 1, IN_BUF, stdin);
        ipos = 0;
        if (ilen == 0) return -1;
    }
    return ibuf[ipos++];
}

static inline ll read_ll(void) {
    int c;
    do { c = read_byte(); } while (c <= ' ' && c != -1);
    ll sign = 1;
    if (c == '-') { sign = -1; c = read_byte(); }
    ll x = 0;
    while (c > ' ') {
        x = x * 10 + (c - '0');
        c = read_byte();
    }
    return x * sign;
}

/* Fast output */
static char *obuf;
static int opos = 0;

static inline void write_ll(ll x) {
    if (x == 0) {
        obuf[opos++] = '0';
        obuf[opos++] = '\n';
        return;
    }
    if (x < 0) {
        obuf[opos++] = '-';
        x = -x;
    }
    char s[32];
    int n = 0;
    while (x) {
        s[n++] = (char)('0' + (x % 10));
        x /= 10;
    }
    while (n--) obuf[opos++] = s[n];
    obuf[opos++] = '\n';
}

/* Correct floor division for C */
static inline ll floordiv(ll a, ll d) {
    ll q = a / d;
    ll r = a % d;
    if (r != 0 && a < 0) q--;
    return q;
}

/* Segment tree */
static ll *lazy, *segMin, *segMax, *segSum;
static int N;

static inline ll llmin(ll a, ll b) { return a < b ? a : b; }
static inline ll llmax(ll a, ll b) { return a > b ? a : b; }

static inline void apply_add(int v, ll add, int len) {
    lazy[v] += add;
    segSum[v] += add * (ll)len;
    segMin[v] += add;
    segMax[v] += add;
}

static inline void push(int v, int l, int r) {
    if (!lazy[v] || l == r) return;
    int mid = (l + r) >> 1;
    apply_add(v << 1, lazy[v], mid - l + 1);
    apply_add(v << 1 | 1, lazy[v], r - mid);
    lazy[v] = 0;
}

static inline void pull(int v) {
    segSum[v] = segSum[v << 1] + segSum[v << 1 | 1];
    segMin[v] = llmin(segMin[v << 1], segMin[v << 1 | 1]);
    segMax[v] = llmax(segMax[v << 1], segMax[v << 1 | 1]);
}

static void build(int v, int l, int r, ll *a) {
    if (l == r) {
        segSum[v] = segMin[v] = segMax[v] = a[l];
        return;
    }
    int mid = (l + r) >> 1;
    build(v << 1, l, mid, a);
    build(v << 1 | 1, mid + 1, r, a);
    pull(v);
}

static void range_add(int v, int l, int r, int ql, int qr, ll c) {
    if (qr < l || r < ql) return;
    if (ql <= l && r <= qr) {
        apply_add(v, c, r - l + 1);
        return;
    }
    push(v, l, r);
    int mid = (l + r) >> 1;
    range_add(v << 1, l, mid, ql, qr, c);
    range_add(v << 1 | 1, mid + 1, r, ql, qr, c);
    pull(v);
}

/* Divide using the same trick as your friend's solution */
static void range_div(int v, int l, int r, int ql, int qr, ll d) {
    if (qr < l || r < ql || d == 1) return;

    if (ql <= l && r <= qr) {
        ll mn = segMin[v];
        ll mx = segMax[v];
        if (mx - mn <= 1) {
            ll dm = floordiv(mn, d) - mn;
            ll dx = floordiv(mx, d) - mx;
            if (dm == dx) {
                apply_add(v, dm, r - l + 1);
                return;
            }
        }
    }

    if (l == r) {
        ll val = floordiv(segSum[v], d);
        segSum[v] = segMin[v] = segMax[v] = val;
        lazy[v] = 0;
        return;
    }

    push(v, l, r);
    int mid = (l + r) >> 1;
    range_div(v << 1, l, mid, ql, qr, d);
    range_div(v << 1 | 1, mid + 1, r, ql, qr, d);
    pull(v);
}

static ll query_min(int v, int l, int r, int ql, int qr) {
    if (qr < l || r < ql) return LLONG_MAX;
    if (ql <= l && r <= qr) return segMin[v];
    push(v, l, r);
    int mid = (l + r) >> 1;
    return llmin(
        query_min(v << 1, l, mid, ql, qr),
        query_min(v << 1 | 1, mid + 1, r, ql, qr)
    );
}

static ll query_sum(int v, int l, int r, int ql, int qr) {
    if (qr < l || r < ql) return 0;
    if (ql <= l && r <= qr) return segSum[v];
    push(v, l, r);
    int mid = (l + r) >> 1;
    return query_sum(v << 1, l, mid, ql, qr) +
           query_sum(v << 1 | 1, mid + 1, r, ql, qr);
}

int main(void) {
    int n = (int)read_ll();
    int q = (int)read_ll();
    N = n;

    ll *a = (ll*)malloc(sizeof(ll) * n);
    for (int i = 0; i < n; i++) a[i] = read_ll();

    int SZ = 4 * n + 5;
    lazy   = (ll*)calloc(SZ, sizeof(ll));
    segMin = (ll*)malloc(sizeof(ll) * SZ);
    segMax = (ll*)malloc(sizeof(ll) * SZ);
    segSum = (ll*)malloc(sizeof(ll) * SZ);

    build(1, 0, n - 1, a);

    obuf = (char*)malloc((size_t)q * 32 + 64);

    for (int i = 0; i < q; i++) {
        int t = (int)read_ll();
        int l = (int)read_ll();
        int r = (int)read_ll();
        if (t == 1) {
            ll c = read_ll();
            range_add(1, 0, n - 1, l, r, c);
        } else if (t == 2) {
            ll d = read_ll();
            range_div(1, 0, n - 1, l, r, d);
        } else if (t == 3) {
            write_ll(query_min(1, 0, n - 1, l, r));
        } else {
            write_ll(query_sum(1, 0, n - 1, l, r));
        }
    }

    fwrite(obuf, 1, opos, stdout);
    return 0;
}
