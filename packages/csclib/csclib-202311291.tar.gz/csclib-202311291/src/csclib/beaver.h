#ifndef _BEAVER_H
 #define _BEAVER_H

#include "mpc.h"
#include "bits.h"
#include "random.h"
#include "mman.h"
#include "precompute.h"

extern long total_btn, total_bt2;


#define ID_BEAVERTRIPLE1 0x19
#define ID_BEAVERTRIPLE2 0x1A


#ifndef MOD
 #define MOD(x) (((x)%(q)+(q)*1) % (q))
#endif

///////////////////////////////////
// 整数の掛け算
// int は 32 bit, long は 64 bit と仮定
// int*int だと桁あふれするので long で計算
///////////////////////////////////
share_t LMUL(share_t x, share_t y, share_t q)
{
  long tmp = x;
  tmp = tmp * y;
  tmp = tmp % q;
  tmp = tmp + q;
  tmp = tmp % q;
  if (tmp != MOD(x*y)) {
    printf("LMUL x %d y %d q %d %d %d\n", x, y, q, (int)tmp, MOD(x*y));
  }
  return tmp;
}



typedef struct {
  packed_array a, b, c;
}* BeaverTriple;

typedef struct {
  precomp_table T1, T2;
  MMAP *map;
}* BT_tables;

//extern BT_tables BT_tbl[];
BT_tables BT_tbl[NC];
long BT_count[NC];


//////////////////////////////////////////////////
// Beaver triple の計算
// a1, a2, b1, b2, c1, c2 のうち c2 だけ通信
// それ以外は乱数の種から生成
//////////////////////////////////////////////////
BeaverTriple BeaverTriple_new_channel(int n, share_t q, int w, int channel)
{
  if (_party >  2) return NULL;
  //printf("BeaverTriple n=%d q=%d\n", n, q);
  if (q == 2) {
    total_bt2 += n;
  } else {
    total_btn += n;
  }
  NEWT(BeaverTriple, bt);

  if (_party <= 0) {
    packed_array Aa1, Aa2, Ab1, Ab2, Ac1, Ac2;
    Aa1 = pa_new(n, w);
    Aa2 = pa_new(n, w);
    Ab1 = pa_new(n, w);
    Ab2 = pa_new(n, w);
    Ac1 = pa_new(n, w);
    Ac2 = pa_new(n, w);
    share_t a, b, c;
    share_t a1, a2, b1, b2, c1, c2;

#if 1111
    for (int i=0; i<n; i++) {
      a1 = RANDOM(mt1[channel], q);
      pa_set(Aa1, i, a1);
      b1 = RANDOM(mt1[channel], q);
      pa_set(Ab1, i, b1);
      c1 = RANDOM(mt1[channel], q);
      pa_set(Ac1, i, c1);
    //  printf("(%d, a1 %d, b1 %d, c1 %d)", i, a1, b1, c1);
    }
    //printf("\n");
    for (int i=0; i<n; i++) {
      a2 = RANDOM(mt2[channel], q);
      pa_set(Aa2, i, a2);
      b2 = RANDOM(mt2[channel], q);
      pa_set(Ab2, i, b2);
    }
    for (int i=0; i<n; i++) {
      a1 = pa_get(Aa1, i);
      a2 = pa_get(Aa2, i);
      b1 = pa_get(Ab1, i);
      b2 = pa_get(Ab2, i);
      a = MOD(a1+a2);
      b = MOD(b1+b2);
      c = LMUL(a, b, q);
      c1 = pa_get(Ac1, i);
      c2 = MOD(c - c1);
      pa_set(Ac2, i, c2);
      //printf("(%d, a2 %d, b2 %d, c2 %d)", i, a2, b2, c2);
    }
    //printf("\n");
#else
    unsigned long init1[5]={0x123, 0x234, 0x345, 0x456, 0};
    init1[4] = 1; // rand();
    MT m1 = MT_init_by_array(init1, 5);
    for (int i=0; i<n; i++) {
      a1 = RANDOM(m1, q);
      pa_set(Aa1, i, a1);
      b1 = RANDOM(m1, q);
      pa_set(Ab1, i, b1);
      c1 = RANDOM(m1, q);
      pa_set(Ac1, i, c1);
      printf("(%d, a1 %d, b1 %d, c1 %d)", i, a1, b1, c1);
    }
    printf("\n");
    MT_free(m1);
    unsigned long init2[5]={0x123, 0x234, 0x345, 0x456, 0};
    init2[4] = 2; // rand();
    MT m2 = MT_init_by_array(init2, 5);
    for (int i=0; i<n; i++) {
      a2 = RANDOM(m2, q);
      pa_set(Aa2, i, a2);
      b2 = RANDOM(m2, q);
      pa_set(Ab2, i, b2);
    }
    MT_free(m2);
    for (int i=0; i<n; i++) {
      a1 = pa_get(Aa1, i);
      a2 = pa_get(Aa2, i);
      b1 = pa_get(Ab1, i);
      b2 = pa_get(Ab2, i);
      a = MOD(a1+a2);
      b = MOD(b1+b2);
      c = LMUL(a, b, q);
      c1 = pa_get(Ac1, i);
      c2 = MOD(c - c1);
      pa_set(Ac2, i, c2);
      printf("(%d, a2 %d, b2 %d, c2 %d)", i, a2, b2, c2);
    }
    printf("\n");
#endif

#if 0 // old
    for (int i=0; i<n; i++) {
      //a1 = RANDOM(m1, q);
      a1 = RANDOM(mt1[channel], q);
      pa_set(Aa1, i, a1);
      //b1 = RANDOM(m1, q);
      b1 = RANDOM(mt1[channel], q);
      pa_set(Ab1, i, b1);
      //c1 = RANDOM(m1, q);
      c1 = RANDOM(mt1[channel], q);
      pa_set(Ac1, i, c1);
      //if (i == 0) printf("(%d, %d,%d,%d)", i, a1, b1, c1);
      printf("(%d, a1 %d, b1 %d, c1 %d)", i, a1, b1, c1);
    }
    printf("\n");
    for (int i=0; i<n; i++) {
      a1 = pa_get(Aa1, i);
      a2 = pa_get(Aa2, i);
      b1 = pa_get(Ab1, i);
      b2 = pa_get(Ab2, i);
      a = MOD(a1+a2);
      b = MOD(b1+b2);
      c = LMUL(a, b, q);
      c1 = pa_get(Ac1, i);
      c2 = MOD(c - c1);
      pa_set(Ac2, i, c2);
      printf("(%d, a2 %d, b2 %d, c2 %d)", i, a2, b2, c2);
    }
    printf("\n");
    for (int i=0; i<n; i++) {
      //a2 = RANDOM(m2, q);
      a2 = RANDOM(mt2[channel], q);
      pa_set(Aa2, i, a2);
      //b2 = RANDOM(m2, q);
      b2 = RANDOM(mt2[channel], q);
      pa_set(Ab2, i, b2);
    }
    for (int i=0; i<n; i++) {
      a1 = pa_get(Aa1, i);
      a2 = pa_get(Aa2, i);
      b1 = pa_get(Ab1, i);
      b2 = pa_get(Ab2, i);
      a = MOD(a1+a2);
      b = MOD(b1+b2);
      c = LMUL(a, b, q);
      c1 = pa_get(Ac1, i);
      c2 = MOD(c - c1);
      pa_set(Ac2, i, c2);
    //  if (i == 0) printf("[%d, %d,%d,%d]", i, a2, b2, c2);
      printf("(%d, a2 %d, b2 %d, c2 %d)", i, a2, b2, c2);
    }
    printf("\n");
#endif

    int size = pa_size(Aa1);
  //  mpc_send(channel*2+TO_PARTY1, init1, sizeof(init1[0])*5); // テスト
  //  mpc_send(channel*2+TO_PARTY2, init2, sizeof(init2[0])*5);
    mpc_send(channel*2+TO_PARTY2, Ac2->B, size);
    pa_free(Aa1);  pa_free(Aa2);
    pa_free(Ab1);  pa_free(Ab2);
    pa_free(Ac1);  pa_free(Ac2);
    bt->a = NULL;
    bt->b = NULL;
    bt->c = NULL;
  } else {
    share_t a1, a2, b1, b2, c1;
  //  unsigned long init[5]={0x123, 0x234, 0x345, 0x456, 0};
    bt->a = pa_new(n, w);
    bt->b = pa_new(n, w);
    bt->c = pa_new(n, w);
    int size = pa_size(bt->a);
  //  mpc_recv(channel*2+FROM_SERVER, init, sizeof(init[0])*5); // テスト
  //  init_by_array(init, 5);
  //  MT m0 = MT_init_by_array(init, 5);
#if 1111

    if (_party == 1) {
      for (int i=0; i<n; i++) {
      //  a1 = RANDOM(m0, q);
        a1 = RANDOM(mts[channel], q);
        pa_set(bt->a, i, a1);
        //b1 = RANDOM(m0, q);
        b1 = RANDOM(mts[channel], q);
        pa_set(bt->b, i, b1);
        //c1 = RANDOM(m0, q);
        c1 = RANDOM(mts[channel], q);
        pa_set(bt->c, i, c1);
      //  if (i == 0) printf("(%d, %d,%d,%d)", i, a1, b1, c1);
      //  printf("(%d, a1 %d, b1 %d, c1 %d)", i, a1, b1, c1);
      }
    } else { // party 2
      unsigned long init[5]={0x123, 0x234, 0x345, 0x456, 0};
      init[4] = 2; // rand();
      MT m0 = MT_init_by_array(init, 5);
      for (int i=0; i<n; i++) {
        //a2 = RANDOM(m0, q);
        a2 = RANDOM(mts[channel], q);
        pa_set(bt->a, i, a2);
        //b2 = RANDOM(m0, q);
        b2 = RANDOM(mts[channel], q);
        pa_set(bt->b, i, b2);
      }
      mpc_recv(channel*2+FROM_SERVER, bt->c->B, size); // c2
#if 0
      for (int i=0; i<n; i++) {
        share_t a2, b2, c2;
        a2 = pa_get(bt->a, i);
        b2 = pa_get(bt->b, i);
        c2 = pa_get(bt->c, i);
        printf("(%d, a2 %d, b2 %d, c2 %d)", i, a2, b2, c2);
      }
      printf("\n");
#endif
    }
#else
    if (_party == 1) {
      unsigned long init[5]={0x123, 0x234, 0x345, 0x456, 0};
      init[4] = 1; // rand();
      MT m0 = MT_init_by_array(init, 5);
      for (int i=0; i<n; i++) {
        a1 = RANDOM(m0, q);
        pa_set(bt->a, i, a1);
        b1 = RANDOM(m0, q);
        pa_set(bt->b, i, b1);
        c1 = RANDOM(m0, q);
        pa_set(bt->c, i, c1);
        printf("(%d, a1 %d, b1 %d, c1 %d)", i, a1, b1, c1);
      }
      printf("\n");
      MT_free(m0);
    } else { // party 2
      unsigned long init[5]={0x123, 0x234, 0x345, 0x456, 0};
      init[4] = 2; // rand();
      MT m0 = MT_init_by_array(init, 5);
      for (int i=0; i<n; i++) {
        a2 = RANDOM(m0, q);
        pa_set(bt->a, i, a2);
        b2 = RANDOM(m0, q);
        pa_set(bt->b, i, b2);
      }
      MT_free(m0);
      mpc_recv(channel*2+FROM_SERVER, bt->c->B, size); // c2
#if 1
      for (int i=0; i<n; i++) {
        share_t a2, b2, c2;
        a2 = pa_get(bt->a, i);
        b2 = pa_get(bt->b, i);
        c2 = pa_get(bt->c, i);
        printf("(%d, a2 %d, b2 %d, c2 %d)", i, a2, b2, c2);
      }
      printf("\n");
#endif
    }

#endif
  }

  return bt;
}

BeaverTriple BeaverTriple_new0_channel(int n, share_t q, int w, int channel)
{
  if (_party >  2) return NULL;
//  printf("BeaverTriple n=%d q=%d\n", n, q);
  if (q == 2) {
    total_bt2 += n;
  } else {
    total_btn += n;
  }
  NEWT(BeaverTriple, bt);

  if (_party <= 0) {
    packed_array Aa1, Aa2, Ab1, Ab2, Ac1, Ac2;
    Aa1 = pa_new(n, w);
    Aa2 = pa_new(n, w);
    Ab1 = pa_new(n, w);
    Ab2 = pa_new(n, w);
    Ac1 = pa_new(n, w);
    Ac2 = pa_new(n, w);
    share_t a, b, c;
    share_t a1, a2, b1, b2, c1, c2;

    unsigned long init1[5]={0x123, 0x234, 0x345, 0x456, 0};
    init1[4] = 1; // rand();
    MT m1 = MT_init_by_array(init1, 5);

    for (int i=0; i<n; i++) {
      a1 = RANDOM(m1, q);
      pa_set(Aa1, i, a1);
      b1 = RANDOM(m1, q);
      pa_set(Ab1, i, b1);
      c1 = RANDOM(m1, q);
      pa_set(Ac1, i, c1);
      printf("(%d, a1 %d, b1 %d, c1 %d)\n", i, a1, b1, c1);
    }
    MT_free(m1);

    unsigned long init2[5]={0x123, 0x234, 0x345, 0x456, 0};
    init2[4] = 2; // rand();
    MT m2 = MT_init_by_array(init2, 5);

    for (int i=0; i<n; i++) {
      a2 = RANDOM(m2, q);
      pa_set(Aa2, i, a2);
      b2 = RANDOM(m2, q);
      pa_set(Ab2, i, b2);
    }
    MT_free(m2);

    for (int i=0; i<n; i++) {
      a1 = pa_get(Aa1, i);
      a2 = pa_get(Aa2, i);
      b1 = pa_get(Ab1, i);
      b2 = pa_get(Ab2, i);
      a = MOD(a1+a2);
      b = MOD(b1+b2);
      c = LMUL(a, b, q);
      c1 = pa_get(Ac1, i);
      c2 = MOD(c - c1);
      pa_set(Ac2, i, c2);
      printf("[%d, a2 %d, b2 %d, c2 %d]\n", i, a2, b2, c2);
    }
    int size = pa_size(Ac2);
    mpc_send(channel*2+TO_PARTY1, init1, sizeof(init1[0])*5);
    mpc_send(channel*2+TO_PARTY2, init2, sizeof(init2[0])*5);
    mpc_send(channel*2+TO_PARTY2, Ac2->B, size);
    pa_free(Aa1);  pa_free(Aa2);
    pa_free(Ab1);  pa_free(Ab2);
    pa_free(Ac1);  pa_free(Ac2);
    bt->a = NULL;
    bt->b = NULL;
    bt->c = NULL;
  } else {
    share_t a1, a2, b1, b2, c1;
    bt->a = pa_new(n, w);
    bt->b = pa_new(n, w);
    bt->c = pa_new(n, w);
    int size = pa_size(bt->c);
    unsigned long init[5]={0x123, 0x234, 0x345, 0x456, 0};
    mpc_recv(channel*2+FROM_SERVER, init, sizeof(init[0])*5);
    printf("seed\n");
    for (int i=0; i<5; i++) printf("%x ", init[i]);
    printf("\n");
    MT m0 = MT_init_by_array(init, 5);
    if (_party == 1) {
      for (int i=0; i<n; i++) {
        a1 = RANDOM(m0, q);
        pa_set(bt->a, i, a1);
        b1 = RANDOM(m0, q);
        pa_set(bt->b, i, b1);
        c1 = RANDOM(m0, q);
        pa_set(bt->c, i, c1);
        printf("(%d, a1 %d, b1 %d, c1 %d)\n", i, a1, b1, c1);
      }
    } else { // party 2
      for (int i=0; i<n; i++) {
        a2 = RANDOM(m0, q);
        pa_set(bt->a, i, a2);
        b2 = RANDOM(m0, q);
        pa_set(bt->b, i, b2);
      }
      mpc_recv(channel*2+FROM_SERVER, bt->c->B, size); // c2
      for (int i=0; i<n; i++) {
        share_t a2, b2, c2;
        a2 = pa_get(bt->a, i);
        b2 = pa_get(bt->b, i);
        c2 = pa_get(bt->c, i);
        printf("[%d, a2 %d, b2 %d, c2 %d]\n", i, a2, b2, c2);
      }
    }
    MT_free(m0);
  }

  return bt;
}


//BeaverTriple BeaverTriple_new(int n, share_t q, int w)
//{
//  return BeaverTriple_new_channel(n, q, w, 0);
//}
#define BeaverTriple_new(n, q, w) BeaverTriple_new_channel(n, q, w, 0)

void BeaverTriple_free(BeaverTriple bt)
{
  if (_party >  2) return;
//  pa_free(bt->a);
//  pa_free(bt->b);
//  pa_free(bt->c);
  free(bt);
}

#if 0
//////////////////////////////////////////////////
// Beaver triple の計算 (事前計算)
//////////////////////////////////////////////////
void BeaverTriple_precompute(int n, share_t q, int w)
{
  if (_party >  2) return;
  FILE *f;

  // party 1 が使う乱数
  unsigned long init1[5]={0x123, 0x234, 0x345, 0x456, 0};
  init1[4] = 1; // rand();
  MT m1 = MT_init_by_array(init1, 5);

  f = fopen("BT.dat.1", "wb");
  if (f == NULL) {
    perror("BeaverTriple_precompute:1\n");
  }
  writeuint(1,ID_BEAVERTRIPLE1,f);
  for (int i=0; i<5; i++) {
    writeuint(sizeof(init1[0]), init1[i], f);
  }
  fclose(f);

  // party 2 が使う乱数
  unsigned long init2[5]={0x123, 0x234, 0x345, 0x456, 0};
  init2[4] = 2; // rand();
  MT m2 = MT_init_by_array(init2, 5);

  packed_array Ac2 = pa_new(n, w);

  share_t a, b, c;
  share_t a1, a2, b1, b2, c1, c2;
  for (int i=0; i<n; i++) {
    a1 = RANDOM(m1, q);
    b1 = RANDOM(m1, q);
    c1 = RANDOM(m1, q);

    a2 = RANDOM(m2, q);
    b2 = RANDOM(m2, q);

    a = MOD(a1+a2);
    b = MOD(b1+b2);
    c = LMUL(a, b, q);
    c2 = MOD(c - c1);
    pa_set(Ac2, i, c2);
  }

  f = fopen("BT.dat.2", "wb");
  if (f == NULL) {
    perror("BeaverTriple_precompute:2\n");
  }
  writeuint(1,ID_BEAVERTRIPLE2,f);
  for (int i=0; i<5; i++) {
    writeuint(sizeof(init2[0]), init2[i], f);
  }
  pa_write(Ac2, f);
  fclose(f);

  pa_free(Ac2);
  MT_free(m1);
  MT_free(m2);

}

unsigned long bt_init[5];
packed_array bt_a = NULL;
long bt_i = 0;
MT bt_mt = NULL;
MMAP *bt_map = NULL;

//////////////////////////////////////////////////
// Beaver triple の計算 (事前計算を利用)
//////////////////////////////////////////////////
BeaverTriple BeaverTriple_new2(int n, share_t q, int w)
{
  if (_party >  2) return NULL;
  if (bt_a == NULL) {
    if (_party <= 0) {
      bt_a = (void*)1;
    } else {
      uchar *p;
      if (_party == 1) {
        bt_map = mymmap("BT.dat.1");
      } else {
        bt_map = mymmap("BT.dat.2");
      }
      if (bt_map->addr==NULL) {
        perror("mmap2\n");
        exit(1);
      }
      p = (uchar *)bt_map->addr;
      int id = getuint(p,0,1);  p += 1;
      if (id != ID_BEAVERTRIPLE1 + _party-1) {
        printf("BeaverTriple_new2: id = %d is not supported.\n",id);
        exit(1);
      }
      for (int i=0; i<5; i++) {
        bt_init[i] = getuint(p,0,sizeof(bt_init[0]));  p += sizeof(bt_init[0]);
      }
      bt_mt = MT_init_by_array(bt_init, 5);
      if (_party == 1) {
        bt_a = (void*)1;
      } else {
        bt_a = pa_read(&p);
        bt_i = 0;
      }
    }
  }

//  printf("BeaverTriple2 n=%d q=%d\n", n, q);
  if (q == 2) {
    total_bt2 += n;
  } else {
    total_btn += n;
  }
  NEWT(BeaverTriple, bt);

  if (_party <= 0) {
    bt->a = NULL;
    bt->b = NULL;
    bt->c = NULL;
  } else {
    share_t a1, a2, b1, b2, c1, c2;
    bt->a = pa_new(n, w);
    bt->b = pa_new(n, w);
    bt->c = pa_new(n, w);
    if (_party == 1) {
      for (int i=0; i<n; i++) {
        a1 = RANDOM(bt_mt, q);
        pa_set(bt->a, i, a1);
        b1 = RANDOM(bt_mt, q);
        pa_set(bt->b, i, b1);
        c1 = RANDOM(bt_mt, q);
        pa_set(bt->c, i, c1);
      }
    } else { // party 2
      for (int i=0; i<n; i++) {
        a2 = RANDOM(bt_mt, q);
        pa_set(bt->a, i, a2);
        b2 = RANDOM(bt_mt, q);
        pa_set(bt->b, i, b2);
        c2 = pa_get(bt_a, bt_i++) % q;
        pa_set(bt->c, i, c2);
      }
    }
  }

  return bt;
}
#endif

//////////////////////////////////////////////////
// Beaver triple の計算 (事前計算，新しいやつ)
//////////////////////////////////////////////////
void BeaverTriple_precomp(int n, share_t q, char *fname)
{
  if (_party >  2) return;
  FILE *f1, *f2;

  char *fname1 = precomp_fname(fname, 1);
  char *fname2 = precomp_fname(fname, 2);

  f1 = fopen(fname1, "wb");
  f2 = fopen(fname2, "wb");


  // party 1 が使う乱数
  unsigned long init1[5]={0x123, 0x234, 0x345, 0x456, 0};
  init1[4] = 1; // rand();
  MT m1 = MT_init_by_array(init1, 5);

  //writeuint(1,ID_BEAVERTRIPLE1,f1);
  precomp_write_seed(f1, n*3, q, init1);



  // party 2 が使う乱数
  unsigned long init2[5]={0x123, 0x234, 0x345, 0x456, 0};
  init2[4] = 2; // rand();
  MT m2 = MT_init_by_array(init2, 5);

  int k = blog(q-1)+1;
  packed_array Ac2 = pa_new(n, k);

  share_t a, b, c;
  share_t a1, a2, b1, b2, c1, c2;
  for (int i=0; i<n; i++) {
    a1 = RANDOM(m1, q);
    b1 = RANDOM(m1, q);
    c1 = RANDOM(m1, q);

    a2 = RANDOM(m2, q);
    b2 = RANDOM(m2, q);

    a = MOD(a1+a2);
    b = MOD(b1+b2);
    c = LMUL(a, b, q);
    c2 = MOD(c - c1);
    pa_set(Ac2, i, c2);
  //  printf("BT(a = %d (%d+%d) b = %d (%d+%d) c = %d (%d+%d))", a, a1, a2, b, b1, b2, c, c1, c2);
  }

  //writeuint(1,ID_BEAVERTRIPLE2,f1);
  precomp_write_seed(f2, n*2, q, init2);
//  pa_write(Ac2, f2);
  precomp_write_share(f2, Ac2);

  pa_free(Ac2);
  MT_free(m1);
  MT_free(m2);

  fclose(f1);
  fclose(f2);

}

void BeaverTriple_free_tables(BT_tables T)
{
  if (T == NULL) return;
  if (_party >  2) return;
  if (_party <= 0) return;
  precomp_free(T->T1);
  if (_party == 2) precomp_free(T->T2);
  mymunmap(T->map);
  free(T);
}

///////////////////////////////////////////////////////////
// 前計算の表を読み込む
///////////////////////////////////////////////////////////
BT_tables BeaverTriple_read(char *fname)
{
  if (_party >  2) return NULL;
  if (_party <= 0) {
    NEWT(BT_tables, T);
    T->map = NULL;
    T->T1 = NULL;
    T->T2 = NULL;
    return T;
  }
  char *fname2 = precomp_fname(fname, _party);

  NEWT(BT_tables, T);

  MMAP *map = NULL;
  map = mymmap(fname2);
  uchar *p = (uchar *)map->addr;
  T->T1 = precomp_read(&p);
  if (_party == 2) T->T2 = precomp_read(&p);
  T->map = map;

  free(fname2);

  return T;
}

//////////////////////////////////////////////////
// Beaver triple の計算 (事前計算を利用，新しいやつ)
//////////////////////////////////////////////////
BeaverTriple BeaverTriple_new3(int n, share_t q, BT_tables T)
{
  if (_party >  2) return NULL;
  NEWT(BeaverTriple, bt);

  BT_count[0] += n; // channel?
  if (_party <= 0) {
    bt->a = NULL;
    bt->b = NULL;
    bt->c = NULL;
    return bt;
  }

  share_t a1, a2, b1, b2, c1, c2;
  int k = blog(q-1)+1;
  bt->a = pa_new(n, k);
  bt->b = pa_new(n, k);
  bt->c = pa_new(n, k);
  if (_party == 1) {
    for (int i=0; i<n; i++) {
      a1 = precomp_get(T->T1) % q;
      pa_set(bt->a, i, a1);
      b1 = precomp_get(T->T1) % q;
      pa_set(bt->b, i, b1);
      c1 = precomp_get(T->T1) % q;
      pa_set(bt->c, i, c1);
    }
  } else { // party 2
    for (int i=0; i<n; i++) {
      a2 = precomp_get(T->T1) % q;
      pa_set(bt->a, i, a2);
      b2 = precomp_get(T->T1) % q;
      pa_set(bt->b, i, b2);
      c2 = precomp_get(T->T2) % q;
      pa_set(bt->c, i, c2);
    }
  }
  return bt;
}

void bt_tbl_init(void)
{
  for (int i=0; i<NC; i++) {
    BT_tbl[i] = NULL;
    BT_count[i] = 0;
  }
}

void bt_tbl_read(int channel, char *fname)
{
  BT_tbl[channel] = BeaverTriple_read(fname);
}



#endif
