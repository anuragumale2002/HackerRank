#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#define MOD 1000000007LL

// ---------------- Fast IO ----------------
typedef struct {
    unsigned char *buf;
    size_t idx, size;
} FastIn;

static FastIn IN;

static void init_fastin() {
    IN.buf = (unsigned char*)malloc(1 << 20);
    IN.idx = 0;
    IN.size = fread(IN.buf, 1, 1 << 20, stdin);
}

static inline int refill() {
    IN.idx = 0;
    IN.size = fread(IN.buf, 1, 1 << 20, stdin);
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
    long long val = 0;
    while (c > ' ') {
        val = val * 10 + (c - '0');
        if (IN.idx >= IN.size && !refill()) break;
        c = IN.buf[IN.idx++];
    }
    *out = (int)(val * sign);
    return 1;
}

// ---------------- Modular ----------------
static inline long long mod_add(long long a, long long b){ a+=b; if(a>=MOD) a-=MOD; if(a<0) a+=MOD; return a; }
static inline long long mod_mul(long long a, long long b){ return (a*b)%MOD; }

static long long mod_pow(long long a, long long e){
    long long r=1%MOD;
    a%=MOD;
    while(e){
        if(e&1) r=mod_mul(r,a);
        a=mod_mul(a,a);
        e>>=1;
    }
    return r;
}
static inline long long mod_inv(long long a){ return mod_pow(a, MOD-2); }

// ---------------- Graph ----------------
typedef struct Edge { int to, nxt; } Edge;
static int *head;
static Edge *edges;
static int ecnt;

static void add_edge(int u,int v){
    edges[ecnt]=(Edge){v, head[u]};
    head[u]=ecnt++;
}

// ---------------- HLD + LCA ----------------
static int N;
static int *parent_, *depth_, *heavy, *sz_, *head_, *pos_, *invpos;
static int curpos;

static int LOG;
static int **up;

static void build_hld(int root){
    // iterative DFS to get parent/depth/order
    int *stack = (int*)malloc(sizeof(int)*N);
    int *order = (int*)malloc(sizeof(int)*N);
    int sp=0, ord=0;

    stack[sp++]=root;
    parent_[root]=0;
    depth_[root]=0;

    while(sp){
        int u=stack[--sp];
        order[ord++]=u;
        for(int e=head[u]; e!=-1; e=edges[e].nxt){
            int v=edges[e].to;
            if(v==parent_[u]) continue;
            parent_[v]=u;
            depth_[v]=depth_[u]+1;
            stack[sp++]=v;
        }
    }

    // sizes + heavy
    for(int i=ord-1;i>=0;i--){
        int u=order[i];
        sz_[u]=1;
        int best=0;
        heavy[u]=0;
        for(int e=head[u]; e!=-1; e=edges[e].nxt){
            int v=edges[e].to;
            if(v==parent_[u]) continue;
            sz_[u]+=sz_[v];
            if(sz_[v]>best){
                best=sz_[v];
                heavy[u]=v;
            }
        }
    }

    // decompose
    curpos=0;
    int *st_u = (int*)malloc(sizeof(int)*N);
    int *st_h = (int*)malloc(sizeof(int)*N);
    int sp2=0;
    st_u[sp2]=root; st_h[sp2]=root; sp2++;

    while(sp2){
        int u=st_u[--sp2];
        int h=st_h[sp2];

        int x=u;
        while(x){
            head_[x]=h;
            pos_[x]=++curpos;
            invpos[curpos]=x;

            for(int e=head[x]; e!=-1; e=edges[e].nxt){
                int v=edges[e].to;
                if(v==parent_[x] || v==heavy[x]) continue;
                st_u[sp2]=v; st_h[sp2]=v; sp2++;
            }
            x=heavy[x];
        }
    }

    free(stack); free(order);
    free(st_u); free(st_h);
}

static void build_lca(){
    LOG = 0;
    while((1<<LOG) <= N) LOG++;
    up = (int**)malloc(sizeof(int*)*LOG);
    for(int k=0;k<LOG;k++) up[k]=(int*)calloc(N+1,sizeof(int));

    for(int i=1;i<=N;i++) up[0][i]=parent_[i];
    for(int k=1;k<LOG;k++){
        for(int i=1;i<=N;i++){
            int mid=up[k-1][i];
            up[k][i]= mid? up[k-1][mid] : 0;
        }
    }
}

static int lca(int a,int b){
    if(depth_[a]<depth_[b]){ int t=a;a=b;b=t; }
    int diff=depth_[a]-depth_[b];
    for(int k=0; diff; k++){
        if(diff&1) a=up[k][a];
        diff>>=1;
    }
    if(a==b) return a;
    for(int k=LOG-1;k>=0;k--){
        if(up[k][a]!=up[k][b]){
            a=up[k][a];
            b=up[k][b];
        }
    }
    return parent_[a];
}

// ---------------- Segment Tree ----------------
//
// Supports range add of sequence: (p0+p1*i+p2*i^2)*q^i over i=0..len-1
// q is either R or invR.
// We store lazy coefficients separately for q=R and q=invR.
//
static long long *segSum;
static long long *lr0,*lr1,*lr2;
static long long *li0,*li1,*li2;

static long long *powR,*powI;
static long long *S0R,*S1R,*S2R;
static long long *S0I,*S1I,*S2I;

static inline void shift_poly(long long p0,long long p1,long long p2,long long off,
                              long long *o0,long long *o1,long long *o2){
    off%=MOD;
    long long off2 = mod_mul(off, off);
    *o0 = (p0 + mod_mul(p1, off) + mod_mul(p2, off2)) % MOD;
    *o1 = (p1 + mod_mul((2*p2)%MOD, off)) % MOD;
    *o2 = p2 % MOD;
}

static inline void add_to_node(int idx, long long p0,long long p1,long long p2, int useR, int len){
    long long add;
    if(useR){
        lr0[idx]=mod_add(lr0[idx], p0);
        lr1[idx]=mod_add(lr1[idx], p1);
        lr2[idx]=mod_add(lr2[idx], p2);
        add = ( mod_mul(p0,S0R[len]) + mod_mul(p1,S1R[len]) + mod_mul(p2,S2R[len]) ) % MOD;
    }else{
        li0[idx]=mod_add(li0[idx], p0);
        li1[idx]=mod_add(li1[idx], p1);
        li2[idx]=mod_add(li2[idx], p2);
        add = ( mod_mul(p0,S0I[len]) + mod_mul(p1,S1I[len]) + mod_mul(p2,S2I[len]) ) % MOD;
    }
    segSum[idx]=mod_add(segSum[idx], add);
}

static void push(int idx,int l,int r){
    if(l==r){
        lr0[idx]=lr1[idx]=lr2[idx]=0;
        li0[idx]=li1[idx]=li2[idx]=0;
        return;
    }
    int mid=(l+r)>>1;
    int left_len = mid-l+1;
    int right_len = r-mid;

    // push R-lazy
    long long p0=lr0[idx], p1=lr1[idx], p2=lr2[idx];
    if(p0||p1||p2){
        add_to_node(idx<<1, p0,p1,p2, 1, left_len);

        long long sp0,sp1,sp2;
        shift_poly(p0,p1,p2,left_len,&sp0,&sp1,&sp2);
        long long mul = powR[left_len];
        sp0=mod_mul(sp0,mul);
        sp1=mod_mul(sp1,mul);
        sp2=mod_mul(sp2,mul);
        add_to_node(idx<<1|1, sp0,sp1,sp2, 1, right_len);

        lr0[idx]=lr1[idx]=lr2[idx]=0;
    }

    // push invR-lazy
    p0=li0[idx]; p1=li1[idx]; p2=li2[idx];
    if(p0||p1||p2){
        add_to_node(idx<<1, p0,p1,p2, 0, left_len);

        long long sp0,sp1,sp2;
        shift_poly(p0,p1,p2,left_len,&sp0,&sp1,&sp2);
        long long mul = powI[left_len];
        sp0=mod_mul(sp0,mul);
        sp1=mod_mul(sp1,mul);
        sp2=mod_mul(sp2,mul);
        add_to_node(idx<<1|1, sp0,sp1,sp2, 0, right_len);

        li0[idx]=li1[idx]=li2[idx]=0;
    }
}

static void range_add_seq(int idx,int l,int r,int L,int R, int useR,
                          long long p0,long long p1,long long p2){
    if(R<l || r<L) return;
    if(L<=l && r<=R){
        int off = l - L;
        long long sp0,sp1,sp2;
        shift_poly(p0,p1,p2,off,&sp0,&sp1,&sp2);
        long long mul = useR ? powR[off] : powI[off];
        sp0=mod_mul(sp0,mul);
        sp1=mod_mul(sp1,mul);
        sp2=mod_mul(sp2,mul);
        add_to_node(idx, sp0,sp1,sp2, useR, r-l+1);
        return;
    }
    push(idx,l,r);
    int mid=(l+r)>>1;
    range_add_seq(idx<<1,l,mid,L,R,useR,p0,p1,p2);
    range_add_seq(idx<<1|1,mid+1,r,L,R,useR,p0,p1,p2);
    segSum[idx]=mod_add(segSum[idx<<1], segSum[idx<<1|1]);
}

static long long range_sum(int idx,int l,int r,int L,int R){
    if(R<l || r<L) return 0;
    if(L<=l && r<=R) return segSum[idx];
    push(idx,l,r);
    int mid=(l+r)>>1;
    return mod_add(range_sum(idx<<1,l,mid,L,R),
                   range_sum(idx<<1|1,mid+1,r,L,R));
}

// ---------------- Apply one HLD segment update ----------------
static long long Rbase, invR;

static void apply_segment(int useR, int Lpos, int Rpos, long long d0,
                          long long c0,long long c1,long long c2){
    d0%=MOD;
    long long d02 = mod_mul(d0,d0);
    long long base = mod_pow(Rbase, (long long)d0); // R^d0

    if(useR){
        // z=d0+i
        long long P2 = c2%MOD;
        long long P1 = (c1 + mod_mul(2*c2%MOD, d0)) % MOD;
        long long P0 = (c0 + mod_mul(c1,d0) + mod_mul(c2,d02)) % MOD;

        long long p0=mod_mul(P0,base), p1=mod_mul(P1,base), p2=mod_mul(P2,base);
        range_add_seq(1,1,N,Lpos,Rpos,1,p0,p1,p2);
    }else{
        // z=d0-i, exponent uses invR^i
        long long P2 = c2%MOD;
        long long P1 = (-c1 - mod_mul(2*c2%MOD, d0)) % MOD; if(P1<0) P1+=MOD;
        long long P0 = (c0 + mod_mul(c1,d0) + mod_mul(c2,d02)) % MOD;

        long long p0=mod_mul(P0,base), p1=mod_mul(P1,base), p2=mod_mul(P2,base);
        range_add_seq(1,1,N,Lpos,Rpos,0,p0,p1,p2);
    }
}

// update path A->B
static void path_update(int A,int B, long long a1,long long d1,long long a2,long long d2){
    a1%=MOD; d1%=MOD; a2%=MOD; d2%=MOD;
    long long c2 = mod_mul(d1,d2);
    long long c1 = (mod_mul(a1,d2) + mod_mul(a2,d1)) % MOD;
    long long c0 = mod_mul(a1,a2);

    int L = lca(A,B);
    int distAL = depth_[A] - depth_[L];

    // A -> L (inclusive), z decreases => use invR, chain direction top->bottom
    int u=A;
    while(head_[u]!=head_[L]){
        int h=head_[u];
        int Lp=pos_[h], Rp=pos_[u];
        long long d0 = (long long)(depth_[A] - depth_[h]);
        apply_segment(0, Lp, Rp, d0, c0,c1,c2);
        u=parent_[h];
    }
    // same head
    apply_segment(0, pos_[L], pos_[u], (long long)(depth_[A]-depth_[L]), c0,c1,c2);

    // L -> B (exclude L), z increases => use R
    // collect segments from top->bottom
    int v=B;
    // store segments in arrays (since O(logN) count)
    int segL[64], segR[64], sc=0;

    while(head_[v]!=head_[L]){
        int h=head_[v];
        segL[sc]=pos_[h];
        segR[sc]=pos_[v];
        sc++;
        v=parent_[h];
    }
    if(v!=L){
        segL[sc]=pos_[L]+1;
        segR[sc]=pos_[v];
        sc++;
    }

    // apply in reverse? These segs are already top->bottom on each chain,
    // and the overall order from L downward is the reverse of how we collected (from B up).
    // So apply from sc-1 downto 0.
    for(int i=sc-1;i>=0;i--){
        int lpos=segL[i], rpos=segR[i];
        int topnode = invpos[lpos];
        long long d0 = (long long)distAL + (long long)(depth_[topnode] - depth_[L]);
        apply_segment(1, lpos, rpos, d0, c0,c1,c2);
    }
}

static long long path_sum(int a,int b){
    long long res=0;
    while(head_[a]!=head_[b]){
        if(depth_[head_[a]] < depth_[head_[b]]){
            int t=a;a=b;b=t;
        }
        res = mod_add(res, range_sum(1,1,N, pos_[head_[a]], pos_[a]));
        a = parent_[head_[a]];
    }
    if(depth_[a] > depth_[b]){
        int t=a;a=b;b=t;
    }
    res = mod_add(res, range_sum(1,1,N, pos_[a], pos_[b]));
    return res;
}

// ---------------- Main ----------------
int main(){
    init_fastin();

    int Rtmp;
    read_int(&N);
    read_int(&Rtmp);
    Rbase = (long long)Rtmp % MOD;
    invR = mod_inv(Rbase);

    head = (int*)malloc((N+1)*sizeof(int));
    head_ = head;
    head = NULL;

    head_ = (int*)malloc((N+1)*sizeof(int));
    head = head_; // alias

    // graph
    head = (int*)malloc((N+1)*sizeof(int));
    for(int i=1;i<=N;i++) head[i]=-1;
    edges = (Edge*)malloc(sizeof(Edge)*2*(N-1));
    ecnt=0;

    for(int i=0;i<N-1;i++){
        int x,y;
        read_int(&x); read_int(&y);
        add_edge(x,y);
        add_edge(y,x);
    }

    parent_ = (int*)calloc(N+1,sizeof(int));
    depth_  = (int*)calloc(N+1,sizeof(int));
    heavy   = (int*)calloc(N+1,sizeof(int));
    sz_     = (int*)calloc(N+1,sizeof(int));
    head_   = (int*)calloc(N+1,sizeof(int));
    pos_    = (int*)calloc(N+1,sizeof(int));
    invpos  = (int*)calloc(N+1,sizeof(int));

    build_hld(1);
    build_lca();

    // segment tree arrays
    int SZ = 4*N + 5;
    segSum = (long long*)calloc(SZ,sizeof(long long));
    lr0 = (long long*)calloc(SZ,sizeof(long long));
    lr1 = (long long*)calloc(SZ,sizeof(long long));
    lr2 = (long long*)calloc(SZ,sizeof(long long));
    li0 = (long long*)calloc(SZ,sizeof(long long));
    li1 = (long long*)calloc(SZ,sizeof(long long));
    li2 = (long long*)calloc(SZ,sizeof(long long));

    // precompute pow and sums up to N
    powR = (long long*)malloc((N+1)*sizeof(long long));
    powI = (long long*)malloc((N+1)*sizeof(long long));
    powR[0]=1; powI[0]=1;
    for(int i=1;i<=N;i++){
        powR[i]=mod_mul(powR[i-1], Rbase);
        powI[i]=mod_mul(powI[i-1], invR);
    }

    S0R = (long long*)calloc(N+1,sizeof(long long));
    S1R = (long long*)calloc(N+1,sizeof(long long));
    S2R = (long long*)calloc(N+1,sizeof(long long));
    S0I = (long long*)calloc(N+1,sizeof(long long));
    S1I = (long long*)calloc(N+1,sizeof(long long));
    S2I = (long long*)calloc(N+1,sizeof(long long));

    for(int i=0;i<N;i++){
        long long qiR = powR[i];
        long long qiI = powI[i];
        S0R[i+1]=mod_add(S0R[i], qiR);
        S1R[i+1]=mod_add(S1R[i], mod_mul((long long)i, qiR));
        S2R[i+1]=mod_add(S2R[i], mod_mul(mod_mul((long long)i,(long long)i), qiR));

        S0I[i+1]=mod_add(S0I[i], qiI);
        S1I[i+1]=mod_add(S1I[i], mod_mul((long long)i, qiI));
        S2I[i+1]=mod_add(S2I[i], mod_mul(mod_mul((long long)i,(long long)i), qiI));
    }

    int U,Q;
    read_int(&U); read_int(&Q);

    // apply all updates
    for(int k=0;k<U;k++){
        int a1,d1,a2,d2,A,B;
        read_int(&a1); read_int(&d1); read_int(&a2); read_int(&d2); read_int(&A); read_int(&B);
        path_update(A,B, (long long)a1, (long long)d1, (long long)a2, (long long)d2);
    }

    // answer queries
    // output buffer
    char *out = (char*)malloc((size_t)Q * 24);
    size_t out_len=0;
    for(int k=0;k<Q;k++){
        int i,j;
        read_int(&i); read_int(&j);
        long long ans = path_sum(i,j) % MOD;
        out_len += (size_t)sprintf(out + out_len, "%lld\n", ans);
    }
    fwrite(out, 1, out_len, stdout);

    return 0;
}
