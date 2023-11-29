#ifndef _SHARE_H
 #define _SHARE_H

//#include "random.h"
//extern MT mt0, mt1[NC], mt2[NC], mts[NC];
//#ifndef _MTVAR
// #define _MTVAR
// MT mt0 = NULL;
// MT mt1[NC], mt2[NC], mts[NC];
//#endif

#include <stdio.h>
#include <stdlib.h>
#include "share_core.h"
#include "func.h"
#include <omp.h>

_ PrefixSum(_ v)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _dup(v);
  _ sum = _slice(v, 0, 1);
  _setpublic(sum, 0, 0);
  for (int i=0; i<n; i++) {
    _addshare(sum, 0, v, i);
    _setshare(ans, i, sum, 0);
  }
  _free(sum);
  return ans;
}

_ SuffixSum(_ v)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _dup(v);
  _ sum = _slice(v, 0, 1);
  _setpublic(sum, 0, 0);
  for (int i=n-1; i>=0; i--) {
    _addshare(sum, 0, v, i);
    _setshare(ans, i, sum, 0);
  }
  _free(sum);
  return ans;
}

_ Diff(_ v, share_t z)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _dup(v);
  _ prev = _slice(v, 0, 1);
  _setpublic(prev, 0, z);
  for (int i=0; i<n; i++) {
    _setshare(ans, i, v, i);
    _subshare(ans, i, prev, 0);
    _setshare(prev, 0, v, i);
  }
  _free(prev);
  return ans;
}

_ rank1(_ v)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _dup(v);
  _ sum = _slice(v, 0, 1);
  _setpublic(sum, 0, 0);
  for (int i=0; i<n; i++) {
    _addshare(sum, 0, v, i);
    _setshare(ans, i, sum, 0);
  }
  _free(sum);
  return ans;
}

_ rank0(_ v)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _dup(v);
  _ sum = _slice(v, 0, 1);
  _setpublic(sum, 0, 0);
  for (int i=0; i<n; i++) {
    _addpublic(sum, 0, 1);
    _subshare(sum, 0, v, i);
    _setshare(ans, i, sum, 0);
  }
  _free(sum);
  return ans;
}

_ sum(_ v)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _slice(v, 0, 1);
  for (int i=1; i<n; i++) {
    _addshare(ans, 0, v, i);
  }
  return ans;
}

_ rshift(_ v, share_t z)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _dup(v);
  _setshares(ans, 1, n, v, 0);
  _setpublic(ans, 0, z);
  return ans;
}

void rshift_(_ v, share_t z)
{
  if (_party >  2) return;
  _ tmp = rshift(v, z);
  pa_free(v->A);  *v = *tmp;  free(tmp);
}

_ lshift(_ v, share_t z)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _dup(v);
  _setshares(ans, 0, n-1, v, 1);
  _setpublic(ans, n-1, z);
  return ans;
}

void lshift_(_ v, share_t z)
{
  if (_party >  2) return;
  _ tmp = lshift(v, z);
  pa_free(v->A);  *v = *tmp;  free(tmp);
}

_ rrotate(_ v)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _dup(v);
  _setshares(ans, 1, n, v, 0);
  _setshare(ans, 0, v, n-1);
  return ans;
}

void rrotate_(_ v)
{
  if (_party >  2) return;
  _ tmp = rrotate(v);
  pa_free(v->A);  *v = *tmp;  free(tmp);
}

_ lrotate(_ v)
{
  if (_party >  2) return NULL;
  int n = len(v);
  _ ans = _dup(v);
  _setshares(ans, 0, n-1, v, 1);
  _setshare(ans, n-1, v, 0);
  return ans;
}

void lrotate_(_ v)
{
  if (_party >  2) return;
  _ tmp = lrotate(v);
  pa_free(v->A);  *v = *tmp;  free(tmp);
}


// if (f == 1) then a else b
// f * a + (1-f) * b
// = f * (a-b) + b
_ IfThenElse_channel(_ f, _ a, _ b, int channel)
{
  if (_party >  2) return NULL;
  int n = len(f);
  if (n !=len(a) || n != len(b)) {
    printf("IfThenElse f->n = %d a->n = %d b->n = %d\n", n, len(a), len(b));
  }
  _ ans = vsub(a, b);
  vmul_channel_(ans, f, channel);
  vadd_(ans, b);

  return ans;
}

//_ IfThenElse(_ f, _ a, _ b)
//{
//  return IfThenElse_channel(f, a, b, 0);
//}
#define IfThenElse(f, a, b) IfThenElse_channel(f, a, b, 0)

void addall(_ a, _ b)
{
  if (_party >  2) return;
  int n = len(a);
  for (int i=0; i<n; i++) {
    _addshare(a, i, b, 0);
  }
}

void setperm(_ a)
{
  if (_party >  2) return;
  int n = len(a);
  for (int i=0; i<n; i++) {
    _setpublic(a, i, i);
  }

}

_ StableSort(_ g)
{
  if (_party >  2) return NULL;
  int n = len(g);
  _ r0 = rank0(g);
  _ r1 = rank1(g);
  _ s0 = rshift(r0, 0);
  _ s1 = rshift(r1, 0);
  for (int i=0; i<n; i++) {
    _addshare(s1, i, r0, n-1);
  }
  _ sigma = IfThenElse(g, s1, s0);
  _free(r0); _free(r1);
  _free(s0); _free(s1);
  return sigma;
}

_ StableSort2_channel(_ g_, int channel)
{
  if (_party >  2) return NULL;
  int n = len(g_);
  int k = blog(n-1)+1;
  _ g;
  if (order(g_) == 2) {
    g = B2A_channel(g_, 1<<k, channel);
  } else {
    g = _dup(g_);
  //  g = B2A_channel(g_, 1<<k, channel);  // test 2023-08-05
  }
  _ r0 = rank0(g);
  _ r1 = rank1(g);
  _ s0 = rshift(r0, 0);
  _ s1 = rshift(r1, 0);
  for (int i=0; i<n; i++) {
    _addshare(s1, i, r0, n-1);
  }
  _ sigma = IfThenElse_channel(g, s1, s0, channel);
  _free(r0); _free(r1);
  _free(s0); _free(s1);
  _free(g);
  return sigma;
}

_ StableSort_channel2(_ g_, int channel)
{
  if (_party >  2) return NULL;
  int n = len(g_);
  int k = blog(n-1)+1;
  _ g;
  //printf("order g %d\n", order(g_));
  if (order(g_) == 2) {
    g = B2A_channel(g_, 1<<k, channel);
  } else {
    g = _dup(g_);
  }
  _ r0 = rank0(g);
  _ r1 = rank1(g);
  _ s0 = rshift(r0, 0);
  _ s1 = rshift(r1, 0);
  for (int i=0; i<n; i++) {
    _addshare(s1, i, r0, n-1);
  }
  _ sigma = IfThenElse_channel(g, s1, s0, channel);
  _free(r0); _free(r1);
  _free(s0); _free(s1);
  _free(g);
  return sigma;
}

_ StableSort_channel3(int d, _ b, int channel)
{
  if (_party >  2) return NULL;
  int n = len(b);
  int k = blog(n-1)+1;
  share_t q = 1<<k;
  int w = 1<<d;
  if (w > order(b)) w = order(b);

//  printf("b "); _print(b);
//  _ ohb = onehotvec_online_channel(b, q, 0, channel);
  _ ohb = onehotvec_channel(b, q, 0, channel);
//  printf("ohb  "); _print(ohb);
//  _check(ohb);
//  printf("ohb2 "); _print(ohb2);
  _ sum = _dup(ohb);
  for (int j=0; j<w; j++) {
    if (j != 0) _addshare(sum, j, sum, (j-1)+(n-1)*w);
    for (int i=1; i<n; i++) {
      _addshare(sum, j+i*w, sum, j+(i-1)*w);
    }
  }
//  printf("sum "); _print(sum);
  _ m = vmul(ohb, sum);
  _ pi = share_const(n, q-1, q);
  for (int i=0; i<n; i++) {
    for (int j=0; j<w; j++) {
      _addshare(pi, i, m, i*w+j);
    }
  }
//  printf("pi "); _print(pi);
  _free(m);
  _free(sum);
  _free(ohb);

  return pi;
}

_ vmul_shamir(_ x, _ y);
_ shamir_reduce(_ x, int step);
_ shamir_convert_channel(_ x, int channel);


_ StableSort_shamir_channel(int d, _ b, int channel)
{
  int n = len(b);
  int k = blog(n-1)+1;
  share_t q = 1<<k;
  int w = 1<<d;
  if (w > order(b)) w = order(b);

//  printf("len(b) %d order(b) %d\n", len(b), order(b));

//  if (_party <= 2) {
//    printf("b "); _print(b);
//    _ ohb2 = onehotvec_online_channel(b, q, 0, channel);
//    printf("ohb2 "); _print(ohb2);
//  }
  _ ohb = onehotvec_shamir_table_channel(d, b, q, PRE_OHS_tbl[d-1][channel], channel);
//  printf("ohb  "); _print(ohb);
//  _check(ohb);
//  printf("ohb2 "); _print(ohb2);
  _ sum = _dup(ohb);
  for (int j=0; j<w; j++) {
    if (j != 0) _addshare_shamir(sum, j, sum, (j-1)+(n-1)*w);
    for (int i=1; i<n; i++) {
      _addshare_shamir(sum, j+i*w, sum, j+(i-1)*w);
    }
  }
//  printf("sum "); _print(sum);
  _ m = vmul_shamir(ohb, sum);
//  printf("m "); _print(m);
  _ m2 = shamir_reduce(m, w);
//  printf("m2 "); _print(m2);
  _ m3 = shamir_convert_channel(m2, 0);
//  printf("m3 "); _print(m3);
  _ pi = share_const(n, q-1, q);
#if 0
  for (int i=0; i<n; i++) {
    for (int j=0; j<w; j++) {
      _addshare(pi, i, m, i*w+j);
    }
  }
#else
  vadd_(pi, m3);
#endif
//  printf("pi "); _print(pi);
  _free(m);
  _free(m2);
  _free(m3);
  _free(sum);
  _free(ohb);

  return pi;
}

//_ StableSort2(_ g_)
//{
//  return StableSort2_channel(g_, 0);
//}
#define StableSort2(g) StableSort2_channel(g, 0)
// in order to avoid compile error, comment out the 2 functions below: "find" and "StableSort_para"
// should fix these functions.
// _ find(_ v, _ g,_ num)
// {
//     int n = len(v);
//     _ ans = _dup(v);
//     _ l = (num >> 1) & 0b01; 
//     _ r = num & 0b01;
//     for (int i = 0; i < n; i++) {
//         _setshare(ans, i, (v[i] && l) && (g[i] && r), 0);
//     }
//     _free(sum);
//     return ans;
// }

// _ StableSort_para(_ g1, _ g0, _ cl)
// {
//     int n = len(g0);
//     _ r;
//     _ s;
//     _ sigma = _dup(g1);
//     _ m;
// #pragma omp parallel for
//     for (int i = 0; i < n; i++) {
//         g0[i] ^= cl;
//         g1[i] ^= cl;
//     }
//     _ v0 = share_reconst(g0);
//     _ v1 = share_reconst(g1);
// #pragma omp parallel for
//     for (int i = 0; i < 4; i++) {
//         _ r[i] = find(g1, g0, i);
//         _ s[i] = prefixsum(r[i]);
//     }
// #pragma omp parallel for
//     for (int i = 0; i < n; i++) {
//         m = ((g1[i] << 1) + g0[i]) ^ cl;
//         _ans = s[m][i];
//         for (int j = 0; j < m; j++) {
//             _addshare(ans, 0, r[j ^ cl], n);
//         }
//         _setshare(sigma, i, ans, 0);
//     }
//     _free(r);
//     _free(s);
//     _free(ans);
//     _free(v0);
//     _free(v1);
//     return sigma;
// }

//def InvPerm(sigma):
//  return AppInvPerm(Perm_ID(len(sigma)), sigma)
_ InvPerm(_ sigma)
{
  if (_party >  2) return NULL;
//  int n = len(sigma);
  _ perm = Perm_ID(sigma);
  _ ans = AppInvPerm(perm, sigma);
  _free(perm);
  return ans;
}

/************************************
def GenCycle(g):
  N = len(g)
  sigma = StableSort(g)
  t0 = vmul(Perm_ID(N), vneg(g))
  t1 = vmul(Perm_ID(N), g)
  u = AppInvPerm(t1, sigma)
  v = lshift(u, 0)
  y = AppPerm(v, sigma)
  pi = vadd(y, t0)
  w = rshift(u, 0)
  z = AppPerm(w, sigma)
  pi_inv = vadd(z, t0)
  pi_inv[0] = u[N-1]
  return (pi, pi_inv)
*************************************/
_pair GenCycle(_ g)
{
  if (_party >  2) {
    _pair ans = {NULL, NULL};
    return ans;
  }
  int n = len(g);
  _ sigma = StableSort(g);
//  printf("check sigma "); _print(sigma);
//  _check(sigma);
  _ perm = Perm_ID(g);
//  printf("perm "); _print(perm);
//  _check(perm);
  _ gneg = vneg(g);
//  printf("g    "); _print(g);
//  _check(g);
//  printf("gneg "); _print(gneg);
//  _check(gneg);
  _ t0 = vmul(perm, gneg);
  _ t1 = vmul(perm, g);
//  printf("t0 "); _print(t0);
//  _check(t0);
//  printf("t1 "); _print(t1);
//  _check(t1);
  _ u = AppInvPerm(t1, sigma);
//  printf("u "); _print(u);
//  _check(u);
  _ v = lshift(u, 0);
  _ y = AppPerm(v, sigma);
  _ pi = vadd(y, t0);
  _ w = rshift(u, 0);
  _ z = AppPerm(w, sigma);
  _ pi_inv = vadd(z, t0);
  _setshare(pi_inv, 0, u, n-1);

  _pair ans = {pi, pi_inv};

  _free(z);
  _free(w);
  _free(y);
  _free(v);
  _free(t0);
  _free(t1);
  _free(u);
  _free(gneg);
  _free(sigma);
  _free(perm);

  return ans;
}

_pair GenCycle2(_ g_)
{
  if (_party >  2) {
    _pair ans = {NULL, NULL};
    return ans;
  }
  int n = len(g_);
  _ sigma = StableSort2(g_);
//  _ g = B2A(g_, n);
  share_t k = blog(n-1)+1;
  share_t q = 1<<k;
  _ g = B2A(g_, q); // !!!
  _ perm = Perm_ID(g);
  _ gneg = vneg(g);
  _ t0 = vmul(perm, gneg);
  _ t1 = vmul(perm, g);
  _ u = AppInvPerm(t1, sigma);
  _ v = lshift(u, 0);
  _ y = AppPerm(v, sigma);
  _ pi = vadd(y, t0);
  _ w = rshift(u, 0);
  _ z = AppPerm(w, sigma);
  _ pi_inv = vadd(z, t0);
  _setshare(pi_inv, 0, u, n-1);

  _pair ans = {pi, pi_inv};

  _free(g);
  _free(z);
  _free(w);
  _free(y);
  _free(v);
  _free(t0);
  _free(t1);
  _free(u);
  _free(gneg);
  _free(sigma);
  _free(perm);

  return ans;
}

/********************************
def Propagate(g, v):
  (pi, pi_inv) = GenCycle(g)
  x = AppInvPerm(v, pi)
  y = x
  y[0] = 0
  z = PrefixSum(vsub(v, y))
  return z
********************************/
_ Propagate(_ g, _ v)
{
  if (_party >  2) return NULL;
  _pair tmp = GenCycle(g);
  _ pi = tmp.x;
  _free(tmp.y);

  _ x = AppInvPerm(v, pi);
  _setpublic(x, 0, 0);
  _ v2 = vsub(v, x);
  _ z = PrefixSum(v2);
  _free(pi);
  _free(x);
  _free(v2);
  return z;
}

_ Propagate2(_ g, _ v)
{
  if (_party >  2) return NULL;
  _pair tmp = GenCycle2(g);
  _ pi = tmp.x;
  _free(tmp.y);

  _ x = AppInvPerm(v, pi);
  _setpublic(x, 0, 0);
  _ v2 = vsub(v, x);
  _ z = PrefixSum(v2);
  _free(pi);
  _free(x);
  _free(v2);
  return z;
}

_bits Propagate_bits(_ g, _bits v)
{
  if (_party >  2) return NULL;
  NEWT(_bits, ans);
  NEWA(ans->a, share_array, v->d);
  for (int i = 0; i<v->d; i++) {
    ans->a[i] = Propagate(g, v->a[i]);
  }
  return ans;
}

/*******************************
def GroupSum(g,v):
    (pi, pi_inv) = GenCycle(g)
    s = SuffixSum(v)
    t = [0] * len(v)
    t[1:] = s[1:]
    y = AppInvPerm(t, pi_inv)
    z = vsub(s, y)
    return z
*******************************/
_ GroupSum(_ g, _ v)
{
  if (_party >  2) return NULL;
  _pair tmp = GenCycle(g);
  _free(tmp.x);
  _ pi_inv = tmp.y;
  _ s = SuffixSum(v);
  _ t = _dup(s);
  _setpublic(t, 0, 0);
  _ y = AppInvPerm(t, pi_inv);
  vsub_(s, y);

  _free(pi_inv);
  _free(t);
  _free(y);

  return s;
}

/*********************************
def select1(g):
  N = len(g)
  s00 = rshift(rank0(g), 0)
  m = sum(g) #   #ones
  s0 = vadd(s00, [m]*N)
  s1 = rshift(rank1(g), 0)
  sigma = IfThenElse(g, s1, s0)
  t0 = smul(N, vneg(g))
  t1 = vmul(Perm_ID(N), g)
  t = vadd(t0, t1)
  u = AppInvPerm(t, sigma)
  return u
*********************************/
_ select1(_ g)
{
  if (_party >  2) return NULL;
  int n = len(g);
  _ s0 = rank0(g);
  rshift_(s0, 0);
  _ m = sum(g);
  for (int i=0; i<n; i++) {
    _addshare(s0, i, m, 0);
  }
  _ s1 = rank1(g);
  rshift_(s1, 0);
  _ sigma = IfThenElse(g, s1, s0);
  _ gneg = vneg(g);
  _ t0 = smul(n, gneg);
  _ t1 = _dup(g);
  for (int i=0; i<n; i++) {
    _mulpublic(t1, i, i);
  }
  _ t = vadd(t0, t1);
  _ u = AppInvPerm(t, sigma);

  _free(s0);
  _free(s1);
  _free(m);
  _free(sigma);
  _free(gneg);
  _free(t0);
  _free(t1);
  _free(t);

  return u;
}

_ select0(_ v)
{
  if (_party >  2) return NULL;
  _ vn = vneg(v);
  _ ans = select1(vn);

  _free(vn);

  return ans;
}

_pair share_radix_sort_channel(_ a_, int channel)
{
  if (_party >  2) {
    _pair ans = {NULL, NULL};
    return ans;
  }
  _ a = _dup(a_);
//  _ pi = Perm_ID(a);
  int w = blog(a->n-1)+1;
  _ pi = Perm_ID2(a->n, 1<<w);
  share_t q = a->q;
//  share_t qb = order(a);
//  share_t qb = 1<<w;
  for (int k=1; k<q; k*=2) {
    // printf("k %d q %d\n", k, q);
//    printf("a "); _print(a);
//    _pair tmp = share_A2QB(a, q/k, qb);
//    printf("old bits "); _print(tmp2.y);
//    printf("old q    "); _print(tmp2.x);
//    _check(a);
    _pair tmp = share_A2QB_channel(a, q/k, 2, channel);
//    printf("new bits "); _print(tmp.y);
//    printf("new q    "); _print(tmp.x);
    //_ sigma = StableSort(tmp.y);
//    printf("bits "); _print(tmp.y);
//    _ sigma = StableSort(tmp.y);
      _ sigma = StableSort2_channel(tmp.y, channel);
//    printf("sigma "); _print(sigma);
    if (tmp.x->q > 1) {
      _move_(a, AppInvPerm_channel(tmp.x, sigma, channel));
    }
    _free(tmp.x);
    _free(tmp.y);
    _move_(pi, AppInvPerm_channel(pi, sigma, channel));
    _free(sigma);
  }
  _free(a);
  _ x = AppPerm_channel(a_, pi, channel);
  _pair ans = {x, pi};
  return ans;
}

//_pair share_radix_sort(_ a_)
//{
//  share_radix_sort_channel(a_, 0);
//}

/////////////////////////////////////////////////////////////////////
// 改良版 (2023-07-21)
/////////////////////////////////////////////////////////////////////
_pair share_radix_sort_channel2(_ a_, int channel)
{
  if (_party >  2) {
    _pair ans = {NULL, NULL};
    return ans;
  }
  _ a = _dup(a_);
//  _ pi = Perm_ID(a);
  int w = blog(a->n-1)+1;
  _ pi = Perm_ID2(a->n, 1<<w);
  share_t q = a->q;
//  share_t qb = order(a);
//  share_t qb = 1<<w;
  for (int k=1; k<q; k*=2) {
    // printf("k %d q %d\n", k, q);
//    printf("a "); _print(a);
//    _pair tmp = share_A2QB(a, q/k, qb);
//    printf("old bits "); _print(tmp2.y);
//    printf("old q    "); _print(tmp2.x);
//    _check(a);
  //  _pair tmp = share_A2QB_channel2(a, q/k, 2, channel);
    _pair tmp = share_A2QB_channel2(a, q/k, 1<<w, channel);
//    printf("new bits "); _print(tmp.y);
//    printf("new q    "); _print(tmp.x);
    //_ sigma = StableSort(tmp.y);
//    printf("bits "); _print(tmp.y);
//    _ sigma = StableSort(tmp.y);
      _ sigma = StableSort_channel2(tmp.y, channel);
//    printf("sigma "); _print(sigma);
    if (tmp.x->q > 1) {
      _move_(a, AppInvPerm_channel(tmp.x, sigma, channel));
    }
    _free(tmp.x);
    _free(tmp.y);
    _move_(pi, AppInvPerm_channel(pi, sigma, channel));
    _free(sigma);
  }
  _free(a);
  _ x = AppPerm_channel(a_, pi, channel);
  _pair ans = {x, pi};
  return ans;
}

//////////////////////////////////////////////////////
// d bit 単位
//////////////////////////////////////////////////////
_pair share_radix_sort_channel3(int d, _ a_, int channel)
{
//  int d = 2; // d ビット単位でソート
  int b = 1<<d;
#if 0
  if (_party >  2) {
    _pair ans = {NULL, NULL};
    return ans;
  }
#endif
  _ a = _dup(a_);
//  _ pi = Perm_ID(a);
  int w = blog(a->n-1)+1;
  _ pi = Perm_ID2(a->n, 1<<w);
  share_t q = a->q;
//  share_t qb = order(a);
//  share_t qb = 1<<w;
  for (int k=1; k<q; k*=b) {
  //  printf("a "); _print(a);
    // printf("k %d q %d\n", k, q);
//    printf("a "); _print(a);
//    _pair tmp = share_A2QB(a, q/k, qb);
//    printf("old bits "); _print(tmp2.y);
//    printf("old q    "); _print(tmp2.x);
//    _check(a);
  //  _pair tmp = share_A2QB_channel2(a, q/k, 2, channel);
    _pair tmp = {NULL, NULL};
    _ sigma;
#if 0
    if (order(a) == 2) {
      tmp = share_A2QB_channel2(a, q/k, 2, channel);
      sigma = StableSort_channel2(tmp.y, channel);
    } else {
      tmp = share_A2QD_channel(d, a, q/k, b, channel);
      sigma = StableSort_channel3(d, tmp.y, channel);
    }
#else
  //  printf("order(a) %d b %d\n", order(a), b);
    if (order(a) < b) {
    //  sigma = StableSort_channel3(d, a, channel);
      int d2 = blog(order(a)-1)+1;
      sigma = StableSort_shamir_channel(d2, a, channel);
      tmp.x = NULL;
      tmp.y = NULL;
    } else {
      tmp = share_A2QD_channel(d, a, q/k, b, channel);
    //  sigma = StableSort_channel3(d, tmp.y, channel);
      sigma = StableSort_shamir_channel(d, tmp.y, channel);
    }
#endif
  //  sigma = StableSort_channel3(d, tmp.y, channel);
//    printf("new bits "); _print(tmp.y);
//    printf("new q    "); _print(tmp.x);
    //_ sigma = StableSort(tmp.y);
//    printf("bits "); _print(tmp.y);
//    _ sigma = StableSort(tmp.y);
//      _ sigma = StableSort_channel3(d, tmp.y, channel);
//    printf("sigma "); _print(sigma);
    if (tmp.x != NULL) {
      if (_party == 3) {
        a->n = tmp.x->n;
        a->q = tmp.x->q;
      }
      if (tmp.x->q > 1) _move_(a, AppInvPerm_channel(tmp.x, sigma, channel));
      _free(tmp.x);
    }
    if (tmp.y != NULL) _free(tmp.y);
    _move_(pi, AppInvPerm_channel(pi, sigma, channel));
    _free(sigma);
  }
  _free(a);
  _ x = AppPerm_channel(a_, pi, channel);
  _pair ans = {x, pi};
  return ans;
}


extern precomp_tables PRE_OF_tbl[OF_MAX][NC];

#if 0
_pair share_radix_sort2(_ a_)
{
  if (_party >  2) {
    _pair ans = {NULL, NULL};
    return ans;
  }

  precomp_tables T = NULL;
#if 0
  if (_party <= 0) {
    T = func1bit3_read("PRE_OF-.dat");
  }
  if (_party == 1) {
    T = func1bit3_read("PRE_OF1.dat");
  }
  if (_party == 2) {
    T = func1bit3_read("PRE_OF2.dat");
  }
#endif
//  char *fname2 = precomp_fname("PRE_OF.dat");
//  T = func1bit3_read("PRE_OF.dat");
  T = PRE_OF_tbl[0];
//  free(fname2);

  _ a = _dup(a_);
  int w = blog(a->n-1)+1;
  _ pi = Perm_ID2(a->n, 1<<w);
  share_t q = a->q;
  for (int k=1; k<q; k*=2) {
    // printf("k %d q %d\n", k, q);
    //_pair tmp = share_A2QB(a, q/k, 2);
    //_pair tmp = share_A2QB2(a, q/k, 2);
//    _pair tmp = share_A2QB3(T, a, q/k, 2);
//    _ sigma = StableSort2(tmp.y);
    _pair tmp = share_A2QB3(T, a, q/k, 1<<w);
    _ sigma = StableSort(tmp.y);
    if (tmp.x->q > 1) {
      _move_(a, AppInvPerm(tmp.x, sigma));
    }
    _free(tmp.x);
    _free(tmp.y);
    _move_(pi, AppInvPerm(pi, sigma));
    _free(sigma);
  }
  _free(a);
  _ x = AppPerm(a_, pi);
  _pair ans = {x, pi};

  precomp_free_tables(T);

  return ans;
}
#endif
#define share_radix_sort(a) share_radix_sort_channel2(a, 0)
#define _radix_sort share_radix_sort

//////////////////////////////////////////////
// キーのタプルに関してソートする際に用いる関数
// pi はこれまでのキーでのソート結果を表す順列
// a は次のキー
//////////////////////////////////////////////
#if 0
_pair share_radix_sort_cont(_ pi, _ a)
{
  if (_party >  2) {
    _pair ans = {NULL, NULL};
    return ans;
  }
  _ key = AppPerm(a, pi);
  _pair tmp = share_radix_sort(key);
  _free(key);
  AppInvPerm_(pi, tmp.y);
  _move_(tmp.y, pi);
  return tmp;
}
#define _radix_sort_cont share_radix_sort_cont
#endif

_ share_radix_sort_bits(_bits a)
{
  if (_party >  2) return NULL;
  int d = a->d;
//  printf("b "); _print(a[0]);
//  _ pi = StableSort(a->a[0]);
  _ pi = StableSort2(a->a[0]);
//  printf("pi "); _print(pi);
  _ ap;
  _ sigma;
  for (int k=1; k<d; k++) {
  //  printf("k %d\n", k);
    ap = AppInvPerm(a->a[k], pi);
//    sigma = StableSort(ap);
    sigma = StableSort2(ap);
    _free(ap);
    _move_(pi, AppPerm(sigma, pi));
    _free(sigma);
  }
  return pi;
}
#define _radix_sort_bits share_radix_sort_bits

_ share_radix_sort_bits_channel(_bits a, int channel)
{
  if (_party >  2) return NULL;
  int d = a->d;
//  printf("b "); _print(a[0]);
//  _ pi = StableSort(a->a[0]);
  _ pi = StableSort2_channel(a->a[0], channel);
//  printf("pi "); _print(pi);
  _ ap;
  _ sigma;
  for (int k=1; k<d; k++) {
  //  printf("k %d\n", k);
    ap = AppInvPerm_channel(a->a[k], pi, channel);
    sigma = StableSort2_channel(ap, channel);
    _free(ap);
    _move_(pi, AppPerm_channel(sigma, pi, channel));
    _free(sigma);
  }
  return pi;
}
#define _radix_sort_bits2(a) share_radix_sort_bits_channel(a, 0)


/*
void genPer(int *c[], int per[], int j[], int k[], int first, int last) {
    if (first == last) {
        *
        * l = len(c);
        * c[l] = (share_t*)realloc(c, sizeof(share_t) * 4);
        * c[l] = share_new(4, q, j);
        *
        return;
    }
    else {
        for (int i = 0; i < last; i++) {
            if (k[i] == 0) {
                k[i] = 1;
                j[first] = per[i];
                genPer(per, j, k, first + 1, last);
                k[i] = 0;
            }
        }
    }
    return;
}
*/

// in order to fix compile error, comment out the function below: "share_radix_sort_parallel"
// should fix this function.
// _ share_radix_sort_parallel(_bits a)
// {
//     int d = a->d;
//     // share_t **c;
//     // c = (share_t **)malloc(4 *sizeof(share_t *));
//     //int per[4] = { 1, 2, 3, 4 };
//     //int j[4], c[4], k[4] = { 0 };
//     //genPer(per, j, k, 0, 4);
//     int cl, n = 24;
    
//     // _ pi = StableSort_para(a->a[1], a->a[0]);
//     _pi = StableSort2(a->a[i], a->a[0]);  // modify the above expression in order to fix a bug. "StableSort_para()"" get 3 arguments but the above get only 2 arguments.
//     _ ap;
//     _ ap1;
//     _ sigma;
//     int k;
//     for (k = 2; k < d; k = k + 2) {
//         ap = AppInvPerm(a->a[k], pi);
//         ap1 = AppInvPerm(a->a[k + 1], pi);
//         // cl = random0(4);
//         cl = RANDOM0(4);  // modify the above expression in order to fix a bug. "random0" isn't defined.
//         sigma = StableSort_para(ap1, ap, cl);
//         _free(ap);
//         _move_(pi, AppPerm(sigma, pi));
//         _free(sigma);
//     }
//     if (k > d) {
//         ap = AppInvPerm(a->a[k], pi);
//         _ sigma;
//         // sigma = StableSort_para(ap); //comment out this line to temporarily avoid compile error. until be fixed this line, "share_radix_sort_parallel" will not work correctly.
//         _free(ap);
//         _move_(pi, AppPerm(sigma, pi));
//         _free(sigma);
//     }
//     return pi;
// }
// #define _radix_sort_parallel share_radix_sort_parallel

/************************************************
def Grouping(V):
  n = len(V)
  G = [0]*n
  G[0] = 1
  for i in range(1,n):
    if V[i] != V[i-1]:
      G[i] = 1
  return G
************************************************/
_ Grouping(_ V)
{
  if (_party >  2) return NULL;
  _ Vp = rshift(V, 1);
  _subshare(Vp, 0, V, 0);
  _ ans = Equality2(V, Vp);
  vneg_(ans);
  _free(Vp);
  return ans;
}

_ Grouping_name(_ L, share_t q)
{
  if (_party >  2) return NULL;
  int n = len(L);
  _ V = _const(n, 0, q);
  for (int i=0; i<n; i++) {
    _setpublic(V, i, i);
  }
//  _ ans = Propagate(L, V);
  _ ans = Propagate2(L, V);
  _free(V);
  return ans;
}

_ Grouping_bit(_ V)
{
  if (_party >  2) return NULL;
  _ Vp = rshift(V, 1);
  _subshare(Vp, 0, V, 0);
  _ ans = Equality_bit(V, Vp);
  vneg_(ans);
  _free(Vp);
  return ans;
}

_ Grouping_bits(_bits V)
{
  if (_party >  2) return NULL;
  int d = V->d;
//  printf("i=0 V "); _print(V->a[0]);
  _ b = Grouping_bit(V->a[0]);
//  printf("i=0 b "); _print(b);
//  _check(b);
  for (int i=1; i<d; i++) {
    _ g = Grouping_bit(V->a[i]);
  //  printf("i=%d g ", i); _print(g);
  //  _check(g);
    _move_(b, OR(b, g));
  //  printf("i=%d b ", i); _print(b);
  //  _check(b);
    _free(g);
  }
  return b;
}

/***********************************************************
# v はアクセスしたい配列．長さ U
# idx は v のアクセスしたい要素の添え字の配列を 1 進数表現にしたもの．
# idx の値の最大値は len(v) 未満 
def BatchAccessUnary(v, idx):
  U = len(v)
  N = len(idx)
  sigma = StableSort(idx)
  n = sum(idx)
  X = v + ([0] * (N-U))
  Y = AppPerm(X, sigma)
  Z = Propagate(vneg(idx), Y)
  W = AppInvPerm(Z, sigma)
  return W[U:]
***********************************************************/
_ BatchAccessUnary(_ v, _ idx)
{
  if (_party >  2) return NULL;
  int U = len(v);
  int N = len(idx);
  _ sigma = StableSort(idx);
//  _ n = sum(idx); // 使ってない?
  _ zeros = _const(N-U, 0, order(v));
  _ X = _concat(v, zeros);
  _ Y = AppPerm(X, sigma);
  _ nidx = vneg(idx);
  _ Z = Propagate(nidx, Y);
  _ W = AppInvPerm(Z, sigma);
  _ ans = _slice(W, U, N);

  _free(sigma);
//  _free(n);
  _free(X);
  _free(Y);
  _free(nidx);
  _free(Z);
  _free(W);
  _free(zeros);

  return ans;
}


/************************************************
def Unary(x, U):
  N = len(x)
  i = 0
  X = [0] * (N+U)
  print('N', N, 'U', U)
  while i < U:
    X[i] = (i, 0, i) # (x, b, pos)
    i += 1
  i = 0
  while i < N:
    X[i+U] = (x[i], 1, i+U)
    i += 1
  print('X1', X)
  X.sort() # log N rounds
  print('X2', X)
  B = [b for (x, b, i) in X]
##  sigma = [i for (x, b, i) in X]
##  print(B)
  return B
************************************************/
_ Unary(_ x, int U)
{
  if (_party >  2) return NULL;
  int N = len(x);
  share_t q = order(x);
  _ X = _const(N+U, 0, q);
//  _ Y = _const(N+U, 0, N+U+1);
  int d = blog(N+U+1)+1;
  _ Y = _const(N+U, 0, 1<<d);
//  _ Z = _const(N+U, 0, N+U+1);
  for (int i=0; i<U; i++) {
    _setpublic(X, i, i);
    _setpublic(Y, i, 0);
//    _setpublic(Z, i, i);
  }
  for (int i=0; i<N; i++) {
    _setshare(X, i+U, x, i);
    _setpublic(Y, i+U, 1);
//    _setpublic(Z, i+U, i+U);
  }
  _pair tmp = share_radix_sort(X);
  _ sigma = _move(tmp.y);
  _ ans = AppPerm(Y, sigma);
  _free(sigma);
  _free(X);
  _free(Y);
//  _free(Z);
  _free(tmp.x);

  return ans;

}

_pair Unary2(_ x, int U)
{
  if (_party >  2) {
    _pair ans = {NULL, NULL};
    return ans;
  }
//  printf("Unary2 x "); _print(x);
  int N = len(x);
  share_t q = order(x);
  _ X = _const(N+U, 0, q);
  int d = blog(N+U+1)+1;
  _ Y = _const(N+U, 0, 1<<d);
  for (int i=0; i<U; i++) {
    _setpublic(X, i, i);
    _setpublic(Y, i, 0);
  }
  for (int i=0; i<N; i++) {
    _setshare(X, i+U, x, i);
    _setpublic(Y, i+U, 1);
  }
//  printf("X "); _print(X);
  _pair tmp = share_radix_sort(X);
  _pair ans;
//  printf("tmp.x "); _print(tmp.x);
//  printf("tmp.y "); _print(tmp.y);
  ans.x = AppPerm(Y, tmp.y);
//  printf("ans.x "); _print(ans.x);

  _ sigma = StableSort(ans.x);
//  printf("sigma "); _print(sigma);
  _ qq = AppInvPerm(tmp.y, sigma);
//  printf("qq "); _print(qq);
  _ rho = _slice(qq, U, U+N);
  for (int i=0; i<N; i++) {
    _addpublic(rho, i, -U);
  }
//  printf("rho "); _print(rho);
  ans.y = rho;

  _free(X);
  _free(Y);
//  _free(Z);
  _free(tmp.x);
  _free(tmp.y);
  _free(sigma);
  _free(qq);

  return ans;

}

_pair Unary_bits(_bits x, int U)
{
  if (_party >  2) {
    _pair ans = {NULL, NULL};
    return ans;
  }

  int N = len(x->a[0]);
  share_t q = order(x->a[0]);
  int d = blog(N+U-1)+1;
  _bits X = _const_bits(N+U, 0, 1<<d, x->d);
  _ Y = _const(N+U, 0, 1<<d);
  for (int i=0; i<U; i++) {
    _setpublic_bits(X, i, i);
    _setpublic(Y, i, 0);
  }
  for (int i=0; i<N; i++) {
    _setshare_bits(X, i+U, x, i);
    _setpublic(Y, i+U, 1);
  }
//  printf("X\n"); _print_bits(X);
  _ tmpy = share_radix_sort_bits(X);
  _pair ans;
//  printf("tmpy "); _print(tmpy);
//  _ tmpy_inv = AppInvPerm(Perm_ID2(N+U, order(tmpy)), tmpy);
  _ tmpy_inv = InvPerm(tmpy);
//  printf("tmpy_inv "); _print(tmpy_inv);
  ans.x = AppPerm(Y, tmpy_inv);
//  printf("ans.x "); _print(ans.x);

  _ sigma = StableSort(ans.x);
//  printf("sigma "); _print(sigma);
  _ qq = AppInvPerm(tmpy_inv, sigma);
//  printf("qq "); _print(qq);
  _ rho = _slice(qq, U, U+N);
  for (int i=0; i<N; i++) {
    _addpublic(rho, i, -U);
  }
//  printf("rho "); _print(rho);
  ans.y = rho;

  _free(sigma);
  _free_bits(X);
  _free(Y);
  _free(qq);
  _free(tmpy);
  _free(tmpy_inv);

  return ans;

}



/************************************************
def BatchAccess(v, idx):
  I = Unary(idx, len(v))
  print('idx', idx, 'unary', I)
  return BatchAccessUnary(v, I)
************************************************/
// idx は単調増加である必要は無い
_ BatchAccess(_ v, _ idx)
{
  if (_party >  2) return NULL;
//  _ I = Unary(idx, m);
  _pair tmp = Unary2(idx, len(v));
  _ I = tmp.x;
  _ sigma = tmp.y;
//  printf("BatchAccess idx "); _print(idx);
//  printf("BatchAccess I "); _print(I);
//  printf("BatchAccess sigma "); _print(sigma);
  _ ans = BatchAccessUnary(v, I);
//  printf("BatchAccess: ans "); _print(ans); 
//  _pair tmp = share_radix_sort(I);
//  _ ans2 = AppInvPerm(ans, tmp.y);
  _ ans2 = AppInvPerm(ans, sigma); // idx で指定した順番に並び替える
//  printf("BatchAccess: ans2"); _print(ans2); 
  _free(I);
  _free(sigma);
  _free(ans);
  return ans2;
}

_bits BatchAccess_bits(_bits v, _ idx)
{
  if (_party >  2) return NULL;
//  _ I = Unary(idx, m);
  _pair tmp = Unary2(idx, len(v->a[0]));
  _ I = tmp.x;
  _ sigma = tmp.y;
//  printf("idx "); _print(idx);
//  printf("unary "); _print(I);
//  printf("sigma "); _print(sigma);
  int d = v->d;
  int n = v->a[0]->n;
  share_t q = v->a[0]->q;
  _bits ans = _const_bits(n, 0, q, d);

//  _pair tmp3 = share_radix_sort(idx);
//  printf("sigma "); _print(sigma);
//  printf("tmp3.y "); _print(tmp3.y);

  for (int i=0; i<d; i++) {
    _ tmp2 = BatchAccessUnary(v->a[i], I);
  //  _move_(ans->a[i], AppInvPerm(tmp2, tmp3.y));
    _move_(ans->a[i], AppInvPerm(tmp2, sigma));
    _free(tmp2);
  }
  _free(sigma);
  _free(I);
  return ans;
}

_bits BatchAccess_bits_bits(_bits v, _bits idx)
{
  if (_party >  2) return NULL;

  _pair tmp = Unary_bits(idx, len(v->a[0]));
  _ I = tmp.x;
  _ sigma = tmp.y;
//  printf("b idx "); _print_bits(idx);
//  printf("b unary "); _print(I);
//  printf("b sigma "); _print(sigma);

  int d = v->d;
  int n = v->a[0]->n;
  share_t q = v->a[0]->q;
  _bits ans;
  ans = _const_bits(n, 0, q, d);

  for (int i=0; i<d; i++) {
    _ tmp2 = BatchAccessUnary(v->a[i], I);
    _move_(ans->a[i], AppInvPerm(tmp2, sigma));
    _free(tmp2);
  }
  _free(I);
  _free(sigma);
  return ans;
}

void precomp_tables_new(void)
{
  bt_tbl_init();
  of_tbl_init();
  b2a_tbl_init();
//  BT_tbl[0] = BeaverTriple_read("PRE_BT.dat");
//  PRE_OF_tbl[0] = func1bit3_read("PRE_OF.dat");
//  PRE_B2A_tbl[0] = func1bit3_read("PRE_B2A.dat");
}

void precomp_tables_free(void) 
{
//  BeaverTriple_free_tables(BT_tbl[0]);
//  precomp_free_tables(PRE_OF_tbl[0]);
//  precomp_free_tables(PRE_B2A_tbl[0]);
  for (int i=0; i<NC; i++) {
    if (BT_tbl[i] != NULL) BeaverTriple_free_tables(BT_tbl[i]);
    if (PRE_B2A_tbl[i] != NULL) precomp_free_tables(PRE_B2A_tbl[i]);
    for (int j=1; j<=OF_MAX; j++) {
      if (PRE_OF_tbl[j-1][i] != NULL) precomp_free_tables(PRE_OF_tbl[j-1][i]);
    }
    for (int j=1; j<=ONEHOT_MAX; j++) {
      if (PRE_OHA_tbl[j-1][i] != NULL) precomp_free_tables(PRE_OHA_tbl[j-1][i]);
      if (PRE_OHX_tbl[j-1][i] != NULL) precomp_free_tables(PRE_OHX_tbl[j-1][i]);
    }
    if (PRE_DS_tbl[i] != NULL) ds_tbl_list_free(PRE_DS_tbl[i]);
  }
  long BT_total=0, B2A_total=0;
  long OHA_total[ONEHOT_MAX], OHX_total[ONEHOT_MAX];
  long OF_total[OF_MAX];
  long DS_total=0;
  for (int j=1; j<=ONEHOT_MAX; j++) {
    OHA_total[j-1] = 0;
    OHX_total[j-1] = 0;
  }
  for (int j=1; j<=OF_MAX; j++) {
    OF_total[j-1] = 0;
  }
  for (int i=0; i<NC; i++) {
    BT_total += BT_count[i];
    B2A_total += PRE_B2A_count[i];
    for (int j=1; j<=ONEHOT_MAX; j++) {
      OHA_total[j-1] += PRE_OHA_count[j-1][i];
      OHX_total[j-1] += PRE_OHA_count[j-1][i];
    }
    for (int j=1; j<=OF_MAX; j++) {
      OF_total[j-1] += PRE_OF_count[j-1][i];
    }
    DS_total += PRE_DS_count[i];
  }
  printf("BT   %ld\n", BT_total);
  printf("B2A  %ld\n", B2A_total);
  printf("DS   %ld\n", DS_total);
  printf("OHA%d %ld\n", 1, OHA_total[1-1]);
  printf("OHA%d %ld\n", 2, OHA_total[2-1]);
  printf("OHA%d %ld\n", 3, OHA_total[3-1]);
  printf("OHX%d %ld\n", 1, OHX_total[1-1]);
  printf("OHX%d %ld\n", 2, OHX_total[2-1]);
  printf("OHX%d %ld\n", 3, OHX_total[3-1]);
  printf("OF%d  %ld\n", 1, OF_total[1-1]);
  printf("OF%d  %ld\n", 2, OF_total[2-1]);
  printf("OF%d  %ld\n", 3, OF_total[3-1]);
}

void PRG_initialize3(int num_parties) {
  unsigned long init[5];
//  init[4] = 0;
//  mt0 = MT_init_by_array(init, 5);
  mt0 = MT_init_by_array(MT_init[_party], 5); // 各 party のみが知る乱数
  if (_party <= 0) {
    for (int i=0; i<5; i++) init[i] = MT_init[1][i];
    for (int i=0; i<NC; i++) {
    //  init[3] = i;
    //  init[4] = 1;
      init[3] = MT_init[1][i]+i;
      mt1[i] = MT_init_by_array(init, 5); // party 0 と 1 が共有する乱数
      if (_party == 0) mpc_send(TO_PARTY1, init, sizeof(init[0])*5);
    }
    for (int i=0; i<5; i++) init[i] = MT_init[2][i];
    for (int i=0; i<NC; i++) {
    //  init[3] = i;
    //  init[4] = 2;
      init[3] = MT_init[2][i]+i;
      mt2[i] = MT_init_by_array(init, 5); // party 0 と 2 が共有する乱数
      if (_party == 0) mpc_send(TO_PARTY2, init, sizeof(init[0])*5);
    }
  }
  if (_party == 1 || _party == 2) {
    unsigned long init[5];
    for (int i=0; i<NC; i++) {
      mpc_recv(FROM_SERVER, init, sizeof(init[0])*5);
      mts[i] = MT_init_by_array(init, 5); // party 0 と自分が共有する乱数
    }
  }
  if (num_parties == 4) {
    if (_party == 3) {
      for (int i=0; i<5; i++) init[i] = MT_init[3][i];
      mpc_send(TO_PARTY1, init, sizeof(init[0])*5);
      for (int i=0; i<NC; i++) {
        init[3] = MT_init[_party][i]+i;
        mt3[i] = MT_init_by_array(init, 5); // party 3 と 1 が共有する乱数
      }
    }
    if (_party == 1) {
      mpc_recv(TO_PARTY3, MT_init[3], sizeof(MT_init[3][0])*5);
      for (int i=0; i<NC; i++) {
        init[3] = MT_init[3][i]+i;
        mt3[i] = MT_init_by_array(init, 5); // party 3 と 1 が共有する乱数
      }
    }
  }
}

void PRG_initialize(void)
{
  PRG_initialize3(3);
}

void PRG_free(void)
{
  printf("MT0 %ld\n", mt0->count);
  MT_free(mt0);
  if (_party <= 0) {
    for (int i=0; i<NC; i++) {
      printf("MT1[%d] %ld\n", i, mt1[i]->count);
      printf("MT2[%d] %ld\n", i, mt2[i]->count);
      MT_free(mt1[i]);
      MT_free(mt2[i]);
    }
  }
  if (_party == 1 || _party == 2) {
    for (int i=0; i<NC; i++) {
      printf("MTS[%d] %ld\n", i, mts[i]->count);
      MT_free(mts[i]);
    }
  }
}

_ vmul_shamir(_ x, _ y)
{
  int n = len(x);
  if (n != len(y)) {
    printf("vmul_shamir_channel: len(x)=%d len(y)=%d\n", n, len(y));
    exit(1);
  }

  if (_party <= 0) {
    return vmul(x, y);
  }

  _ ans;
  share_t q = order(x);

  ans = _dup(x);
  for (int i=0; i<n; i++) {
    share_t t;
    if (_party == 1) t = MOD(3*pa_get(x->A, i)*pa_get(y->A, i));
    if (_party == 2) t = MOD(3*q - 3*pa_get(x->A, i)*pa_get(y->A, i));
    if (_party == 3) t = MOD(pa_get(x->A, i)*pa_get(y->A, i));
    pa_set(ans->A, i, t);
  }

  return ans;
}

_ shamir_reduce(_ x, int step)
{
  int n = len(x);
  int m = n/step;
  if (m * step != n) {
    printf("shamir_reduce: n = %d step = %d\n", n, step);
    exit(1);
  }
  _ ans = _const(m, 0, order(x));
  for (int i=0; i<m; i++) {
    for (int j=0; j<step; j++) {
      _addshare_shamir(ans, i, x, i*step+j);
    }
  }
  return ans;
}

_ shamir_convert_channel(_ x, int channel)
{
  int n = len(x);

  if (_party <= 0) {
    return _dup(x);
  }

  _ ans;
  share_t q = order(x);
  if (_party == 1 || _party == 2) {
    ans = _dup(x);
    _ tmp = _dup(x);
    if (_party == 1) {
    //  unsigned long init[5];
    //  mpc_recv(TO_PARTY3, init, sizeof(init[0])*5);
    //  MT m3 = MT_init_by_array(init, 5);
      for (int i=0; i<n; i++) {
      //  share_t r = RANDOM(m3, q);
        share_t r = RANDOM(mt3[channel], q);
        pa_set(tmp->A, i, r);
      }
    //  MT_free(m3);
    } else {
      mpc_recv_share_channel(TO_PARTY3, tmp, channel);
    }
    vadd_(ans, tmp);
    _free(tmp);
  }
  if (_party == 3) {
  //  unsigned long init[5]={0x123, 0x234, 0x345, 0x456, 0};
  //  MT m3 = MT_init_by_array(init, 5);
    _ a1 = share_dup(x);
    _ a2 = share_dup(x);
    for (int i=0; i<n; i++) {
      share_t t = pa_get(x->A, i);
    //  share_t r = RANDOM(m3, q);
      share_t r = RANDOM(mt3[channel], q);
      pa_set(a1->A, i, r);
      pa_set(a2->A, i, MOD(q+t-r));
    }
    //MT_free(m3);
    //mpc_send(channel+TO_PARTY1, init, sizeof(init[0])*5);
    mpc_send_share_channel(TO_PARTY2, a2, channel);
    _free(a1);
    _free(a2);
    ans = NULL;
  }
  return ans;
}



#ifndef _TESTVAR
 #define _TESTVAR
 long total_btn = 0, total_bt2 = 0;
 long total_perm = 0;

 long send_1 = 0, send_2 = 0, send_3 = 0, send_4 = 0, send_5 = 0, send_6 = 0, send_7 = 0, send_8 = 0;
#endif

#endif
