////////////////////////////////////////////
// 構造体の中身をいじったり通信をする関数はこの中に
////////////////////////////////////////////

#ifndef _SHARE_CORE_H
 #define _SHARE_CORE_H

typedef int share_t;
//typedef long share_t;
//typedef packed_array share_t;


#include "mpc.h"
#include "bits.h"
#include "beaver.h"

extern long send_1, send_2, send_3, send_4, send_5, send_6, send_7, send_8;

#ifndef RANDOM0
// #define RANDOM0(n) (rand() % (n))
 #define RANDOM0(n) (genrand_int32() % (n))
#endif

typedef struct {
  int n; // 要素数
  share_t q; // mod
  packed_array A; // 元の値 (party==0) またはシェア (party==1,2)
  int own; // 1 の時は解放しない
}* share_array;
#define _ share_array

typedef share_array _b;

typedef struct {
  share_array x, y;
} share_pair;
#define _pair share_pair

typedef struct bits {
  int d; // 桁数
  _* a;
}* _bits;

typedef struct {
  _bits x;
  _ y;
} share_pair_bits;
#define _pair_bits share_pair_bits

#ifndef MOD
// #define MOD(x) (((x)+(q)*1) % (q))
 #define MOD(x) (((x)%(q)+(q)*1) % (q))
#endif


/***********************************************************
 * x = f(g(y), z) のときは g(y) のメモリは解放したい
 * z は解放すべきではない．関数の最後で解放する．
 * 関数の返り値は一時的なもので，変数に代入すると確定する
 * 変数への代入は必ず特殊関数を使うことにする
 *   _D(x, f(y))  // x の定義と代入
 *   _M(x, f(y))  // 元の x の解放?と代入
 * 全ての関数で，return 時に一時的な引数の解放を行う
***********************************************************/
//#define _D(x, val) _ x = (val); x->own = 1;
//#define _M(x, val) x = (val); x->own = 1;

static int len(share_array a)
{
  return a->n;
}

static share_t order(share_array a)
{
  return a->q;
}

static packed_array share_raw(share_array a)
{
  return a->A;
}



static void mpc_send_share_channel(int party_to, _ A, int channel)
{
  if (_party < 0) return;
  void *buf = A->A->B;
  int size = pa_size(A->A);
  int c = 0;
  switch (party_to) {
  //case TO_SERVER:
  case TO_PARTY1:
  case TO_PARTY2:
  //case TO_PAIR:
    c = channel*2+party_to;
    break;
  case TO_PARTY3:
    c = channel+party_to;
    break;
  default:
    c = party_to;
  }
  mpc_send(c, buf, size);  send_6 += size;
}
#define mpc_send_share(party_to, A) mpc_send_share_channel(party_to, A, 0)


static void mpc_recv_share_channel(int party_from, _ A, int channel)
{
  if (_party < 0) return;
  void *buf = A->A->B;
  int size = pa_size(A->A);
  int c = 0;
  switch (party_from) {
  //case FROM_SERVER:
  case FROM_PARTY1:
  case FROM_PARTY2:
  //case FROM_PAIR:
    c = channel*2+party_from;
    break;
  case TO_PARTY3:
    c = channel+party_from;
    break;
  default:
    c = party_from;
  }
  mpc_recv(c, buf, size);
}
#define mpc_recv_share(party_to, A) mpc_recv_share_channel(party_to, A, 0)

static void mpc_exchange_share_channel(_ share_send, _ share_recv, int channel)
{
  if (_party >  2) return;
  if (_party <= 0) return;

  void *buf_send = share_send->A->B;
  void *buf_recv = share_recv->A->B;
  int size = pa_size(share_send->A);
  mpc_exchange_channel(buf_send, buf_recv, size, channel);
}
#define mpc_exchange_share(send, recv) mpc_exchange_share_channel(send, recv, 0)





static void share_print(share_array a)
{
//  if (_party >  2) return;
  if (a == NULL) return;
  printf("n = %d q = %d w = %d party %d: ", a->n, (int)a->q, a->A->w, _party);
  if (a->A != NULL) {
    for (int i=0; i<a->n; i++) printf("%d ", (int)pa_get(a->A, i));
  }
  printf("\n");
}
#define _print share_print

static void share_fprint(FILE *f, share_array a)
{
//  if (_party >  2) return;
  if (a->A == NULL) return;
  fprintf(f, "n = %d q = %d w = %d party %d: ", a->n, (int)a->q, a->A->w, _party);
  for (int i=0; i<a->n; i++) fprintf(f, "%d ", (int)pa_get(a->A, i));
  fprintf(f, "\n");
}


static share_array share_new_channel(int n, share_t q, share_t *A, int channel)
{
//  if (_party >  2) return NULL;
  int i;
  NEWT(share_array, ans);
//  comm c;
//  comm c1, c2;
  int k;

//  printf("share_new n = %d q = %d\n", n, q);

  ans->n = n;
  ans->q = q;
  ans->own = 0;
  k = blog(q-1)+1;
  ans->A = NULL;
  if (_party == 3) return ans;

  ans->A = pa_new(n, k);
  if (_party <= 0) {
    packed_array A1, A2;
    A1 = pa_new(n, k);
    A2 = pa_new(n, k);
    for (i=0; i<n; i++) {
      share_t r;
      pa_set(ans->A, i, A[i]);
      r = RANDOM0(q);
      pa_set(A1, i, r);
      pa_set(A2, i, MOD(A[i] - r));
    }
    mpc_send(channel*2+TO_PARTY1, A1->B, pa_size(A1));  send_7 += pa_size(A1);
    mpc_send(channel*2+TO_PARTY2, A2->B, pa_size(A2));

    pa_free(A1);
    pa_free(A2);
  } else {
    mpc_recv_share(channel*2+FROM_SERVER, ans);
  }

  return ans;
}
#define share_new(n, q, A) share_new_channel(n, q, A, 0)

static share_array share_new_queue_channel(int n, share_t q, share_t *A, int channel)
{
  if (_party >  2) return NULL;
  int i;
  NEWT(share_array, ans);
//  comm c;
//  comm c1, c2;
  int k;

//  printf("share_new n = %d q = %d\n", n, q);

  ans->n = n;
  ans->q = q;
  ans->own = 0;
  k = blog(q-1)+1;
  ans->A = pa_new(n, k);
  if (_party <= 0) {
    packed_array A1, A2;
    A1 = pa_new(n, k);
    A2 = pa_new(n, k);
    for (i=0; i<n; i++) {
      share_t r;
      pa_set(ans->A, i, A[i]);
      r = RANDOM0(q);
      pa_set(A1, i, r);
      pa_set(A2, i, MOD(A[i] - r));
    }
    mpc_send_queue(channel*2+TO_PARTY1, A1->B, pa_size(A1));  send_7 += pa_size(A1);
    mpc_send_queue(channel*2+TO_PARTY2, A2->B, pa_size(A2));

    pa_free(A1);
    pa_free(A2);
  } else {
    mpc_recv_share(channel*2+FROM_SERVER, ans);
  }

  return ans;
}


static void share_resend_channel(_ a, int channel)
{
  if (_party >  2) return;
  if (_party < 0) return;
  int n = len(a);
  share_t q = order(a);
  int k = blog(q-1)+1;
  int w = a->A->w;

  if (_party <= 0) {
    packed_array A1, A2;
  //  A1 = pa_new(n, k);
  //  A2 = pa_new(n, k);
    A1 = pa_new(n, w);
    A2 = pa_new(n, w);
    for (int i=0; i<n; i++) {
      share_t r, v;
      v = pa_get(a->A, i);
      r = RANDOM0(q);
      pa_set(A1, i, r);
      pa_set(A2, i, MOD(v - r));
    }
    mpc_send(channel*2+TO_PARTY1, A1->B, pa_size(A1));  send_7 += pa_size(A1);
    mpc_send(channel*2+TO_PARTY2, A2->B, pa_size(A2));

    pa_free(A1);
    pa_free(A2);
  } else {
    mpc_recv_share(channel*2+FROM_SERVER, a);
  }
}
#define share_resend(a) share_resend_channel(a, 0)

//static share_array share_new(int n, share_t q, share_t *A)
//{
//  share_new_channel(n, q, A, 0);
//}

static void share_free(share_array a)
{
//  if (_party >  2) return;
  if (a == NULL) return;
  if (a->A != NULL) pa_free(a->A);
  free(a);
}
#define _free share_free

static void share_save(share_array a, char *filename)
{
  if (_party >  2) return;
  char buf[100];
  int p = _party;
  if (p < 0) p = 0;
  sprintf(buf, "%s%d.txt", filename, p);
  FILE *f = fopen(buf, "w");
  if (f == NULL) {
    perror("share_save: ");
  }
  int n = len(a);
  fprintf(f, "%d %d\n", n, (int)order(a));
  for (int i=0; i<n; i++) {
  //  fprintf(f, "%d\n", (int)a->A[i]);
    fprintf(f, "%d\n", (int)pa_get(a->A, i));
  }
  fclose(f);
}
#define _save share_save

static share_array share_load(char *filename)
{
  if (_party >  2) return NULL;
  char buf[100];
  int p = _party;
  if (p < 0) p = 0;
  sprintf(buf, "%s%d.txt", filename, p);
  FILE *f = fopen(buf, "r");
  if (f == NULL) {
    perror("share_load: ");
  }
  int n;
  share_t q, v;
  int qtmp;
  fscanf(f, " %d %d", &n, &qtmp);
  q = qtmp;
  int k = blog(q-1)+1;
  NEWT(share_array, a);
  a->A = pa_new(n, k);
  a->n = n;
  a->q = q;
  for (int i=0; i<n; i++) {
    int vtmp;
    fscanf(f, " %d", &vtmp);
    v = vtmp;
    pa_set(a->A, i, v);
  }
  fclose(f);
  return a;
}
#define _load share_load


static void share_save_binary(share_array a, char *filename)
{
  if (_party >  2) return;

  int p = _party;
  if (p < 0) p = 0;
  char *fname = precomp_fname(filename, p);

  FILE *f = fopen(fname, "w");
  if (f == NULL) {
    perror("share_save_binary: ");
  }
  writeuint(1,ID_SHARE,f);
  writeuint(sizeof(a->n), a->n, f);
  writeuint(sizeof(a->q), a->q, f);

  pa_write(a->A, f);

  fclose(f);
  free(fname);
}
#define _save_binary share_save_binary


static _ share_load_binary(char *filename)
{
  if (_party >  2) return NULL;

  int party = _party;
  if (party < 0) party = 0;
  char *fname = precomp_fname(filename, party);

  MMAP *map = NULL;
  map = mymmap(fname);
  uchar *p = (uchar *)map->addr;

  int type = getuint(p,0,1);  p += 1;
  if (type != ID_SHARE) {
    printf("share_load_binary: ID = %d\n", type);
    exit(1);
  }

  NEWT(_, ans);
  ans->n = getuint(p,0,sizeof(ans->n));  p += sizeof(ans->n);
  ans->q = getuint(p,0,sizeof(ans->q));  p += sizeof(ans->q);
  ans->own = 0;
  ans->A = pa_read(&p);

  free(fname);

  return ans;
}
#define _load_binary share_load_binary

static void share_check(share_array a)
{
  if (_party >  2) return;
  int i, n;
//  comm c0, c1, c2;
  share_t q;

//  printf("share_check\n");
  n = a->n;
  q = a->q;
  int k = blog(q-1)+1;
//  printf("share_check q=%d k=%d w=%d\n", q, k, a->A->w);
  int err=0;
  if (_party <= 0) {
    packed_array A1, A2;
    A1 = pa_new(n, k);
    A2 = pa_new(n, k);
    printf("check party %d: ", _party);
    mpc_recv(FROM_PARTY1, A1->B, pa_size(a->A));
    mpc_recv(FROM_PARTY2, A2->B, pa_size(a->A));
    if (_party == 0) {
      for (i=0; i<n; i++) {
        share_t x;
        x = MOD(q + pa_get(A1, i) + pa_get(A2, i));
        if ((u64)x != pa_get(a->A, i)) {
          printf("i = %d A = %d %d A1 = %d A2 = %d\n", i, (int)pa_get(a->A, i), (int)x, (int)pa_get(A1,i), (int)pa_get(A2,i));
          err=1;
          exit(1);
        }
      }
      printf("check done\n");
    }
    pa_free(A1);
    pa_free(A2);
  } else {
    printf("check party %d: ", _party);
    mpc_send_share(TO_SERVER, a);
  }
}
#define _check share_check

static share_array share_reconstruct_channel(share_array a, int channel)
{
  if (_party >  2) return NULL;
  int i, n;
//  comm c;
  share_t q;

  int mode = 0;
//  if (mode < 0 || mode > 2) {
//    printf("reconstruct: mode = %d\n", mode);
//    exit(1);
//  }

//  printf("share_reconstruct\n");
  NEWT(share_array, ans);
  *ans = *a;
  n = a->n;
  q = a->q;
  int k = blog(q-1)+1;
  ans->A = pa_new(n, k);

  if (_party <= 0) {
    for (i=0; i<n; i++) {
      pa_set(ans->A, i, pa_get(a->A, i));
    }
  } else {
    packed_array x;
//    share_t *tmp;
    x = pa_new(n, k);
    if (mode == 0) {
      mpc_exchange_channel(a->A->B, x->B, pa_size(a->A), channel);
      for (i=0; i<n; i++) {
        pa_set(ans->A, i, MOD(pa_get(a->A,i) + pa_get(x,i)));
      }
    } else {
      if (_party != mode) {
        mpc_send_share(channel*2+TO_PAIR, a);  send_8 += pa_size(a->A);
      } else {
        mpc_recv(channel*2+FROM_PAIR, x->B, pa_size(a->A));
        for (i=0; i<n; i++) {
          pa_set(ans->A, i, MOD(pa_get(a->A,i) + pa_get(x,i)));
        }
      }
    }
    pa_free(x);
  }
  return ans;
}
#define _reconstruct_channel share_reconstruct_channel
#define share_reconstruct(a) share_reconstruct_channel(a, 0)
#define _reconstruct share_reconstruct

///////////////////////////////////////////////////
// a に乱数 r, -r を加える
// 乱数列を共有することにも使える（これを別に作る方が良い？）
///////////////////////////////////////////////////
static void share_randomize(share_array a)
{
  if (_party >  2) return;
  if (_party <= 0) return;

  unsigned long init[5]={0x123, 0x234, 0x345, 0x456, 0};

  if (_party == 1) {
    init[4] = 1; // rand();
    mpc_send(TO_PARTY2, init, sizeof(init[0])*5);
  } else {
    mpc_recv(FROM_PARTY2, init, sizeof(init[0])*5);
  }
//  init_by_array(init, 5);
  MT m0 = MT_init_by_array(init, 5);

  share_t q, x, r;
  q = order(a);
  int n = len(a);
  for (int i=0; i<n; i++) {
    r = RANDOM(m0, q);
    x = pa_get(a->A, i);
    if (_party == 1) {
      x = MOD(x + r);
    } else {
      x = MOD(x - r);
    }
    pa_set(a->A, i, x);
  }
  MT_free(m0);
}
#define _randomize share_randomize

static share_array share_dup(share_array a)
{
//  if (_party >  2) return NULL;
//  printf("dup "); _print(a);
  NEWT(share_array, D);
  *D = *a;
  D->A = NULL;
  if (a->A != NULL) {
    D->A = pa_new(D->n, a->A->w);
  //  for (int i=0; i<D->n; i++) pa_set(D->A,i, pa_get(a->A,i));
    memcpy(D->A->B, a->A->B, pa_size(a->A));
  }
  return D;
}
#define _dup share_dup



//////////////////////////////////
// P0, P1, P2 で同期をとる
//////////////////////////////////
void _sync(void)
{
  if (_party >  2) return;
  share_t A[1] = {0};
  _ tmp = share_new(1, 2, A);
//  _ tmp2 = _reconstruct(tmp);
  _check(tmp);
  _free(tmp);
//  _free(tmp2);
//  printf("sync\n");
//  getchar();
}

void _sync_channel(int channel)
{
  if (_party >  2) return;
  char tmp[1];
  tmp[0] = '$';
  if (_party == 0) {
    mpc_send(channel*2+TO_PARTY1, tmp, 1);
    mpc_send(channel*2+TO_PARTY2, tmp, 1);
  }
  tmp[0] = '?';
  if (_party == 1 || _party == 2) {
    mpc_recv(channel*2+FROM_SERVER, tmp, 1);
    if (tmp[0] != '$') {
      printf("sync: recv %c %d\n", tmp[0], tmp[0]);
      exit(1);
    }
  }
}



//////////////////////////////////
// a := b (古い a, b のメモリを解放する)
//////////////////////////////////
static void share_move_(share_array a, share_array b)
{
//  if (_party >  2) return;
  if (a == NULL) return;
  if (b == NULL) return;
  if (a->A != NULL) pa_free(a->A);
  *a = *b;
  free(b);
}
#define _move_ share_move_

static share_array share_move(share_array b)
{
  if (_party >  2) return NULL;
  return b;
}
#define _move share_move

///////////////////////////////////////
// シェアの片割れを得る
///////////////////////////////////////
static share_t share_getraw(share_array a, int i)
{
  if (i < 0 || i >= a->n) {
    printf("share_getraw n %d i %d\n", a->n, i);
  }
  if (a->A == NULL) return 0;
  return pa_get(a->A,i);
}

static void share_setraw(share_array a, int i, share_t x)
{
  if (i < 0 || i >= a->n) {
    printf("share_setraw n %d i %d\n", a->n, i);
  }
  if (x < 0) {
    printf("share_setraw x %d q %d\n", x, a->q);
  }
  if (a->A == NULL) return;
  share_t q = a->q;
  pa_set(a->A, i, MOD(x));
}

///////////////////////////////////////
// x は公開の平文
///////////////////////////////////////
static void share_setpublic(share_array a, int i, share_t x)
{
  if (_party >  2) return;
  if (i < 0 || i >= a->n) {
    printf("share_setpublic n %d i %d\n", a->n, i);
  }
  share_t q = a->q;
  if (_party == 2) {
    pa_set(a->A, i, 0);
  } else {
    pa_set(a->A, i, MOD(x));
  }
}
#define _setpublic share_setpublic

////////////////////////////////////////////
// a[i] := b[j]
////////////////////////////////////////////
static void share_setshare(share_array a, int i, share_array b, int j)
{
//  if (_party >  2) return;
  if (i < 0 || i >= a->n) {
    printf("share_setshare a: n %d i %d\n", a->n, i);
    exit(1);
  }
  if (j < 0 || j >= b->n) {
    printf("share_setshare b: n %d j %d\n", b->n, j);
    exit(1);
  }
  if (a->q != b->q) {
    printf("share_setshare a->q %d b->q %d\n", (int)a->q, (int)b->q);
    exit(1);
  }
  if (a->A != NULL && b->A != NULL) pa_set(a->A,i, pa_get(b->A,j));
}
#define _setshare share_setshare

////////////////////////////////////////////
// a[is:ie) := b[js:je)
////////////////////////////////////////////
static void share_setshares(share_array a, int is, int ie, share_array b, int js)
{
//  if (_party >  2) return;
  if (is < 0 || is >= a->n) {
    printf("share_setshares a: n %d is %d\n", a->n, is);
    exit(1);
  }
  if (ie > a->n) {
    printf("share_setshares a: n %d ie %d\n", a->n, ie);
    exit(1);
  }
  if (js < 0 || js >= b->n) {
    printf("share_setshares b: n %d js %d\n", b->n, js);
    exit(1);
  }
  if (js + (ie-is) > b->n) {
    printf("share_setshares b: n %d is %d ie %d js %d\n", b->n, is, ie, js);
    exit(1);
  }
  if (a->q != b->q) {
    printf("share_setshares a->q %d b->q %d\n", (int)a->q, (int)b->q);
    exit(1);
  }
  if (a->A != NULL && b->A != NULL) {
    for (int i = 0; i < ie-is; i++) {
      pa_set(a->A,is + i, pa_get(b->A,js + i));
    }
  }
}
#define _setshares share_setshares


static void share_addpublic(share_array a, int i, share_t x)
{
  if (_party >  2) return;
  if (i < 0 || i >= a->n) {
    printf("share_addpublic n %d i %d\n", a->n, i);
  }
  share_t q = a->q;
  if (_party != 2) pa_set(a->A, i, MOD(pa_get(a->A,i) + x));
}
#define _addpublic share_addpublic

static void share_addshare_shamir(share_array a, int i, share_array b, int j)
{
//  if (_party >  2) return;
  if (i < 0 || i >= a->n) {
    printf("share_addshare a: n %d i %d\n", a->n, i);
  }
  if (j < 0 || j >= b->n) {
    printf("share_addshare b: n %d j %d\n", b->n, j);
  }
  if (a->q != b->q) {
    printf("share_addshare a->q %d b->q %d\n", (int)a->q, (int)b->q);
  }
  share_t q = a->q;
  pa_set(a->A,i,MOD(pa_get(a->A,i) + pa_get(b->A,j)));
}
#define _addshare_shamir share_addshare_shamir

static void share_addshare(share_array a, int i, share_array b, int j)
{
  if (_party >  2) return;
  return share_addshare_shamir(a, i, b, j);
}
#define _addshare share_addshare


static void share_subshare(share_array a, int i, share_array b, int j)
{
  if (_party >  2) return;
  if (i < 0 || i >= a->n) {
    printf("share_subshare a: n %d i %d\n", a->n, i);
  }
  if (j < 0 || j >= b->n) {
    printf("share_subshare b: n %d j %d\n", b->n, j);
  }
  if (a->q != b->q) {
    printf("share_subshare a->q %d b->q %d\n", (int)a->q, (int)b->q);
  }
  share_t q = a->q;
  pa_set(a->A,i,MOD(pa_get(a->A,i) - pa_get(b->A,j)));
}
#define _subshare share_subshare


static void share_mulpublic(share_array a, int i, int x)
{
  if (_party >  2) return;
  if (i < 0 || i >= a->n) {
    printf("share_mulpublic n %d i %d\n", a->n, i);
  }
  share_t q = a->q;
  pa_set(a->A, i, LMUL(pa_get(a->A,i), x, q));
}
#define _mulpublic share_mulpublic

/////////////////////////////////////////
// [start, end-1] の範囲を切り出す
// end は含まないことに注意（Python風）
/////////////////////////////////////////
static share_array share_slice(share_array a, int start, int end)
{
  if (_party >  2) return NULL;
  if (start < 0) start = a->n + start;
  if (end <= 0) end = a->n + end;
  if (start < 0 || start > a->n) {
    printf("share_slice n %d start %d\n", a->n, start);
  }
  if (end < 0 || end > a->n) {
    printf("share_slice n %d end %d\n", a->n, end);
  }
  NEWT(share_array, ans);
  ans->n = end - start;
  ans->q = a->q;
  ans->A = pa_new(ans->n, a->A->w);
  for (int i=0; i<ans->n; i++) pa_set(ans->A,i,pa_get(a->A,start+i));
  return ans;
}
#define _slice share_slice

static void share_slice_(share_array a, int start, int end)
{
  if (_party >  2) return;
  share_array tmp = share_slice(a, start, end);
  pa_free(a->A);  *a = *tmp;  free(tmp);
}
#define _slice_ share_slice_

static share_array share_concat(share_array a, share_array b)
{
  if (_party >  2) return NULL;
  if (a->q != b->q) {
    printf("share_concat a->q %d b->q %d\n", (int)a->q, (int)b->q);
  }
  NEWT(share_array, ans);
  ans->n = a->n + b->n;
  ans->q = a->q;
  ans->A = pa_new(ans->n, a->A->w);
  for (int i=0; i<a->n; i++) pa_set(ans->A,i,pa_get(a->A,i));
  for (int i=0; i<b->n; i++) pa_set(ans->A,a->n + i, pa_get(b->A,i));
  return ans;
}
#define _concat share_concat

static void share_concat_(share_array a, share_array b)
{
  if (_party >  2) return;
  share_array tmp = share_concat(a, b);
  pa_free(a->A);  *a = *tmp;  free(tmp);
}
#define _concat_ share_concat_



static share_array share_insert_head(share_array a, share_t x)
{
  if (_party >  2) return NULL;
  NEWT(share_array, ans);
  ans->n = a->n + 1;
  ans->q = a->q;
  ans->A = pa_new(ans->n, a->A->w);
  if (_party == 2) {
    pa_set(ans->A, 0, 0);
  } else {
    pa_set(ans->A, 0, x);
  }
  for (int i=1; i<ans->n; i++) pa_set(ans->A, i, pa_get(a->A, i-1));
  return ans;
}
#define _insert_head share_insert_head

static void share_insert_head_(share_array a, share_t x)
{
  if (_party >  2) return;
  share_array tmp = share_insert_head(a, x);
  pa_free(a->A);  *a = *tmp;  free(tmp);
}
#define _insert_head_ share_insert_head_

static share_array share_insert_tail(share_array a, share_t x)
{
  if (_party >  2) return NULL;
  NEWT(share_array, ans);
  ans->n = a->n + 1;
  ans->q = a->q;
  ans->A = pa_new(ans->n, a->A->w);
  if (_party == 2) {
    pa_set(ans->A, ans->n-1, 0);
  } else {
    pa_set(ans->A, ans->n-1, x);
  }
  for (int i=0; i<ans->n-1; i++) pa_set(ans->A, i, pa_get(a->A, i));
  return ans;
}
#define _insert_tail share_insert_tail

static void share_insert_tail_(share_array a, share_t x)
{
  if (_party >  2) return;
  share_array tmp = share_insert_tail(a, x);
  pa_free(a->A);  *a = *tmp;  free(tmp);
}
#define _insert_tail_ share_insert_tail_


static share_array vadd(share_array a, share_array b)
{
  if (_party >  2) return NULL;
  int n = a->n;
  share_t q = a->q;
  if (a->n != b->n) {
    printf("vadd a->n = %d b->n = %d\n", a->n, b->n);
  }
  if (a->q != b->q) {
    printf("vadd a->q = %d b->q = %d\n", (int)a->q, (int)b->q);
  }
  NEWT(share_array, ans);
  *ans = *a;
  ans->A = pa_new(a->n, a->A->w);
  for (int i=0; i<n; i++) {
    pa_set(ans->A, i, MOD(pa_get(a->A, i) + pa_get(b->A, i)));
  }
  return ans;
}
#define _vadd vadd

static void vadd_(share_array a, share_array b)
{
  if (_party >  2) return;
  share_array tmp = vadd(a, b);
  pa_free(a->A);  *a = *tmp;  free(tmp);
}
#define _vadd_ vadd_

static share_array vsub(share_array a, share_array b)
{
  if (_party >  2) return NULL;
  int n = a->n;
  share_t q = a->q;
  if (a->n != b->n) {
    printf("vsub a->n = %d b->n = %d\n", a->n, b->n);
  }
  if (a->q != b->q) {
    printf("vsub a->q = %d b->q = %d\n", (int)a->q, (int)b->q);
  }
  NEWT(share_array, ans);
  *ans = *a;
  ans->A = pa_new(a->n, a->A->w);
  for (int i=0; i<n; i++) {
    pa_set(ans->A, i, MOD(pa_get(a->A, i) - pa_get(b->A, i)));
  }
  return ans;
}
#define _vsub vsub

static void vsub_(share_array a, share_array b)
{
  if (_party >  2) return;
  share_array tmp = vsub(a, b);
  pa_free(a->A);  *a = *tmp;  free(tmp);
}
#define _vsub_ vsub_

static share_array vmul_channel(share_array x, share_array y, int channel)
{
  if (_party >  2) return NULL;
  int n = x->n;
  share_t q = x->q;
  int i;
  if (x->n != y->n) {
    printf("vmul x->n = %d y->n = %d\n", x->n, y->n);
  }
  if (x->q != y->q) {
    printf("vmul x->q = %d y->q = %d\n", (int)x->q, (int)y->q);
  }
  NEWT(share_array, ans);
  *ans = *x;
  ans->A = pa_new(n, x->A->w);

// Beaver Triple の計算
  BeaverTriple bt;
//  printf("channel %d tbl %p\n", channel, BT_tbl[channel]);

#if 0
  share_array sigma, rho;
  share_array sigma_c, rho_c;
  NEWT(share_array, a);
  NEWT(share_array, b);
#endif
  if (BT_tbl[channel] != NULL) {
  //  printf("using bt tbl\n");
    bt = BeaverTriple_new3(n, q, BT_tbl[channel]); // 事前計算
  } else {
  //  printf("without bt tbl\n");
    bt = BeaverTriple_new_channel(n, q, x->A->w, channel);
  //  bt = BeaverTriple_new0_channel(n, q, x->A->w, channel);
  }
  if (_party <= 0) {
    for (i=0; i<n; i++) {
      pa_set(ans->A, i, LMUL(pa_get(x->A,i), pa_get(y->A,i), q));
    }
  } else {
//  BeaverTriple bt = BeaverTriple_new2(n, q, x->A->w); // 事前計算
//  BeaverTriple bt = BeaverTriple_new3(n, q, BT_tbl[0]); // 事前計算
//    BeaverTriple bt = BeaverTriple_new(n, q, x->A->w);
    NEWT(share_array, a);
    *a = *x;
    a->A = bt->a;
    NEWT(share_array, b);
    *b = *x;
    b->A = bt->b;

  //  printf("x "); _print(x);
  //  printf("a "); _print(a);
  //  printf("y "); _print(y);
  //  printf("b "); _print(b);
    NEWT(share_array, ctmp);
    *ctmp = *x;
    ctmp->A = bt->b;
  //  printf("c "); _print(ctmp);

    share_array sigma, rho;
    sigma = vsub(x, a);
    rho = vsub(y, b);
#if 0
  }
  if (_party <= 0) {
    sigma = _dup(x);
    rho = _dup(y);
  } else {
    sigma = vsub(x, a);
    rho = vsub(y, b);
  }
#endif
    share_array sigma_c, rho_c;
    sigma_c = share_reconstruct_channel(sigma, channel); //
    rho_c = share_reconstruct_channel(rho, channel); //
#if 0
  if (_party > 0) {
#endif
    for (i=0; i<n; i++) {
      share_t tmp;
      if (_party == 1) {
        tmp = LMUL(pa_get(sigma_c->A, i), pa_get(rho_c->A, i), q);
      } else {
        tmp = 0;
      }
      tmp = MOD(tmp + LMUL(pa_get(a->A,i), pa_get(rho_c->A,i), q));  
      tmp = MOD(tmp + LMUL(pa_get(b->A,i), pa_get(sigma_c->A,i), q));
      tmp = MOD(tmp + pa_get(bt->c,i));
      pa_set(ans->A,i,tmp);
    }
    pa_free(bt->c);
    share_free(a);  share_free(b);
    share_free(sigma); share_free(rho);
    share_free(sigma_c); share_free(rho_c);
  //  BeaverTriple_free(bt);
  }
  BeaverTriple_free(bt);


  return ans;
}
#define _vmul vmul

//static share_array vmul(share_array x, share_array y)
//{
//  return vmul_channel(x, y, 0);
//}
#define vmul(x, y) vmul_channel(x, y, 0)

static void vmul_channel_(share_array a, share_array b, int channel)
{
  if (_party >  2) return;
  share_array tmp = vmul_channel(a, b, channel);
  pa_free(a->A);  *a = *tmp;  free(tmp);
}
#define _vmul_ vmul_

//static void vmul_(share_array a, share_array b)
//{
//  vmul_channel_(a, b, 0);
//}
#define vmul_(x, y) vmul_channel_(x, y, 0)


//////////////////////////////////////////////////
// ビット反転（0,1 以外の値の時は未定義）
//////////////////////////////////////////////////
static share_array vneg(share_array v)
{
  if (_party >  2) return NULL;
  int n = v->n;
  share_t q = v->q;
  NEWT(share_array, ans);
  *ans = *v;
  ans->A = pa_new(v->n, v->A->w);
  for (int i=0; i<n; i++) {
    if (_party == 2) {
      pa_set(ans->A, i, MOD(0 - pa_get(v->A,i)));
    } else {
      pa_set(ans->A, i, MOD(1 - pa_get(v->A,i)));
    }
  }
  return ans;
}
#define _vneg vneg

static void vneg_(share_array v)
{
  if (_party >  2) return;
  share_array tmp = vneg(v);
  pa_free(v->A);  *v = *tmp;  free(tmp);
}
#define _vneg_ vneg_

static share_array smul(share_t s, share_array a) // s は公開値
{
  if (_party >  2) return NULL;
  int n = a->n;
  share_t q = a->q;
  NEWT(share_array, ans);
  *ans = *a;
//  printf("smul s = %d\n", s);
  ans->A = pa_new(a->n, a->A->w);
  for (int i=0; i<n; i++) {
  //  printf("i=%d x = %d -> %d\n", i, pa_get(a->A, i), LMUL(s, pa_get(a->A, i), q));
    pa_set(ans->A, i, LMUL(s, pa_get(a->A, i), q));
  }
  return ans;
}
#define _smul smul

static void smul_(share_t s, share_array v)
{
  if (_party >  2) return;
  share_array tmp = smul(s, v);
  pa_free(v->A);  *v = *tmp;  free(tmp);
}
#define _smul_ smul_

static share_array smod(share_t s, share_array a) // s は公開値
{
  if (_party >  2) return NULL;
  int n = a->n;
  share_t q = a->q;
  NEWT(share_array, ans);
  *ans = *a;
//  printf("smul s = %d\n", s);
  ans->A = pa_new(a->n, a->A->w);
  for (int i=0; i<n; i++) {
  //  printf("i=%d x = %d -> %d\n", i, pa_get(a->A, i), LMUL(s, pa_get(a->A, i), q));
    pa_set(ans->A, i, pa_get(a->A, i) % s);
  }
  return ans;
}

static void smod_(share_t s, share_array v)
{
  if (_party >  2) return;
  share_array tmp = smod(s, v);
  pa_free(v->A);  *v = *tmp;  free(tmp);
}


/////////////////////////////////
// 論理演算
// 入力は 0, 1 のみ
/////////////////////////////////
_ AND(_ a, _ b)
{
  if (_party >  2) return NULL;
  return vmul(a, b);
}

_ OR(_ a, _ b)
{
  if (_party >  2) return NULL;
  _ ap = vneg(a);
  _ bp = vneg(b);
  _ ans = AND(ap, bp);
  vneg_(ans);
  _free(ap);
  _free(bp);
  return ans;
}

_ XOR(_ a, _ b)
{
  if (_party >  2) return NULL;
  _ ans = vadd(a, b);
  _ c = vmul(a, b);
  smul_(2, c);
  vsub_(ans, c);
  _free(c);
  return ans;
}

_ Equality2(_ a, _ b)
{
  if (_party >  2) return NULL;
  _ ans = XOR(a, b);
  vneg_(ans);
  return ans;
}





static share_array Perm_ID(share_array a)
{
  if (_party >  2) return NULL;
  if (a->q < a->n) {
    printf("Perm_ID: n = %d q = %d", a->n, (int)a->q);
  }
  NEWT(share_array, ans);
  ans->n = a->n;
  ans->q = a->q;
  ans->A = pa_new(a->n, a->A->w);
  for (int i=0; i<ans->n; i++) {
    if (_party == 2) {
      pa_set(ans->A, i, 0);
    } else {
      pa_set(ans->A, i, i);
    }
  }
  return ans;
}

static share_array Perm_ID2(int n, share_t q)
{
  if (_party >  2) return NULL;
  NEWT(share_array, ans);
  ans->n = n;
  ans->q = q;
  int w = blog(q-1)+1;
  ans->A = pa_new(n, w);
  for (int i=0; i<ans->n; i++) {
    if (_party == 2) {
      pa_set(ans->A, i, 0);
    } else {
      pa_set(ans->A, i, i);
    }
  }
  return ans;
}


static share_array share_const(int n, share_t v, share_t q)
{
//  if (_party >  2) return NULL;
  NEWT(share_array, ans);
  ans->n = n;
  ans->q = q;
  int k = blog(q-1)+1;
  ans->A = pa_new(n, k);
  for (int i=0; i<n; i++) {
    if (_party == 2) {
      pa_set(ans->A, i, 0);
    } else {
      pa_set(ans->A, i, v);
    }
  }
  return ans;
}
#define _const share_const



///////////////////////////////////////////////////
// 0,1 の xor を取る
// 位数は任意．結果の位数は元と同じ
// (位数が 2 ならローカルにできる)
///////////////////////////////////////////////////
static share_array share_xor(share_array b)
{
  if (_party >  2) return NULL;
  int n = len(b);
  share_t q = order(b);
  _ b0 = _const(n, 0, q);
  for (int i=0; i<n; i++) {
    pa_set(b0->A, i, pa_get(b->A, i) % 2); // 加法的シェアの最下位ビット
  }
  _ b1 = _const(n, 0, q);
  if (_party == 2) {
    for (int i=0; i<n; i++) {
      pa_set(b1->A, i, pa_get(b->A, i) % 2); // 加法的シェアの最下位ビット
    }
  }
  _ b2 = _const(n, 0, q);
  if (_party != 2) {
    for (int i=0; i<n; i++) {
      pa_set(b2->A, i, pa_get(b->A, i) % 2); // 加法的シェアの最下位ビット
    }
  }
  _ c = vmul(b1, b2);
  _free(b1);
  _free(b2);

  _smul_(2, c);
  _vsub_(b0, c);
  _free(c);

  return b0;
}
#define _xor share_xor

#include "dshare.h"
#include "compare.h"

#endif
