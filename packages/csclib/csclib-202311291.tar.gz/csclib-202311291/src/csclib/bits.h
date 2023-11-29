#ifndef _BITS_H
 #define _BITS_H

//#define FAST_BIT

typedef long i64;
typedef unsigned long u64;
typedef unsigned char uchar;

#ifdef FAST_BIT
 #define logQ 5
// typedef unsigned int bitvec_t;
 typedef u64 bitvec_t;
#else
 #define logQ 6
 typedef u64 bitvec_t;
#endif

#define _Q (1L<<logQ) // 小ブロック(1ワード)のサイズ

#define ID_PACKEDARRAY 0x18
#define ID_SHARE 0x1C

/////////////////////////////////////////////////////
// 整数の桁数を求める
// to store an integer in [0,x-1], we need blog(x-1)+1 bits
/////////////////////////////////////////////////////
static int blog(u64 x)
{
int l;
  l = -1;
  while (x>0) {
    x>>=1;
    l++;
  }
  return l;
}



static int setbit(bitvec_t *B, i64 i,int x)
{
  i64 j,l;

  j = i / _Q;
  l = i & (_Q-1);
  if (x==0) B[j] &= (~(1L<<(l)));
  else if (x==1) B[j] |= (1L<<(l));
  else {
    printf("error setbit x=%d\n",x);
    exit(1);
  }
  return x;
}

static int getbit(bitvec_t *B, i64 i)
{
  i64 j,l;

  j = i >> logQ;
  l = i & (_Q-1);
  return (B[j] >> (l)) & 1;
}

static u64 getbits(bitvec_t *B, i64 i, int d)
{
  u64 x,z;

  if (d == 0) return 0;
  B += (i >>logQ);
  i &= (_Q-1);
  if (i+d <= _Q) {
    x = B[0];
    x <<= i;
    x >>= (_Q-d);  // Q==64, d==0 だと動かない
  } else {
    x = B[0] << i;
    x >>= _Q-d;
    z = B[1] >> (_Q-(i+d-_Q));
    x += z;
  }
  return x;
}

static void setbits(bitvec_t *B, i64 i, int d, u64 x)
{
  u64 y,m;
  int d2;

  B += (i>>logQ);
  i &= (_Q-1);

  while (i+d > _Q) {
    d2 = _Q-i; // x の上位 d2 ビットを格納
    y = x >> (d-d2);
    m = (1<<d2)-1;
    *B = (*B & (~m)) | y;
    B++;  i=0;
    d -= d2;
    x &= (1L<<d)-1; // x の上位ビットを消去
  }
  m = (1L<<d)-1;
  y = x << (_Q-i-d);
  m <<= (_Q-i-d);
  *B = (*B & (~m)) | y;

}

static void writeuint(int k, i64 x, FILE *f)
{
  int i;
  for (i=k-1; i>=0; i--) {
    fputc(x & 0xff,f); // little endian
    x >>= 8;
  }
}

static u64 getuint(uchar *s, i64 i, i64 w)
{
  u64 x;
  i64 j;
  s += i*w;
  x = 0;
  for (j=0; j<w; j++) {
    x += ((u64)(*s++)) << (j*8);
  }
  return x;
}

static void putuint(uchar *s, i64 i, i64 x, i64 w)
{
  i64 j;
  s += i*w;
  for (j=0; j<w; j++) {
    *s++ = x & 0xff;
    x >>= 8;
  }
}



typedef struct {
  i64 n;
  int w;
  bitvec_t *B;
}* packed_array;

static packed_array pa_new(i64 n, int w)
{
  i64 i,x;

#ifdef FAST_BIT
  w = _Q;
#endif

//  if (w >= 32) {
//    printf("warning: w=%d\n",w);
//  }

//  w = 32;  比較用

  NEWT(packed_array, p);
  p->n = n;  p->w = w;
  x = (n / _Q)*w + ((n % _Q)*w + _Q-1) / _Q;
  NEWA(p->B, bitvec_t, x);
  for (i=0; i<x; i++) p->B[i] = 0;
  return p;
}

static int pa_size(packed_array p)
{
  i64 n = p->n;
  i64 w = p->w;
  i64 x;

  x = (n / _Q)*w + ((n % _Q)*w + _Q-1) / _Q;
  return (int)(x*sizeof(bitvec_t));
}

static void pa_free(packed_array p)
{
  free(p->B);
  free(p);
}

static void pa_free_map(packed_array p)
{
  //free(p->B);
  free(p);
}

static u64 pa_get(packed_array p, i64 i)
{
  int w;
  bitvec_t *B;

#ifdef FAST_BIT
  return (u64)p->B[i];
#endif

  w = p->w;
  B = p->B + (i>>logQ)*w;
  i = (i % _Q)*w;

  return getbits(B,i,p->w);
}

static void pa_set(packed_array p, i64 i, u64 x)
{
  int w;
  bitvec_t *B;

#ifdef FAST_BIT
  p->B[i] = x;
  return;
#endif


#if 1
  if (x < 0 || (long)x > (1L<<p->w)) {
    printf("pa_set: x=%ld w=%d\n",x,p->w);
  }
  if (i < 0 || i >= p->n) {
    printf("pa_set: i=%ld n=%ld\n",i,p->n);
  }
#endif
  w = p->w;
  B = p->B + (i>>logQ)*w;
  i = (i % _Q)*w;

  setbits(B,i,p->w,x);
}



i64 pa_write(packed_array pa, FILE *f)
{
  i64 size = 0;
  writeuint(1,ID_PACKEDARRAY,f);
  writeuint(sizeof(pa->n), pa->n, f);
  writeuint(sizeof(pa->w), pa->w, f);
  size += 1 + sizeof(pa->n) + sizeof(pa->w);

  i64 x = (pa->n / _Q)*pa->w + ((pa->n % _Q)*pa->w + _Q-1) / _Q;
  for (i64 i=0; i<x; i++) {
    writeuint(sizeof(pa->B[0]), pa->B[i], f); size += sizeof(pa->B[0]);
  }

  return size;
}

packed_array pa_read(uchar **map)
{
  i64 x;
  uchar *p;

  p = *map;

  x = getuint(p,0,1);  p += 1;
  if (x != ID_PACKEDARRAY) {
    printf("pa_read: id = %ld is not supported.\n", x);
    exit(1);
  }

  NEWT(packed_array, pa);

  pa->n = getuint(p,0,sizeof(pa->n));  p += sizeof(pa->n);
  pa->w = getuint(p,0,sizeof(pa->w));  p += sizeof(pa->w);
  pa->B = (bitvec_t *)p;
  x = (pa->n / _Q)*pa->w + ((pa->n % _Q)*pa->w + _Q-1) / _Q;
  p += x * sizeof(pa->B[0]);

  *map = p;

  return pa;
}

void pa_print(packed_array a)
{
  for (int i=0; i<a->n; i++) {
    printf("%ld ", pa_get(a, i));
  }
  printf("\n");
}

#undef logQ
#undef _Q


#endif
