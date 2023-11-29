#ifndef _DSHARE_H
 #define _DSHARE_H
#include "share.h"
#include "func.h"
#include "compare.h"

extern long total_perm;

//extern long send_1, send_2, send_3, send_4, send_5;


/////////////////////////////////////////////////
// 置換 (平文) 0, 1, ..., n-1
/////////////////////////////////////////////////
typedef packed_array perm;

typedef struct dshare {
// public
  int n;
  share_t q;       // 配列の要素の位数
  int bs;

// P0
  perm pi;
  perm p1, p2p;
  perm p2, p1p;

// P1, P2
  perm g, gp;


/////////////////
// correlated_random
/////////////////

// P0
  perm a1, b1;
  perm a2, b2;

// P1, P2
  perm a, b;

}* dshare;

static perm perm_id(int n)
{
  if (_party >  2) return NULL;
  perm pi;
  int i;
  int k = blog(n-1)+1;
  pi = pa_new(n, k);

  for (i=0; i<n; i++) pa_set(pi, i, i);

  return pi;
}

static void perm_print(int n, perm pi)
{
  if (_party >  2) return;
  int i;
  printf("(");
  for (i=0; i<n; i++) {
    printf("%d", (int)pa_get(pi, i));
    if (i < n-1) printf(" ");
  }
  printf(")\n");
}

static void perm_free(perm pi)
{
  if (_party >  2);
  pa_free(pi);
}


static perm perm_inverse(perm pi)
{
  if (_party >  2) return NULL;
  perm pi_inv = perm_id(pi->n);

  int n = pi->n;
  for (int i=0; i<n; i++) {
    if ((pa_get(pi, i) < 0) || (pa_get(pi, i) >= (u64)n)) {
      printf("pi[%d] = %d", i, (int)pa_get(pi, i));
      exit(1);
    }
    pa_set(pi_inv, pa_get(pi, i) % n, i);
  }

  return pi_inv;
}

//////////////////////////////////////////////////////////////////////
// ランダムな置換 (平文)
//////////////////////////////////////////////////////////////////////
static perm perm_random(MT mt, int n)
{
  if (_party >  2) return NULL;
  perm pi = perm_id(n);
  perm pi2 = perm_id(n);
  int i, j, m;
//  share_t v1, v2;

  for (m=0; m<n; m++) {
  //  i = RANDOM0(n-m);
    i = RANDOM(mt, n-m);
    j = pa_get(pi2, i);
    pa_set(pi, j, m);
    pa_set(pi2, i, pa_get(pi2, n-1-m));
  }
  pa_free(pi2);
//  printf("perm_random: ");  perm_print(n, pi);
  return pi;
}

static _ share_random_perm(int n)
{
  if (_party >  2) return NULL;
  int k = blog(n-1)+1;
  _ ans = share_const(n, 0, 1<<k);
  if (_party <= 0) {
    perm p = perm_random(mt0, n);
    for (int i=0; i<n; i++) {
      pa_set(ans->A, i, pa_get(p, i));
    }
    perm_free(p);
  }
  return ans;
}
#define _random_perm share_random_perm


/////////////////////////////////////////////////////
// 置換 q に対し p・q を計算
/////////////////////////////////////////////////////
static perm block_perm_apply(int bs, perm p, perm q) {
  if (_party >  2) return NULL;
    perm pq;
    int k = p->w;
    int n = q->n;
    pq = pa_new(n*bs, k);
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < bs; ++j) {
            pa_set(pq, i*bs + j, pa_get(p, pa_get(q, i)*bs + j));
        }
    }
    return pq;
}
#define perm_apply(p, q) block_perm_apply(1, p, q)

static share_array block_share_perm(int bs, _ x, perm pi) {
  if (_party >  2) return NULL;
  if (x->n/bs != pi->n) {
    printf("block_share_perm: x->n %d pi->n %ld\n", x->n, pi->n);
  }
  _ ans = _dup(x);
  int n = len(x)/bs;
  for (int i = 0; i < n; ++i) {
    for (int j = 0; j < bs; ++j) {
      _setshare(ans, i*bs + j, x, pa_get(pi, i) * bs + j);
    }
  }
  return ans;
}
#define share_perm(a, pi) block_share_perm(1, a, pi) 



/////////////////////////////////////////////////////////////////////////////
// dshare の相関乱数をオンラインで計算する
/////////////////////////////////////////////////////////////////////////////
static void block_dshare_correlated_random_channel(dshare ds, int channel) {
  if (_party >  2) return;
    int bs = ds->bs;
    int n = ds->n;
    share_t q = ds->q;
    int k = blog(q - 1) + 1;
    if (_party <= 0) {
        ds->a1 = pa_new(n*bs, k);
        ds->a2 = pa_new(n*bs, k);
        perm c = pa_new(n*bs, k);

        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            pa_set(ds->a1, i*bs+j, RANDOM(mt1[channel], q));
          }
        }
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            pa_set(ds->a2, i*bs+j, RANDOM(mt2[channel], q));
          }
        }
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            pa_set(c, i*bs+j, RANDOM(mt0, q));
          }
        }
        ds->b1 = block_perm_apply(bs, ds->a2, ds->p1p);
        ds->b2 = block_perm_apply(bs, ds->a1, ds->p2p);

        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            int p = i*bs+j;
            pa_set(ds->b1, p, MOD(pa_get(ds->b1, p) + pa_get(c, p)));
            pa_set(ds->b2, p, MOD(pa_get(ds->b2, p) - pa_get(c, p)));
          }
        }

        perm_free(c);

        if (_party == 0) {
            mpc_send(channel*2+TO_PARTY1, ds->b1->B, pa_size(ds->b1));    send_3 += pa_size(ds->b1);
            mpc_send(channel*2+TO_PARTY2, ds->b2->B, pa_size(ds->b2));
        }
    }
    else {  // party 1, 2
        ds->a = pa_new(n*bs, k);
        ds->b = pa_new(n*bs, k);
        
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            int p = i*bs+j;
            pa_set(ds->a, p, RANDOM(mts[channel], q));
          }
        }
        mpc_recv(channel*2+FROM_SERVER, (char *)ds->b->B, pa_size(ds->b));
    }
}
//#define block_dshare_correted_random(bs, ds) block_dshare_correlated_random_channel(bs, ds, 0)
#define dshare_correlated_random_channel(ds, channel) block_dshare_correlated_random_channel(ds, channel)
#define dshare_correlated_random(ds) dshare_correlated_random_channel(ds, 0)

///////////////////////////////////////////////////////////////////////////////////
// dshare をオンラインで計算する
// ds はここでは使わない
///////////////////////////////////////////////////////////////////////////////////
static dshare block_dshare_new2_channel(int bs, perm pi, share_t q, int channel) {
  if (_party >  2) return NULL;
    NEWT(dshare, ds);
    int n = pi->n;
    ds->n = n;
    ds->q = q;
    ds->bs = bs;
    if (_party <= 0) {
        ds->pi = perm_id(n);
        for (int i = 0; i < n; ++i) {
            pa_set(ds->pi, i, pa_get(pi, i));
        }

        perm p1_inv, p2_inv;
        ds->p1 = perm_random(mt1[channel], n);
        p1_inv = perm_inverse(ds->p1);
        ds->p2p = perm_apply(p1_inv, pi);

        ds->p2 = perm_random(mt2[channel], n);
        p2_inv = perm_inverse(ds->p2);
        ds->p1p = perm_apply(p2_inv, pi);
        perm_free(p1_inv);
        perm_free(p2_inv);

        if (_party == 0) {
            mpc_send(channel*2+TO_PARTY1, ds->p1p->B, pa_size(ds->p1p));  //send_4 += pa_size(ds->p1p);
            mpc_send(channel*2+TO_PARTY2, ds->p2p->B, pa_size(ds->p2p));
        }
    }
    else {
        ds->g = perm_random(mts[channel], n);
        ds->gp = perm_id(n);
        mpc_recv(channel*2+FROM_SERVER, (char *)ds->gp->B, pa_size(ds->gp));
    }

//    block_dshare_correlated_random_channel(bs, ds, channel);

    return ds;
}


///////////////////////////////////////////////////////////////////////////////////
// dshare をオンラインで計算する
///////////////////////////////////////////////////////////////////////////////////
static dshare block_dshare_new_channel(int bs, perm pi, share_t q, int channel)
{
  dshare ds = block_dshare_new2_channel(bs, pi, q, channel);
  block_dshare_correlated_random_channel(ds, channel);
  return ds;
}
#define dshare_new_channel(pi, q, channel) block_dshare_new_channel(1, pi, q, channel)
#define dshare_new(pi, q) dshare_new_channel(pi, q, 0)
#define block_dshare_new(bs, pi, q) block_dshare_new_channel(bs, pi, q, 0)

static dshare block_dshare_new_party0(int bs, int n, share_t q)
{
  if (_party >  2) return NULL;

  NEWT(dshare, ds);
  ds->n = n;
  ds->q = q;
  ds->bs = bs;

  ds->pi = perm_id(n);

  perm p1_inv, p2_inv;
  ds->p1 = perm_id(n);
  ds->p2p = perm_id(n);

  ds->p2 = perm_id(n);
  ds->p1p = perm_id(n);


  int k = blog(q-1)+1;

  ds->a1 = pa_new(n*bs, k);
  ds->a2 = pa_new(n*bs, k);
  for (int i=0; i<n*bs; i++) {
    pa_set(ds->a1, i, 0);
  }
  for (int i=0; i<n*bs; i++) {
    pa_set(ds->a2, i, 0);
  }
  ds->b1 = block_perm_apply(bs, ds->a2, ds->p1p);
  ds->b2 = block_perm_apply(bs, ds->a1, ds->p2p);

  return ds;
}
#define dshare_new_party0(n, q) block_dshare_new_party0(1, n, q)

///////////////////////////////////////////
// 順列のみ生成．加える乱数は別に作る．
///////////////////////////////////////////
static dshare dshare_new2_channel(perm pi, share_t q, int channel)
{
  if (_party >  2) return NULL;
  int n = pi->n;
//  printf("Dshare2 n=%d q=%d\n", n, q);
  total_perm++;

  NEWT(dshare, ds);
  ds->n = n;
  ds->q = q;
  ds->bs = 1;
  if (_party <= 0) {
    ds->pi = perm_id(n);
    for (int i=0; i<n; i++) pa_set(ds->pi, i, pa_get(pi, i));

    perm p1_inv, p2_inv;
    ds->p1 = perm_random(mt1[channel], n);
    p1_inv = perm_inverse(ds->p1);
    ds->p2p = perm_apply(p1_inv, pi);

    ds->p2 = perm_random(mt2[channel], n);
    p2_inv = perm_inverse(ds->p2);
    ds->p1p = perm_apply(p2_inv, pi);
    perm_free(p1_inv);
    perm_free(p2_inv);

    mpc_send(channel*2+TO_PARTY1, ds->p1p->B, pa_size(ds->p1p));  send_5 += pa_size(ds->p1p);
    mpc_send(channel*2+TO_PARTY2, ds->p2p->B, pa_size(ds->p2p));
  } else {
    ds->g = perm_random(mts[channel], n);
    ds->gp = perm_id(n);
    mpc_recv(channel*2+FROM_SERVER, (char *)ds->gp->B, pa_size(ds->gp));
  }

  return ds;
}

#define dshare_new2(pi, q) dshare_new2_channel(pi, q, 0)

static void dshare_free(dshare ds)
{
  if (_party >  2) return;
  if (_party <= 0) {
    perm_free(ds->pi);
    perm_free(ds->p1);
    perm_free(ds->p1p);
    perm_free(ds->p2);
    perm_free(ds->p2p);
    perm_free(ds->a1);
    perm_free(ds->b1);
    perm_free(ds->a2);
    perm_free(ds->b2);
  } else {
    perm_free(ds->g);
    perm_free(ds->gp);
    perm_free(ds->a);
    perm_free(ds->b);
  }
  free(ds);
}

///////////////////////////////////////////
// 加える乱数以外を解放
///////////////////////////////////////////
static void dshare_free2(dshare ds)
{
  if (_party >  2) return;
  if (_party <= 0) {
    perm_free(ds->pi);
    perm_free(ds->p1);
    perm_free(ds->p1p);
    perm_free(ds->p2);
    perm_free(ds->p2p);
//    perm_free(ds->a1);
//    perm_free(ds->b1);
//    perm_free(ds->a2);
//    perm_free(ds->b2);
  } else {
    perm_free(ds->g);
    perm_free(ds->gp);
//    perm_free(ds->a);
//    perm_free(ds->b);
  }
  free(ds);
}

///////////////////////////////////////////
// 加える乱数のみを解放
///////////////////////////////////////////
static void dshare_free3(dshare ds)
{
  if (_party >  2) return;
  if (_party <= 0) {
    perm_free(ds->a1);
    perm_free(ds->b1);
    perm_free(ds->a2);
    perm_free(ds->b2);
  } else {
    perm_free(ds->a);
    perm_free(ds->b);
  }
}

/*************************************************************
def dshare_shuffle(X1, X2, p1, p2, p1p, p2p, a1, a2, a1p, a2p):
  n = len(X1)

# P1
  x1 = X1
  v1 = perm_apply(x1, p1)
  i = 0
  while i < n:
    v1[i] += a1[i]
    i += 1

# P2
  x2 = X2
  v2 = perm_apply(x2, p2)
  i = 0
  while i < n:
    v2[i] += a2[i]
    i += 1

# P1
  y1 = perm_apply(v2, p1p)
  i = 0
  while i < n:
    y1[i] -= a1p[i]
    i += 1

# P2
  y2 = perm_apply(v1, p2p)
  i = 0
  while i < n:
    y2[i] -= a2p[i]
    i += 1

  return (y1, y2)
*************************************************************/

/////////////////////////////////////////////////////////////////////////////////////////////
// dshare ds を用いて x を並び替える
/////////////////////////////////////////////////////////////////////////////////////////////
static share_array block_dshare_shuffle_channel(int bs, share_array x, dshare ds, int channel) {
  if (_party >  2) return NULL;
    if (bs != ds->bs) {
      printf("block_dshare_shuffle_channel: bs = %d ds->bs = %d\n", bs, ds->bs);
      exit(1);
    }
    share_t q = order(x);
    share_array v;
    int n = len(x) / bs;
    if (n != ds->n) {
        printf("block_dshare_shuffle_channel: n %d ds->n %d\n", n, ds->n);
        exit(EXIT_FAILURE);
    }

    if (_party <= 0) {
        v = block_share_perm(bs, x, ds->p1);
        // printf("v ok\n");   fflush(stdout);
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            int p = i*bs+j;
            pa_set(v->A, p, MOD(pa_get(v->A, p) + pa_get(ds->a1, p)));
          }
        }
    }
    else {
        v = block_share_perm(bs, x, ds->g);
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            int p = i*bs+j;
            pa_set(v->A, p, MOD(pa_get(v->A, p) + pa_get(ds->a, p)));
          }
        }
    }

    share_array y;
    if (_party <= 0) {
        y = block_share_perm(bs, v, ds->p2p);
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            int p = i*bs+j;
            pa_set(y->A, p, MOD(pa_get(y->A, p) - pa_get(ds->b2, p)));
          }
        }
        perm tmp = block_perm_apply(bs, ds->a2, ds->p1p);
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            int p = i*bs+j;
            pa_set(y->A, p, MOD(pa_get(y->A, p) + pa_get(tmp, p) - pa_get(ds->b1, p)));
          }
        }
        perm_free(tmp);
        // send_8 += pa_size(v->a->A);
    }
    else {
        share_array z = share_dup(v);
        mpc_exchange_channel(v->A->B, z->A->B, pa_size(v->A), channel);
        y = block_share_perm(bs, z, ds->gp);
        for (int i = 0; i < n; ++i) {
          for (int j = 0; j < bs; ++j) {
            int p = i*bs+j;
            pa_set(y->A, p, MOD(pa_get(y->A, p) - pa_get(ds->b, p)));
          }
        }
        _free(z);
    }
    _free(v);

    return y;
}
#define block_dshare_shuffle(bs, x, ds) block_dshare_shuffle_channel(bs, x, ds, 0)
#define dshare_shuffle_channel(X, ds, channel) block_dshare_shuffle_channel(1, X, ds, channel)
#define dshare_shuffle(X, ds) dshare_shuffle_channel(X, ds, 0)

typedef struct {
  int n;
  int bs;
  precomp_table PRG;
  precomp_table pp_1, b_1, pp_2, b_2;
  MMAP *map;
}* DS_tables;

typedef struct ds_tbl_list {
  DS_tables tbl;
  int n;
  int inverse;
  long count;
  struct ds_tbl_list *next;
}* ds_tbl_list;

ds_tbl_list PRE_DS_tbl[NC];
long PRE_DS_count[NC];


//////////////////////////////////////////////////
// dshare の計算 (事前計算)
// n: 順列の長さ
// m: 順列の個数
//////////////////////////////////////////////////
void DS_tables_precomp(int bs, int m, int n, share_t q, int inverse, char *fname)
{
  FILE *f0, *f1, *f2;

//  int kq = blog(q-1)+1;
  int kn = blog(n-1)+1;

  char *fname0 = precomp_fname(fname, 0);
  char *fname1 = precomp_fname(fname, 1);
  char *fname2 = precomp_fname(fname, 2);

  f0 = fopen(fname0, "wb");
  f1 = fopen(fname1, "wb");
  f2 = fopen(fname2, "wb");

  unsigned long init[5]={0x123, 0x234, 0x345, 0x456, 0};
  MT m0 = MT_init_by_array(init, 5);

  // party 1 が使う乱数
  unsigned long init1[5]={0x123, 0x234, 0x345, 0x456, 0};
  init1[4] = 1; // rand();
  mt1[0] = MT_init_by_array(init1, 5); // 注意 この関数は通常の計算中に使ってはならない

  // party 2 が使う乱数
  unsigned long init2[5]={0x123, 0x234, 0x345, 0x456, 0};
  init2[4] = 2; // rand();
  mt2[0] = MT_init_by_array(init2, 5);

  perm g = perm_random(m0, n);
  dshare ds1, ds2;
  share_t qq = max(1<<kn, q);

  if (inverse == 0) {
    perm g_inv = perm_inverse(g);
    ds1 = block_dshare_new(bs, g, 1<<kn);
    ds2 = block_dshare_new(bs, g_inv, q);
    perm_free(g_inv);
  } else {
    ds1 = block_dshare_new(bs, g, qq);
    ds2 = block_dshare_new(bs, g, qq);
  }
  perm_free(g);

  writeuint(sizeof(m), m, f1);
  writeuint(sizeof(m), m, f2);
  writeuint(sizeof(n), n, f1);
  writeuint(sizeof(n), n, f2);
  writeuint(sizeof(bs), bs, f1);
  writeuint(sizeof(bs), bs, f2);
//  precomp_write_seed(f1, n*2, qq, init1); // p1 と a1 を作るために 2n 個の乱数を使う
//  precomp_write_seed(f2, n*2, qq, init2); // p2 と a2
  precomp_write_seed(f1, n*(1+bs), qq, init1);
  precomp_write_seed(f2, n*(1+bs), qq, init2);
  precomp_write_share(f1, ds1->p1p);
  precomp_write_share(f2, ds1->p2p);
  precomp_write_share(f1, ds1->b1);
  precomp_write_share(f2, ds1->b2);
  precomp_write_share(f1, ds2->p1p);
  precomp_write_share(f2, ds2->p2p);
  precomp_write_share(f1, ds2->b1);
  precomp_write_share(f2, ds2->b2);

  MT_free(m0);
  dshare_free(ds1);
  dshare_free(ds2);

  fclose(f0);
  fclose(f1);
  fclose(f2);

  free(fname0);
  free(fname1);
  free(fname2);
}
#define block_dshare_precomp(bs, m, n, q, inverse, fname) DS_tables_precomp(bs, m, n, q, inverse, fname)
#define dshare_precomp(m, n, q, inverse, fname) block_dshare_precomp(1, m, n, q, inverse, fname)


void DS_tables_free(DS_tables T)
{
  if (T == NULL) return;
  if (_party >  2) return;
  if (_party < 0) return;
  precomp_free(T->PRG);
  precomp_free(T->pp_1);
  precomp_free(T->b_1);
  precomp_free(T->pp_2);
  precomp_free(T->b_2);
  if (T->map != NULL) mymunmap(T->map);
  free(T);
}

DS_tables DS_tables_read(char *fname)
{
//  if (_party >  2) return NULL;
//  if (_party <  0) return NULL;

  NEWT(DS_tables, T);

  if (_party <= 0 || _party > 2) {
    T->PRG = T->pp_1 = T->b_1 = T->pp_2 = T->b_2 = NULL;
    T->map = NULL;
    return T;
  }

  char *fname2 = precomp_fname(fname, _party);

  MMAP *map = NULL;
  map = mymmap(fname2);
  uchar *p = (uchar *)map->addr;
  int m = getuint(p, 0, sizeof(int)); p += sizeof(int);
  T->n = getuint(p, 0, sizeof(int)); p += sizeof(int);
  T->bs = getuint(p, 0, sizeof(int)); p += sizeof(int);
  T->PRG = precomp_read(&p);
  T->pp_1 = precomp_read(&p);
  T->b_1 = precomp_read(&p);
  T->pp_2 = precomp_read(&p);
  T->b_2 = precomp_read(&p);
  T->map = map;

  free(fname2);

  return T;
}

#if 0
static void dshare_new_precomp0(DS_tables tbl, int n, share_t q_x, share_t q_sigma, dshare *ds1_, dshare *ds2_)
{
  if (_party >  2) return;
  if (_party <= 0) {
    dshare ds1 = dshare_new_party0(n, q_sigma);
    dshare ds2 = dshare_new_party0(n, q_x);
    *ds1_ = ds1;
    *ds2_ = ds2;
    return;
  }

/////////////////// ランダム順列
  NEWT(dshare, ds1);
  int k_sigma = blog(q_sigma-1)+1;
  ds1->n = n;
  ds1->q = q_sigma;

  ds1->g = perm_random(tbl->PRG->u.seed.r, n);
  ds1->gp = pa_new(n, k_sigma);
  for (int i=0; i<n; i++) {
    pa_set(ds1->gp, i, precomp_get(tbl->pp_1) % q_sigma);
  }
  //ds1->a = pa_new(n, k_x);
  ds1->a = pa_new(n, k_sigma);
  for (int i=0; i<n; i++) {
  //  pa_set(ds1->a, i, precomp_get(tbl->PRG) % q_x);
    pa_set(ds1->a, i, precomp_get(tbl->PRG) % q_sigma);
  }
  //ds1->b = pa_new(n, k_x);
  ds1->b = pa_new(n, k_sigma);
  for (int i=0; i<n; i++) {
  //  pa_set(ds1->b, i, precomp_get(tbl->b_1) % q_x);
    pa_set(ds1->b, i, precomp_get(tbl->b_1) % q_sigma);
  }

/////////////////// 値に加える乱数
  NEWT(dshare, ds2);
  int k_x = blog(q_x-1)+1;
  ds2->n = n;
  ds2->q = q_x;

  ds2->g = perm_random(tbl->PRG->u.seed.r, n);
  ds2->gp = pa_new(n, k_sigma);
  for (int i=0; i<n; i++) {
    pa_set(ds2->gp, i, precomp_get(tbl->pp_2) % q_sigma);
  }
  ds2->a = pa_new(n, k_x);
  for (int i=0; i<n; i++) {
    pa_set(ds2->a, i, precomp_get(tbl->PRG) % q_x);
  }
  ds2->b = pa_new(n, k_x);
  for (int i=0; i<n; i++) {
    pa_set(ds2->b, i, precomp_get(tbl->b_2) % q_x);
  }
  *ds1_ = ds1;  *ds2_ = ds2;
}
#endif

///////////////////////////////////////////////////////////////////
// 事前計算の表から取ってくる
// bs はデータのブロックサイズ．表 tbl のブロックサイズ以下ならば良い
////////////////////////////////////////////////////////////////////////
static void block_dshare_new_precomp(int bs, DS_tables tbl, int n, share_t q_x, share_t q_sigma, dshare *ds1_, dshare *ds2_)
{
  if (_party >  2) return;
  PRE_DS_count[0] += 1; // channel?
  if (_party <= 0) {
    dshare ds1 = dshare_new_party0(n, q_sigma);
    dshare ds2 = block_dshare_new_party0(bs, n, q_x);
    *ds1_ = ds1;
    *ds2_ = ds2;
    return;
  }

/////////////////// ランダム順列
  NEWT(dshare, ds1);
  int k_sigma = blog(q_sigma-1)+1;
  ds1->n = n;
  ds1->q = q_sigma;
  ds1->bs = 1;

  ds1->g = perm_random(tbl->PRG->u.seed.r, n);
  ds1->gp = pa_new(n, k_sigma);
  for (int i=0; i<n; i++) {
    pa_set(ds1->gp, i, precomp_get(tbl->pp_1) % q_sigma);
  }
  //ds1->a = pa_new(n, k_x);
  ds1->a = pa_new(n, k_sigma);
  for (int i=0; i<n; i++) {
  //  pa_set(ds1->a, i, precomp_get(tbl->PRG) % q_x);
    pa_set(ds1->a, i, precomp_get(tbl->PRG) % q_sigma);
  }
  //ds1->b = pa_new(n, k_x);
  ds1->b = pa_new(n, k_sigma);
  for (int i=0; i<n; i++) {
  //  pa_set(ds1->b, i, precomp_get(tbl->b_1) % q_x);
    pa_set(ds1->b, i, precomp_get(tbl->b_1) % q_sigma);
  }

/////////////////// 値に加える乱数
  NEWT(dshare, ds2);
  int k_x = blog(q_x-1)+1;
  ds2->n = n;
  ds2->q = q_x;
//  ds2->bs = tbl->bs;
  ds2->bs = bs;

  ds2->g = perm_random(tbl->PRG->u.seed.r, n);
  ds2->gp = pa_new(n, k_sigma);
  for (int i=0; i<n; i++) {
    pa_set(ds2->gp, i, precomp_get(tbl->pp_2) % q_sigma);
  }
  ds2->a = pa_new(n*bs, k_x);
  //NEWT(share_t*, ptmp);
  share_t *ptmp;
  NEWA(ptmp, share_t, tbl->bs);
  for (int i=0; i<n; i++) {
    for (int j=0; j<tbl->bs; j++) {
      ptmp[j] = precomp_get(tbl->PRG) % q_x;
    }
    for (int j=0; j<bs; j++) {
      int j2 = j % tbl->bs; // 表が足りないときは使いまわす (本当はダメ)
      pa_set(ds2->a, i*bs+j, ptmp[j2]);
    }
    for (int j=bs; j<tbl->bs; j++) {
      precomp_get(tbl->PRG); // skip
    }
  }
  ds2->b = pa_new(n*bs, k_x);
  for (int i=0; i<n; i++) {
    for (int j=0; j<tbl->bs; j++) {
      ptmp[j] = precomp_get(tbl->b_2) % q_x;
    }
    for (int j=0; j<bs; j++) {
      int j2 = j % tbl->bs; // 表が足りないときは使いまわす (本当はダメ)
      pa_set(ds2->b, i*bs+j, ptmp[j2]);
    }
    for (int j=bs; j<tbl->bs; j++) {
      precomp_get(tbl->b_2); // skip
    }
  }
  free(ptmp);
  *ds1_ = ds1;  *ds2_ = ds2;
}
#define dshare_new_precomp(tbl, n, q_x, q_sigma, ds1_, ds2_) block_dshare_new_precomp(1, tbl, n, q_x, q_sigma, ds1_, ds2_)

ds_tbl_list ds_tbl_list_insert(DS_tables tbl, int n, int inverse, ds_tbl_list head)
{
  NEWT(ds_tbl_list, list);
  list->tbl = tbl;
  list->n = n;
  list->inverse = inverse;
  list->count = 0;
  list->next = head;
  return list;
}

////////////////////////////////////////////////////////////////////////
// 長さ n の順列の dshare を返す
////////////////////////////////////////////////////////////////////////
DS_tables ds_tbl_list_search(ds_tbl_list list, int inverse, int n)
{
  DS_tables ans = NULL;
  while (list != NULL) {
  //  printf("list n %d inverse %d\n", list->n, list->inverse);
    if (list->tbl->n == n && list->inverse == inverse) {
      ans = list->tbl;
      break;
    }
    list = list->next;
  }
  return ans;
}

////////////////////////////////////////////////////////////////////////
// n 以上の長さの順列の dshare を返す
////////////////////////////////////////////////////////////////////////
DS_tables ds_tbl_list_search2(ds_tbl_list list, int inverse, int n)
{
  DS_tables ans = NULL;
  while (list != NULL) {
  //  printf("list n %d inverse %d\n", list->n, list->inverse);
    if ((list->n >= n) && (list->n < n*2) && (list->inverse == inverse)) {
      ans = list->tbl;
      break;
    }
    list = list->next;
  }
  return ans;
}

void ds_tbl_list_free(ds_tbl_list list)
{
  ds_tbl_list next;
  while (list != NULL) {
    next = list->next;
    DS_tables_free(list->tbl);
    free(list);
    list = next;
  }
}

void ds_tbl_init(void)
{
  for (int i=0; i<NC; i++) {
    PRE_DS_tbl[i] = NULL;
    PRE_DS_count[i] = 0;
  }
}

void ds_tbl_read(int channel, int n, int inverse, char *fname)
{
  DS_tables tbl = DS_tables_read(fname);
  tbl->n = n; // test
  PRE_DS_tbl[channel] = ds_tbl_list_insert(tbl, n, inverse, PRE_DS_tbl[channel]);
}

//////////////////////////////////////////////////////////////////////////////////////////
// 長さ n の順列を，長さ n2 > n の順列に埋め込んで，事前計算したものを用いる
//////////////////////////////////////////////////////////////////////////////////////////
static share_array block_AppPerm_fwd_offline_channel(DS_tables tbl, int bs, share_array x, share_array sigma, int channel)
{
  dshare ds1;
  dshare ds2;
//  printf("block_AppPerm_fwd_offline_channel: tbl->n %d bs %d len(x) %d len(sigma) %d\n", tbl->n, bs, len(x), len(sigma));
  int n2 = tbl->n;
  int n = len(x) / bs;
//  printf("n %d n2 %d order %d\n", n, n2, order(sigma));
  int k = blog(n2-1)+1;
  _ sigma2 = _const(n2, 0, 1<<k);
  for (int i=0; i<n; i++) {
    pa_set(sigma2->A, i, pa_get(sigma->A, i) % (1<<k));
  }
  for (int i=n; i<n2; i++) _setpublic(sigma2, i, i);
  _ x2 = _const(n2*bs, 0, order(x));
  _setshares(x2, 0, n*bs, x, 0);
  for (int i=n*bs; i<n2*bs; i++) _setpublic(x2, i, 0);
  block_dshare_new_precomp(bs, tbl, n2, order(x2), order(sigma2), &ds1, &ds2);

  _ w;
  _ rho = dshare_shuffle_channel(sigma2, ds1, channel);
  if (_party <= 0) {
      w = block_share_perm(bs, x2, share_raw(rho));
      // send_5 += pa_size(w->A);
  } else {
    _ r = share_reconstruct_channel(rho, channel);
    w = block_share_perm(bs, x2, share_raw(r));
    _free(r);
  }

  _ ans0 = block_dshare_shuffle_channel(bs, w, ds2, channel);
  _ ans = _slice(ans0, 0, n*bs);

  dshare_free(ds1);
  dshare_free(ds2);
  _free(rho);
  _free(w);
  _free(sigma2);
  _free(x2);
  _free(ans0);
    
  return ans;
}

//////////////////////////////////////////////////////////////////////////////////////////
// 長さ n の順列を，長さ n2 > n の順列に埋め込んで，事前計算したものを用いる
//////////////////////////////////////////////////////////////////////////////////////////
static share_array block_AppPerm_inverse_offline_channel(DS_tables tbl, int bs, share_array x, share_array sigma, int channel)
{
  dshare ds1;
  dshare ds2;
//  printf("block_AppPerm_inverse_offline_channel: tbl->n %d bs %d len(x) %d len(sigma) %d\n", tbl->n, bs, len(x), len(sigma));
  int n2 = tbl->n;
  int n = len(x) / bs;
  int k = blog(n2-1)+1;
  _ sigma2 = _const(n2, 0, 1<<k);
  for (int i=0; i<n; i++) {
    pa_set(sigma2->A, i, pa_get(sigma->A, i) % (1<<k));
  }
  for (int i=n; i<n2; i++) _setpublic(sigma2, i, i);
  _ x2 = _const(n2*bs, 0, order(x));
  _setshares(x2, 0, n*bs, x, 0);
  for (int i=n*bs; i<n2*bs; i++) _setpublic(x2, i, 0);
  block_dshare_new_precomp(bs, tbl, n2, order(x2), order(sigma2), &ds1, &ds2);

  _ rho = dshare_shuffle_channel(sigma2, ds1, channel);
  _ z = block_dshare_shuffle_channel(bs, x2, ds2, channel);
  _ r = share_reconstruct_channel(rho, channel);  // send_6 += pa_size(r->A);
  perm rho_inv = perm_inverse(share_raw(r));
  _ ans0 = block_share_perm(bs, z, rho_inv);
  _ ans = _slice(ans0, 0, n*bs);

  _free(r);
  _free(z);
  perm_free(rho_inv);
  _free(rho);
  dshare_free(ds1);
  dshare_free(ds2);
  _free(sigma2);
  _free(x2);
  _free(ans0);
    
  return ans;
}

////////////////////////////////////////////////////////////////////////////////////////////
// 事前計算の表があれば用い，無ければオンラインで計算する
////////////////////////////////////////////////////////////////////////////////////////////
static share_array block_AppPerm_fwd_channel(int bs, share_array x, share_array sigma, int channel)
{
  if (_party >  2) return NULL;
    int n = len(x) / bs;
    if (n != len(sigma)) {
        printf("block_AppPerm_fwd_channel: block_len(x) %d len(sigma) %d\n", n, len(sigma));
    }
    dshare ds1;
    dshare ds2;

    //printf("AppPerm_fwd n = %d\n", n);

    DS_tables tbl;

    if (tbl = ds_tbl_list_search2(PRE_DS_tbl[channel], 0, n)) {
      int n2 = tbl->n;
      //printf("using DS_table n = %d n2 = %d\n", n, n2);
      if (n2 > n) {
        return block_AppPerm_fwd_offline_channel(tbl, bs, x, sigma, channel);
      } else {
        block_dshare_new_precomp(bs, tbl, n, order(x), order(sigma), &ds1, &ds2);
      }
    } else {
        printf("without DS_table n = %d\n", n);
        perm g;
        if (_party == 0) {
            g = perm_random(mt0, n);
        } else {
            g = perm_id(n);
        }
        perm g_inv = perm_inverse(g);

        ds1 = dshare_new_channel(g, order(sigma), channel);
        ds2 = block_dshare_new_channel(bs, g_inv, order(x), channel);
        perm_free(g_inv);
        perm_free(g);
    }
    // ここまでが前計算

    _ w;
    _ rho = dshare_shuffle_channel(sigma, ds1, channel);
    if (_party <= 0) {
        w = block_share_perm(bs, x, share_raw(rho));
        // send_5 += pa_size(w->A);
    }
    else {
        _ r = share_reconstruct_channel(rho, channel);
        w = block_share_perm(bs, x, share_raw(r));
        _free(r);
    }

    _ ans = block_dshare_shuffle_channel(bs, w, ds2, channel);

    dshare_free(ds1);
    dshare_free(ds2);
    _free(rho);
    _free(w);
    
    return ans;
}
#define block_AppPerm_fwd(bs, x, sigma) block_AppPerm_fwd_channel(bs, x, sigma, 0)
#define AppPerm_fwd_channel(x, sigma, channel) block_AppPerm_fwd_channel(1, x, sigma, channel)
#define AppPerm_fwd(x, sigma) AppPerm_fwd_channel(x, sigma, 0)


//static share_array block_AppPerm_channel(int bs, _ x, _ sigma, int channel) {
//  if (_party >  2) return NULL;
//  _ ans = block_AppPerm_fwd_channel(bs, x, sigma, channel);
//  return ans;
//}
#define block_AppPerm(bs, x, sigma) block_AppPerm_fwd_channel(bs, x, sigma, 0)

static void block_AppPerm_channel_(int bs, _ x, _ sigma, int channel) {
  if (_party >  2) return;
  _ ans = block_AppPerm_fwd_channel(bs, x, sigma, channel);
  _move_(x, ans);
}
#define block_AppPerm_(bs, x, sigma) block_AppPerm_channel_(bs, x, sigma, 0)

////////////////////////////////////////////////////////////////////////////////////////////
// 事前計算の表があれば用い，無ければオンラインで計算する
////////////////////////////////////////////////////////////////////////////////////////////
static share_array block_AppPerm_inverse_channel(int bs, share_array x, _ sigma, int channel) {
  if (_party >  2) return NULL;
    int n = len(x) / bs;
    if (n != len(sigma)) {
        printf("block_AppPerm_inverse: block_len(x) %d len(sigma) %d\n", n, len(sigma));
    }

    //printf("AppPerm_inverse n = %d\n", n);

    dshare ds1;
    dshare ds2;

    DS_tables tbl;

    int ln = blog(n-1) + 1;
    if (tbl = ds_tbl_list_search2(PRE_DS_tbl[channel], 1, n)) {
      int n2 = tbl->n;
    //  printf("using DSi_table n = %d n2 = %d\n", n, n2);
      if (n2 > n) {
        return block_AppPerm_inverse_offline_channel(tbl, bs, x, sigma, channel);
      } else {
        block_dshare_new_precomp(bs, tbl, n, order(x), order(sigma), &ds1, &ds2);
      }
    } else {
        printf("without DSi_table n = %d\n", n);
        perm g;
        if (_party == 0) {
            g = perm_random(mt0, n);
        } else {
            g = perm_id(n);
        }

        ds1 = dshare_new_channel(g, order(sigma), channel);
        ds2 = block_dshare_new_channel(bs, g, order(x), channel);
        
        perm_free(g);
    }
    // ここまでが前計算

    _ rho = dshare_shuffle_channel(sigma, ds1, channel);
    // printf("rho ");  share_print(rho);  fflush(stdout);
    share_array z = block_dshare_shuffle_channel(bs, x, ds2, channel);
    // printf("z   ");     share_print(z);  fflush(stdout);
    _ r = share_reconstruct_channel(rho, channel);  // send_6 += pa_size(r->A);
    // printf("r   ");  share_print(r);    fflush(stdout);
    perm rho_inv = perm_inverse(share_raw(r));
    share_array ans = block_share_perm(bs, z, rho_inv);
    // printf("ans "); share_print(ans);  fflush(stdout);
    _free(r);
    _free(z);
    perm_free(rho_inv);
    _free(rho);
    dshare_free(ds1);
    dshare_free(ds2);

    return ans;
}
#define AppPerm_inverse_channel(x, sigma, channel) block_AppPerm_inverse_channel(1, x, sigma, channel)

static void block_AppInvPerm_channel_(int bs, share_array x, _ sigma, int channel) {
  if (_party >  2) return;
    share_array ans = block_AppPerm_inverse_channel(bs, x, sigma, channel);
    _move_(x, ans);
}
#define block_AppInvPerm_(bs, x, sigma) block_AppInvPerm_channel_(bs, x, sigma, 0)


/*****************************************************************
def AppPerm(x, sigma):
  print("AppPerm x", x, "sigma", sigma)
  n = len(x)
  if n != len(sigma):
    print("AppPerm len(x)", len(x), "len(sigma)", len(sigma))
  g = perm_random(n)
#  g = Perm_ID(n)
  print("AppPerm g", g)
  (p1, pi_inv, p2p, p2, p2_inv, p1p) = dshare_new(g)
  (a1, a2, b1, b2, c) = dshare_correlated_random(p1p, p2p)
  X1 = [None] * n
  X2 = [None] * n
  i = 0
  while i < n:
    X1[i] = random.randint(0, n-1)
    X2[i] = sigma[i] - X1[i]
    i = i+1
  (y1, y2) = dshare_shuffle(X1, X2, p1, p2, p1p, p2p, a1, a2, b1, b2)
  y = [None] * n
  i = 0
  while i < n:
    y[i] = (y1[i]+y2[i]) % n
    i = i+1
  print("AppPerm y", y)
  w = perm_apply(x, y)
  g_inv = perm_inverse(g)
  w2 = perm_apply(w, g_inv)
  print("AppPerm w2", w2)
#  y_ = AppPerm_(x, sigma)
#  print("AppPerm_ y", y_)
#  return y_
  return w2
*****************************************************************/

///////////////////////////////////////////////////////////////////////////////////
// オンラインで計算する場合のメイン (bits版)
///////////////////////////////////////////////////////////////////////////////////
static _bits AppPerm_new_bits_channel(_bits x, _ sigma, int inverse, int channel)
{
  if (_party >  2) return NULL;
  dshare ds;
  int d = x->d;
//  printf("AppPerm sigma:"); share_print(sigma);
//  printf("AppPerm x:"); share_print(x);
//  printf("sigma k=%d\n", sigma->A->w);
//  printf("x k=%d\n", x->A->w);
  int n = len(x->a[0]);
  if (n != len(sigma)) {
    printf("AppPerm: len(x) = %d len(sigma) = %d", len(x->a[0]), len(sigma));
  }
  perm g;
  if (_party == 0) {
  //  g = perm_random(n);
    g = perm_random(mt0, n);
  } else {
    g = perm_id(n);
  }
//  printf("g "); perm_print(g);

  //_ z;
  NEWT(_bits, z);
  NEWA(z->a, _, d);
  z->d = d;
  //_ w;
  NEWT(_bits, w);
  NEWA(w->a, _, d);
  w->d = d;

  ds = dshare_new_channel(g, order(sigma), channel);
  _ rho = dshare_shuffle_channel(sigma, ds, channel);
  dshare_free(ds);

  if (inverse) {
    dshare ds_x = dshare_new2_channel(g, order(x->a[0]), channel);
    for (int i=0; i<d; i++) {
      dshare_correlated_random_channel(ds_x, channel);
      z->a[i] = dshare_shuffle_channel(x->a[i], ds_x, channel);
      dshare_free3(ds_x);
    }
    dshare_free2(ds_x);
//    printf("AppInvPerm z:"); share_print(z);
  } else {
    if (_party <= 0) {
    //  printf("rho k=%d\n", rho->A->w);
    //  w = share_perm_bits(x, share_raw(rho));
      for (int i=0; i<d; i++) {
        w->a[i] = share_perm(x->a[i], share_raw(rho));
      }
    } else {
      _ r = _reconstruct_channel(rho, channel);
      //_save(r, "tmp_r");
      //w = share_perm_bits(x, share_raw(r));
      for (int i=0; i<d; i++) {
        w->a[i] = share_perm(x->a[i], share_raw(r));
      }
      _free(r);
    }
//    printf("AppPerm w:"); share_print(w);
  }


  //_ ans;
  NEWT(_bits, ans);
  NEWA(ans->a, _, d);
  ans->d = d;
  if (inverse == 0) {
    perm g_inv = perm_inverse(g);
//    printf("g_inv "); perm_print(g_inv);
    ds = dshare_new2_channel(g_inv, order(w->a[0]), channel);

    //ans = dshare_shuffle_bits(w, ds);
    for (int i=0; i<d; i++) {
      dshare_correlated_random_channel(ds, channel);
      ans->a[i] = dshare_shuffle_channel(w->a[i], ds, channel);
      dshare_free3(ds);
    }
    dshare_free2(ds);
//    printf("AppPerm w2:"); share_print(w2);

    perm_free(g_inv);

  } else {
    _ r = _reconstruct_channel(rho, channel);
    perm rho_inv = perm_inverse(share_raw(r));
    //ans = share_perm_bits(z, rho_inv);
    for (int i=0; i<d; i++) {
      ans->a[i] = share_perm(z->a[i], rho_inv);
    }
    _free(r);
    //_free(z);
    //_free_bits(z);
    perm_free(rho_inv);
  }

  perm_free(g);
  _free(rho);
//  if (inverse == 0) _free(w);
  if (inverse == 0) _free_bits(w);

  return ans;
}
#define AppPerm_new_bits(x, sigma, inverse) AppPerm_new_bits_channel(x, sigma, inverse, 0)

_ Bits_to_block(_bits x)
{
  int n = len(x->a[0]);
  int d = x->d;
  _ ans = _const(n*d, 0, order(x->a[0]));
  for (int j=0; j<d; j++) {
    _ b = x->a[j];
    for (int i=0; i<n; i++) {
      _setshare(ans, i*d+j, b, i);
    }
  }
  return ans;
}

_bits block_to_Bits(int bs, _ b)
{
  int n = len(b) / bs;
  NEWT(_bits, ans);
  NEWA(ans->a, _, bs);
  ans->d = bs;
  for (int j=0; j<bs; j++) {
    ans->a[j] = _const(n, 0, order(b));
    for (int i=0; i<n; i++) {
      _setshare(ans->a[j], i, b, i*bs+j);
    }
  }
  return ans;
}

#if 0
///////////////////////////////////////////////////////////////////////////////
// bits を block に変換してからオンラインで計算
///////////////////////////////////////////////////////////////////////////////
static _bits AppPerm_bits4_channel(_bits x, _ sigma, int inverse, int channel)
{
  if (_party >  2) return NULL;
  dshare ds;
  int d = x->d;
//  printf("AppPerm sigma:"); share_print(sigma);
//  printf("AppPerm x:"); share_print(x);
//  printf("sigma k=%d\n", sigma->A->w);
//  printf("x k=%d\n", x->A->w);
  int n = len(x->a[0]);
  if (n != len(sigma)) {
    printf("AppPerm: len(x) = %d len(sigma) = %d", len(x->a[0]), len(sigma));
  }
  perm g;
  if (_party == 0) {
  //  g = perm_random(n);
    g = perm_random(mt0, n);
  } else {
    g = perm_id(n);
  }
//  printf("g "); perm_print(g);

  ds = dshare_new_channel(g, order(sigma), channel);
  _ rho = dshare_shuffle_channel(sigma, ds, channel);
  dshare_free(ds);


  _ z;
  //NEWT(_bits, z);
  //NEWA(z->a, _, d);
  //z->d = d;
  _ w;
  //NEWT(_bits, w);
  //NEWA(w->a, _, d);
  //w->d = d;

  _ xb = Bits_to_block(x);


  if (inverse) {
#if 0
    dshare ds_x = dshare_new2_channel(g, order(x->a[0]), channel);
    for (int i=0; i<d; i++) {
      dshare_correlated_random_channel(ds_x, channel);
      z->a[i] = dshare_shuffle_channel(x->a[i], ds_x, channel);
      dshare_free3(ds_x);
    }
    dshare_free2(ds_x);
#else
    dshare ds_x = block_dshare_new_channel(d, g, order(xb), channel);
    z = block_dshare_shuffle_channel(d, xb, ds_x, channel);
    dshare_free(ds_x);
#endif
//    printf("AppInvPerm z:"); share_print(z);
  } else {
    if (_party <= 0) {
    //  printf("rho k=%d\n", rho->A->w);
    //  w = share_perm_bits(x, share_raw(rho));
#if 0
      for (int i=0; i<d; i++) {
        w->a[i] = share_perm(x->a[i], share_raw(rho));
      }
#else
    w = block_share_perm(d, xb, share_raw(rho));
#endif
    } else {
      _ r = _reconstruct_channel(rho, channel);
      //_save(r, "tmp_r");
      //w = share_perm_bits(x, share_raw(r));
#if 0
      for (int i=0; i<d; i++) {
        w->a[i] = share_perm(x->a[i], share_raw(r));
      }
#else
      w = block_share_perm(d, xb, share_raw(r));
#endif
      _free(r);
    }
//    printf("AppPerm w:"); share_print(w);
  }


  _bits ans;
  //NEWT(_bits, ans);
  //NEWA(ans->a, _, d);
  //ans->d = d;
  if (inverse == 0) {
    perm g_inv = perm_inverse(g);
//    printf("g_inv "); perm_print(g_inv);
//    ds = dshare_new_channel(g_inv, order(w), channel);
    ds = block_dshare_new_channel(d, g_inv, order(w), channel);

    //ans = dshare_shuffle_bits(w, ds);
#if 0
    for (int i=0; i<d; i++) {
      dshare_correlated_random_channel(ds, channel);
      ans->a[i] = dshare_shuffle_channel(w->a[i], ds, channel);
      dshare_free3(ds);
    }
#else
    _ ans_b = block_dshare_shuffle_channel(d, w, ds, channel);
    ans = block_to_Bits(d, ans_b);
    _free(ans_b);
#endif
    dshare_free(ds);
//    printf("AppPerm w2:"); share_print(w2);

    perm_free(g_inv);

  } else {
    _ r = _reconstruct_channel(rho, channel);
    perm rho_inv = perm_inverse(share_raw(r));
    //ans = share_perm_bits(z, rho_inv);
#if 0
    for (int i=0; i<d; i++) {
      ans->a[i] = share_perm(z->a[i], rho_inv);
    }
#else
    _ ans_b = block_share_perm(d, z, rho_inv);
    ans = block_to_Bits(d, ans_b);
    _free(ans_b);
#endif
    _free(r);
    //_free(z);
    //_free_bits(z);
    perm_free(rho_inv);
  }

  perm_free(g);
  _free(rho);
  if (inverse == 0) _free(w);
//  if (inverse == 0) _free_bits(w);
  _free(xb);
  _free(z);

  return ans;
}
#define AppPerm_bits4(a, sigma) AppPerm_bits4_channel(a, sigma, 0, 0)
#define AppInvPerm_bits4(a, sigma) AppPerm_bits4_channel(a, sigma, 1, 0)
#endif

static _bits AppPerm_bits_bd_channel(_bits x, _ sigma, int inverse, int channel)
{
  int d = x->d;
  _ xb = Bits_to_block(x);
  _ ans_b;
  if (inverse) {
    ans_b = block_AppPerm_inverse_channel(d, xb, sigma, channel);
  } else {
    ans_b = block_AppPerm_fwd_channel(d, xb, sigma, channel);
  }
  _bits ans = block_to_Bits(d, ans_b);
  _free(ans_b);
  _free(xb);

  return ans;
}
#define AppPerm_bits_channel(a, sigma, channel) AppPerm_bits_bd_channel(a, sigma, 0, 0)
#define AppInvPerm_bits_channel(a, sigma, channel) AppPerm_bits_bd_channel(a, sigma, 1, 0)
#define AppPerm_bits(a, sigma) AppPerm_bits_channel(a, sigma, 0)
#define AppInvPerm_bits(a, sigma) AppInvPerm_bits_channel(a, sigma, 0)

#if 0
// 通信量が多い
static _bits AppPerm_new_bits3_channel(_bits x, _ sigma, int inverse, int channel)
{
  if (_party >  2) return NULL;
  int d = x->d;

  NEWT(_bits, ans);
  NEWA(ans->a, _, d);
  ans->d = d;

  for (int i=0; i<d; i++) {
    if (inverse) {
      ans->a[i] = block_AppPerm_inverse_channel(1, x->a[i], sigma, channel);
    } else {
      ans->a[i] = block_AppPerm_fwd_channel(1, x->a[i], sigma, channel);
    }
  }

  return ans;
}

static _bits AppInvPerm_bits3_channel(_bits a, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  return AppPerm_new_bits3_channel(a, sigma, 1, channel);
}
#define AppInvPerm_bits3(a, sigma) AppInvPerm_bits3_channel(a, sigma, 0)

static _bits AppPerm_bits3_channel(_bits a, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  return AppPerm_new_bits3_channel(a, sigma, 0, channel);
}
#define AppPerm_bits3(a, sigma) AppPerm_bits3_channel(a, sigma, 0)
#endif


#if 0
static _ AppPerm_channel(_ x, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  //_ ans = AppPerm_new_channel(x, sigma, 0, channel);
  _ ans = AppPerm_fwd_channel(x, sigma, channel);
  return ans;
}
#endif

static _ AppPerm_channel(_ x, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  //_ ans = AppPerm_new_channel(x, sigma, 0, channel);
  _ ans = block_AppPerm_fwd_channel(1, x, sigma, channel);
  return ans;
}

static _ AppPerm(_ x, _ sigma)
{
  if (_party >  2) return NULL;
  return AppPerm_fwd_channel(x, sigma, 0);
}

static void AppPerm_channel_(_ x, _ sigma, int channel)
{
  if (_party >  2) return;
//  _ ans = AppPerm_new_channel(x, sigma, 0, channel);
  _ ans = AppPerm_fwd_channel(x, sigma, channel);
  _move_(x, ans);
}
#define AppPerm_(x, sigma) AppPerm_channel_(x, sigma, 0)

#if 0
static _ AppInvPerm_channel(_ x, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  //_ ans = AppPerm_new_channel(x, sigma, 1, channel);
  _ ans = AppPerm_inverse_channel(x, sigma, channel);
  return ans;
}
#define AppInvPerm_(x, sigma) AppInvPerm_channel_(x, sigma, 0)
#endif

static _ AppInvPerm_channel(_ x, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  _ ans = block_AppPerm_inverse_channel(1, x, sigma, channel);
  return ans;
}
#define AppInvPerm(x, sigma) AppInvPerm_channel(x, sigma, 0)


static void AppInvPerm_channel_(_ x, _ sigma, int channel)
{
  if (_party >  2) return;
//  _ ans = AppPerm_new_channel(x, sigma, 1, channel);
  _ ans = AppPerm_inverse_channel(x, sigma, channel);
  _move_(x, ans);
}
#define AppInvPerm_(x, sigma) AppInvPerm_channel_(x, sigma, 0)

#if 0
static void AppInvPerm_bits_channel_(_bits a, _ sigma, int channel)
{
  if (_party >  2) return;
  for (int i=0; i<a->d; i++) {
    AppInvPerm_channel_(a->a[i], sigma, channel);
  }
}
#define AppInvPerm_bits_(a, sigma) AppInvPerm_bits_channel_(a, sigma, 0)

static void AppPerm_bits_channel_(_bits a, _ sigma, int channel)
{
  if (_party >  2) return;
  for (int i=0; i<a->d; i++) {
    AppPerm_channel_(a->a[i], sigma, channel);
  }
}
#define AppPerm_bits_(a, sigma) AppPerm_bits_channel_(a, sigma, 0)
#endif

#if 0
static _bits AppInvPerm_bits_channel(_bits a, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  NEWT(_bits, ans);
  NEWA(ans->a, _, a->d);
  ans->d = a->d;
  for (int i=0; i<a->d; i++) {
    ans->a[i] = AppInvPerm_channel(a->a[i], sigma, channel);
  }
  return ans;
}
#define AppInvPerm_bits(a, sigma) AppInvPerm_bits_channel(a, sigma, 0)


static _bits AppPerm_bits_channel(_bits a, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  NEWT(_bits, ans);
  NEWA(ans->a, _, a->d);
  ans->d = a->d;
  for (int i=0; i<a->d; i++) {
    ans->a[i] = AppPerm_channel(a->a[i], sigma, channel);
  }
  return ans;
}
#define AppPerm_bits(a, sigma) AppPerm_bits_channel(a, sigma, 0)
#endif

static _bits AppPerm_bits_online_channel(_bits a, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  return AppPerm_new_bits_channel(a, sigma, 0, channel);
}
#define AppPerm_bits_online(a, sigma) AppPerm_bits_online_channel(a, sigma, 0)

static _bits AppInvPerm_bits_online_channel(_bits a, _ sigma, int channel)
{
  if (_party >  2) return NULL;
  return AppPerm_new_bits_channel(a, sigma, 1, channel);
}
#define AppInvPerm_bits_online(a, sigma) AppInvPerm_bits_online_channel(a, sigma, 0)


#if 0
typedef struct AppPerm_args {
  int channel; // 0, 1, ..., NC-1
  _ x;
  _ sigma;
  int inverse;
  _ ans;
}* AppPerm_args;

void *AppPerm_concurrent(void *args_) {
  if (_party >  2) return NULL;
  AppPerm_args args = (AppPerm_args)args_;
  int channel = args->channel;
  _ x = args->x;
  _ sigma = args->sigma;
  int inverse = args->inverse;
  _ ans;
  if (inverse == 0) {
    ans = AppPerm_fwd_channel(x, sigma, channel);
  } else {
    ans = AppPerm_inverse_channel(x, sigma, channel);
  }
  args->ans = ans;
  return NULL;
}

void *AppPerm_concurrent_(void *args_) {
  if (_party >  2) return NULL;
  AppPerm_concurrent(args_);
  AppPerm_args args = (AppPerm_args)args_;
  _move_(args->x, args->ans);
  return NULL;
}
#endif

#endif
