#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#define N 1000000
#define MAX_ADDS 32          // visited buckets in one j-step are small (<= ~25)
#define TRANSIENT_LIMIT 8    // number of steps before we assume we reached FIXED (usually <= 2)

static inline int popc32(uint32_t x) { return __builtin_popcount(x); }

/* ------------ Fast Input ------------ */
typedef struct {
    unsigned char *buf;
    size_t idx, size;
} FastIn;

static FastIn IN;

static void init_fastin() {
    IN.size = 1 << 20;
    IN.buf = (unsigned char*)malloc(IN.size);
    IN.idx = 0;
    IN.size = fread(IN.buf, 1, IN.size, stdin);
}

static inline int refill() {
    IN.idx = 0;
    IN.size = fread(IN.buf, 1, (1 << 20), stdin);
    return IN.size > 0;
}

static inline int read_int(int *out) {
    int c;
    do {
        if (IN.idx >= IN.size && !refill()) return 0;
        c = IN.buf[IN.idx++];
    } while (c <= ' ');

    int sign = 1;
    if (c == '-') { sign = -1; 
        if (IN.idx >= IN.size && !refill()) return 0;
        c = IN.buf[IN.idx++];
    }

    int val = 0;
    while (c > ' ') {
        val = val * 10 + (c - '0');
        if (IN.idx >= IN.size && !refill()) break;
        c = IN.buf[IN.idx++];
    }
    *out = val * sign;
    return 1;
}

static inline int read_char(char *out) {
    int c;
    do {
        if (IN.idx >= IN.size && !refill()) return 0;
        c = IN.buf[IN.idx++];
    } while (c <= ' ');
    *out = (char)c;
    return 1;
}

/* ------------ Fenwick Tree ------------ */
static int64_t *BIT;

static inline void bit_add(int idx, int64_t delta) {
    for (int i = idx; i <= N; i += (i & -i)) BIT[i] += delta;
}

static inline int64_t bit_sum(int idx) {
    int64_t s = 0;
    for (int i = idx; i > 0; i -= (i & -i)) s += BIT[i];
    return s;
}

static inline int64_t bit_range(int l, int r) {
    return bit_sum(r) - bit_sum(l - 1);
}

/* ------------ Transition memoization (exact) ------------ */
typedef struct {
    uint32_t next;
    uint8_t len;
    uint32_t adds[MAX_ADDS];
    uint8_t ready;
} StepInfo;

static StepInfo *STEP;

/*
 * Exact one j-iteration, matching the pseudocode:
 * add at pos
 * in = popcount(pos)
 * for k=0..:
 *   s = pos + 2^k
 *   if popcount(s) <= in:
 *      in = popcount(s)
 *      pos = s
 *      if pos > N: break
 *      add at pos
 * pos = pos - N (if exceeded)
 */
static inline void compute_step(uint32_t pos) {
    StepInfo *si = &STEP[pos];
    if (si->ready) return;

    uint32_t p = pos;
    uint32_t adds[MAX_ADDS];
    int len = 0;

    adds[len++] = p;
    int inb = popc32(p);

    for (int k = 0; k < 25; k++) {
        uint32_t s = p + (1u << k);
        int pc = popc32(s);
        if (pc <= inb) {
            inb = pc;
            p = s;
            if (p > (uint32_t)N) break;
            if (len < MAX_ADDS) adds[len++] = p;
        }
    }

    if (p > (uint32_t)N) p -= (uint32_t)N;

    si->next = p;
    si->len = (uint8_t)len;
    for (int i = 0; i < len; i++) si->adds[i] = adds[i];
    si->ready = 1;
}

/* Find a fixed point of next(pos): next(FIXED)=FIXED */
static uint32_t find_fixed_point() {
    uint32_t p = 1;
    for (int i = 0; i < 64; i++) {
        compute_step(p);
        uint32_t np = STEP[p].next;
        if (np == p) return p;
        p = np;
    }
    /* fallback: walk until repeat */
    uint8_t *seen = (uint8_t*)calloc(N + 1, 1);
    p = 1;
    while (!seen[p]) {
        seen[p] = 1;
        compute_step(p);
        p = STEP[p].next;
    }
    free(seen);
    return p;
}

/* ------------ Per-update accumulator (no hash map) ------------ */
static int64_t *delta;
static uint32_t *vis;
static uint32_t stamp_id = 0;
static uint32_t touched[200000];   // plenty; actual touched is usually a few thousand
static int touched_sz;

/* mark+add in O(1) */
static inline void acc_add(uint32_t idx, int64_t val) {
    if (vis[idx] != stamp_id) {
        vis[idx] = stamp_id;
        touched[touched_sz++] = idx;
    }
    delta[idx] += val;
}

int main() {
    init_fastin();

    BIT = (int64_t*)calloc(N + 1, sizeof(int64_t));
    STEP = (StepInfo*)calloc(N + 1, sizeof(StepInfo));
    delta = (int64_t*)calloc(N + 1, sizeof(int64_t));
    vis = (uint32_t*)calloc(N + 1, sizeof(uint32_t));

    int Q;
    if (!read_int(&Q)) return 0;

    /* precompute fixed point + its adds */
    uint32_t FIXED = find_fixed_point();
    compute_step(FIXED);
    StepInfo fixedInfo = STEP[FIXED];

    /* output buffer */
    char *out = (char*)malloc((size_t)Q * 24);
    size_t out_len = 0;

    for (int qi = 0; qi < Q; qi++) {
        char type;
        read_char(&type);

        if (type == 'R') {
            int l, r;
            read_int(&l); read_int(&r);
            int64_t ans = bit_range(l, r);
            out_len += (size_t)sprintf(out + out_len, "%lld\n", (long long)ans);
        } else { /* 'U' */
            int pos0_i, M_i, plus_i;
            read_int(&pos0_i);
            read_int(&M_i);
            read_int(&plus_i);

            uint32_t pos0 = (uint32_t)pos0_i;
            int64_t M = (int64_t)M_i;
            uint32_t plus = (uint32_t)plus_i;

            stamp_id++;
            touched_sz = 0;

            uint32_t pos = pos0;

            for (int ii = 0; ii < 50; ii++) {
                uint32_t back = pos;

                /* do transient steps until reaching FIXED (usually in 1-2) */
                uint32_t cur = pos;
                int steps = 0;

                while (steps < 1000 && cur != FIXED && steps < TRANSIENT_LIMIT) {
                    compute_step(cur);
                    StepInfo *si = &STEP[cur];
                    for (int t = 0; t < si->len; t++) acc_add(si->adds[t], M);
                    cur = si->next;
                    steps++;
                }

                /* bulk remaining steps at FIXED */
                if (steps < 1000) {
                    int rem = 1000 - steps;
                    int64_t bulk = M * (int64_t)rem;
                    for (int t = 0; t < fixedInfo.len; t++) acc_add(fixedInfo.adds[t], bulk);
                    cur = FIXED;
                }

                /* next outer iteration starts from back + plus (wrap once) */
                pos = back + plus;
                if (pos > (uint32_t)N) pos -= (uint32_t)N;
            }

            /* apply accumulated updates to BIT */
            for (int i = 0; i < touched_sz; i++) {
                uint32_t idx = touched[i];
                int64_t d = delta[idx];
                if (d) {
                    bit_add((int)idx, d);
                    delta[idx] = 0;
                }
            }
        }
    }

    fwrite(out, 1, out_len, stdout);

    free(out);
    free(vis);
    free(delta);
    free(STEP);
    free(BIT);
    free(IN.buf);
    return 0;
}
