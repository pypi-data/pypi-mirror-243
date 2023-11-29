////////////////////////////////////////////////////////
// MPC全般の処理（シェアに関係することは書かない）
////////////////////////////////////////////////////////

#ifndef _MPC_H
 #define _MPC_H

#include <pthread.h>
#include "comm.h"

#ifndef NC
 #define NC 1
#endif


#define NP (NC*2+1)




typedef void *(*thread_func)(void *);

typedef struct parties {
  char *addr;
  int port;
}* parties;

extern parties *_Parties;
extern int _party;

#ifndef _Parties_VAR
 #define _Parties_VAR
 parties *_Parties;
 int _party = 0;
#endif

//extern void* BT_tbl[];
//extern void* PRE_OF_tbl[];
//extern void* PRE_B2A_tbl[];

void bt_tbl_init(void);
void of_tbl_init(void);
void b2a_tbl_init(void);
void bt_tbl_read(int channel, char *fname);
void of_tbl_read(int d, int channel, char *fname);
void b2a_tbl_read(int channel, char *fname);
void onehot_tbl_init(void);
void onehot_tbl_read(int d, int xor, int channel, char *fname);
void onehot_shamir_tbl_read(int d, int channel, char *fname);
void ds_tbl_read(int channel, int n, int inverse, char *fname);

#define scmp(p, q) strncasecmp(p, q, strlen(q))

extern unsigned long MT_init[4][5];

void read_option(FILE *fin)
{
  char buf[1000];
  char fname[1000];
  int channel;
  if (fgets(buf, 1000, fin) == NULL) return;
  while (1) {
    if (scmp(buf, "[mt_seeds]") == 0) {
      unsigned long init[5];
      int party;
      while (1) {
        if (fgets(buf, 1000, fin) == NULL) return;
        if (sscanf(buf, " %d %ld %ld %ld %ld %ld", &party, &init[0], &init[1], &init[2], &init[3], &init[4]) != 6) break;
        if (party < 0 || party > 3) {
          printf("error party %d\n", party);
          exit(1);
        }
        for (int i=0; i<5; i++) MT_init[party][i] = init[i];
      }
    } else if (scmp(buf, "[pre_bt]") == 0) {
      while (1) {
        if (fgets(buf, 1000, fin) == NULL) return;
        if (sscanf(buf, " %d %s", &channel, fname) != 2) break;
        if (channel >= NC) {
          printf("error channel %d NC %d\n", channel, NC);
          exit(1);
        }
        bt_tbl_read(channel, fname);
        printf("BT_tbl %d %s\n", channel, fname);
      }
    } else if (scmp(buf, "[pre_of]") == 0) {
      while (1) {
        int d;
        if (fgets(buf, 1000, fin) == NULL) return;
        if (sscanf(buf, " %d %d %s", &d, &channel, fname) != 3) break;
        if (channel >= NC) {
          printf("error channel %d NC %d\n", channel, NC);
          exit(1);
        }
        of_tbl_read(d, channel, fname);
        printf("PRE_OF_tbl bits=%d channel=%d %s\n", d, channel, fname);
      }
    } else if (scmp(buf, "[pre_b2a]") == 0) {
      while (1) {
        if (fgets(buf, 1000, fin) == NULL) return;
        if (sscanf(buf, " %d %s", &channel, fname) != 2) break;
        if (channel >= NC) {
          printf("error channel %d NC %d\n", channel, NC);
          exit(1);
        }
        b2a_tbl_read(channel, fname);
        printf("PRE_B2A_tbl %d %s\n", channel, fname);
      }
    } else if (scmp(buf, "[pre_onehot]") == 0) {
      while (1) {
        int d, xor;
        if (fgets(buf, 1000, fin) == NULL) return;
        if (sscanf(buf, " %d %d %d %s", &d, &xor, &channel, fname) != 4) break;
        if (channel >= NC) {
          printf("error channel %d NC %d\n", channel, NC);
          exit(1);
        }
        if (_party <= 2) {
          onehot_tbl_read(d, xor, channel, fname);
          printf("PRE_OH_tbl bits=%d xor=%d channel=%d %s\n", d, xor, channel, fname);
        }
      }
    } else if (scmp(buf, "[pre_onehot_shamir]") == 0) {
      while (1) {
        int d, xor;
        if (fgets(buf, 1000, fin) == NULL) return;
        if (sscanf(buf, " %d %d %s", &d, &channel, fname) != 3) break;
        if (channel >= NC) {
          printf("error channel %d NC %d\n", channel, NC);
          exit(1);
        }
        onehot_shamir_tbl_read(d, channel, fname);
        printf("PRE_OHS_tbl bits=%d channel=%d %s\n", d, channel, fname);
      }
    } else if (scmp(buf, "[pre_ds]") == 0) {
      while (1) {
        int n, inverse;
        if (fgets(buf, 1000, fin) == NULL) return;
        if (sscanf(buf, " %d %d %d %s", &n, &inverse, &channel, fname) != 4) break;
        if (channel >= NC) {
          printf("error channel %d NC %d\n", channel, NC);
          exit(1);
        }
        ds_tbl_read(channel, n, inverse, fname);
        printf("PRE_DS_tbl %d %d %d %s\n", n, inverse, channel, fname);
      }
    } else if (buf[0] == '#') { // skip comments
      if (fgets(buf, 1000, fin) == NULL) break;
    } else {
      if (fgets(buf, 1000, fin) == NULL) break;
    }
  }
}

static parties* party_read(int num_parties)
{
  FILE *fin;
//  comm C;
  char buf[1000];
//  char dest_addr[100];
//  int  dest_port;
//  int  recv_port;
  int  i;

  parties *P;
//  NEWA(P, parties, num_parties);
  P = (parties *)malloc(num_parties*sizeof(*P));

  fin = fopen("config.txt", "r");
  if (fin == NULL) {
    printf("cannot open config.txt\n");
    exit(1);  
  }
  i = 0;
  while (i < num_parties) {
    char addr[100];
    int port;
    if (fgets(buf, 1000, fin) == NULL) break;
    sscanf(buf, " %s %d", addr, &port);
  //  NEW(P[i], 1);
    P[i] = (parties)malloc(sizeof(**P));
    P[i]->addr = strdup(addr);
    P[i]->port = port;
    printf("party %d %s:%d\n", i, addr, port);
    i++;
  }
  read_option(fin);
  fclose(fin);
  return P;
}

static void party_free(parties *P, int num_parties)
{
  for (int i=0; i<num_parties; i++) {
    free(P[i]->addr);
    free(P[i]);
  }
  free(P);
}

comm _C[NP+NC];
#define TO_PARTY1 1
#define TO_PARTY2 2
#define FROM_PARTY1 1
#define FROM_PARTY2 2
#define TO_SERVER 1
#define FROM_SERVER 1
#define TO_PAIR 2
#define FROM_PAIR 2
//#define TO_PARTY3 3
//#define FROM_PARTY3 3
#define TO_PARTY3 (NC*2+1)
#define FROM_PARTY3 0

//char send_queue[NP][BUFFER_SIZE];
//int send_queue_idx[NP] = {0,0,0};
int send_queue_idx[NP+NC];
char *send_queue[NP+NC];

typedef struct thread_param {
  pthread_t th;
  thread_func func; // 不要?
  void *args;       // 不要?
}* thread_param;

thread_param thread_new(thread_func func, void *args)
{
  NEWT(thread_param, param);
  param->func = func;
  param->args = args;

  int ret = pthread_create(&param->th, NULL, func, args);
  if (ret != 0) {
    printf("thread_new: ret %d\n", ret);
    exit(1);
  }
  return param;
}

void thread_end(thread_param param)
{
  int ret;
  ret = pthread_join(param->th, NULL);
  if (ret != 0) {
    printf("thread_end: ret %d\n", ret);
  }
  free(param);
}

typedef struct comm_init_args {
  int server;
  int port;
  char *dest_name;
  comm ans;
}* comm_init_args;

void *comm_init_thread(void *arg_)
{
  comm_init_args arg = (comm_init_args)arg_;
  if (arg->server) {
    arg->ans = comm_init_server(arg->port);
  } else {
    arg->ans = comm_init_client(arg->dest_name, arg->port);
  }
  return NULL;
}

void precomp_tables_new(void); 
void precomp_tables_free(void); 


static void mpc_start(int num_parties)
{
  precomp_tables_new();

  if (_party < 0) {
    party_read(0);
    return;
  }
  _Parties = party_read(num_parties);
  printf("party %d\n", _party);

  for (int i=0; i<NP+NC; i++) _C[i] = NULL;


  thread_param params[NP+1+NC];

  struct comm_init_args args[NP+1+NC];

  if (_party == 0) {
    for (int i=0; i<NC; i++) {
      args[i*2+FROM_PARTY1].server = 1;
      args[i*2+FROM_PARTY1].port = _Parties[0]->port + i+1;
      params[i*2+FROM_PARTY1] = thread_new(comm_init_thread, &args[i*2+FROM_PARTY1]);
      printf("i=%d port %d\n", i*2+FROM_PARTY1, args[i*2+FROM_PARTY1].port);
      args[i*2+FROM_PARTY2].server = 1;
      args[i*2+FROM_PARTY2].port = _Parties[0]->port + i+2;
      params[i*2+FROM_PARTY2] = thread_new(comm_init_thread, &args[i*2+FROM_PARTY2]);
      printf("i=%d port %d\n", i*2+FROM_PARTY2, args[i*2+FROM_PARTY2].port);
    }
    if (num_parties >= 4) {
      args[FROM_PARTY3].server = 1;
      args[FROM_PARTY3].port = _Parties[0]->port + FROM_PARTY3;
      params[FROM_PARTY3] = thread_new(comm_init_thread, &args[FROM_PARTY3]);
      printf("i=%d port %d\n", FROM_PARTY3, args[FROM_PARTY3].port);
    }
  }
  if (_party == 1) {
    for (int i=0; i<NC; i++) {
      args[i*2+TO_SERVER].server = 0;
      args[i*2+TO_SERVER].dest_name = _Parties[0]->addr;
      args[i*2+TO_SERVER].port = _Parties[0]->port + i*2 + _party;
      params[i*2+TO_SERVER] = thread_new(comm_init_thread, &args[i*2+TO_SERVER]);
      printf("i=%d server %s port %d\n", i, args[i*2+TO_SERVER].dest_name, args[i*2+TO_SERVER].port);
      args[i*2+TO_PAIR].server = 1;
      args[i*2+TO_PAIR].port = _Parties[1]->port + i*2+TO_PAIR;
      params[i*2+TO_PAIR] = thread_new(comm_init_thread, &args[i*2+TO_PAIR]);
      printf("i=%d port %d\n", i*2+TO_PAIR, args[i*2+TO_PAIR].port);
    }
    if (num_parties >= 4) {
      for (int i=0; i<NC; i++) {
        args[i+TO_PARTY3].server = 0;
        args[i+TO_PARTY3].dest_name = _Parties[3]->addr;
        args[i+TO_PARTY3].port = _Parties[3]->port + i*2+_party;
        params[i+TO_PARTY3] = thread_new(comm_init_thread, &args[i+TO_PARTY3]);
        printf("i=%d server %s port %d\n", i, args[i+TO_PARTY3].dest_name, args[i+TO_PARTY3].port);
      }
    }
  }
  if (_party == 2) {
    for (int i=0; i<NC; i++) {
      args[i*2+TO_SERVER].server = 0;
      args[i*2+TO_SERVER].dest_name = _Parties[0]->addr;
      args[i*2+TO_SERVER].port = _Parties[0]->port + i*2 + _party;
      params[i*2+TO_SERVER] = thread_new(comm_init_thread, &args[i*2+TO_SERVER]);
      printf("i=%d server %s port %d\n", i*2+TO_SERVER, args[i*2+TO_SERVER].dest_name, args[i*2+TO_SERVER].port);
      args[i*2+TO_PAIR].server = 0;
      args[i*2+TO_PAIR].dest_name = _Parties[1]->addr;
      args[i*2+TO_PAIR].port = _Parties[1]->port + i*2+TO_PAIR;
      params[i*2+TO_PAIR] = thread_new(comm_init_thread, &args[i*2+TO_PAIR]);
      printf("i=%d server %s port %d\n", i*2+TO_PAIR, args[i*2+TO_PAIR].dest_name, args[i*2+TO_PAIR].port);
    }
    if (num_parties >= 4) {
      for (int i=0; i<NC; i++) {
        args[i+TO_PARTY3].server = 0;
        args[i+TO_PARTY3].dest_name = _Parties[3]->addr;
        args[i+TO_PARTY3].port = _Parties[3]->port + i*2+_party;
        params[i+TO_PARTY3] = thread_new(comm_init_thread, &args[i+TO_PARTY3]);
        printf("i=%d server %s port %d\n", i, args[i+TO_PARTY3].dest_name, args[i+TO_PARTY3].port);
      }
    }
  }
  if (_party == 3) {
    if (num_parties >= 4) {
      for (int i=0; i<NC; i++) {
        args[i*2+FROM_PARTY1].server = 1;
        args[i*2+FROM_PARTY1].port = _Parties[3]->port + i*2+FROM_PARTY1;
        params[i*2+FROM_PARTY1] = thread_new(comm_init_thread, &args[i*2+FROM_PARTY1]);
        printf("i=%d port %d\n", i*2+FROM_PARTY1, args[i*2+FROM_PARTY1].port);
        args[i*2+FROM_PARTY2].server = 1;
        args[i*2+FROM_PARTY2].port = _Parties[3]->port + i*2+FROM_PARTY2;
        params[i*2+FROM_PARTY2] = thread_new(comm_init_thread, &args[i*2+FROM_PARTY2]);
        printf("i=%d port %d\n", i*2+FROM_PARTY2, args[i*2+FROM_PARTY2].port);
      }
      args[FROM_PARTY3].server = 0;
      args[FROM_PARTY3].dest_name = _Parties[0]->addr;
      args[FROM_PARTY3].port = _Parties[0]->port + FROM_PARTY3;
      params[FROM_PARTY3] = thread_new(comm_init_thread, &args[FROM_PARTY3]);
      printf("i=%d server %s port %d\n", FROM_PARTY3, args[FROM_PARTY3].dest_name, args[FROM_PARTY3].port);
    }
  }

  if (_party == 0) {
    for (int i=1; i<NP; i++) {
      thread_end(params[i]);
      _C[i] = args[i].ans;
      _C[i]->total_send = 0;
      _C[i]->total_recv = 0;
    }
    if (num_parties >= 4) {
      thread_end(params[0]);
      _C[0] = args[0].ans;
      _C[0]->total_send = 0;
      _C[0]->total_recv = 0;
    }
  }

  if (_party == 1 || _party == 2) {
    for (int i=1; i<NP; i++) {
      thread_end(params[i]);
      _C[i] = args[i].ans;
      _C[i]->total_send = 0;
      _C[i]->total_recv = 0;
    }
    if (num_parties >= 4) {
      for (int i=NP; i<NP+NC; i++) {
        thread_end(params[i]);
        _C[i] = args[i].ans;
        _C[i]->total_send = 0;
        _C[i]->total_recv = 0;
      }
    }
  }
  if (_party == 3) {
    for (int i=0; i<NP; i++) {
      thread_end(params[i]);
      _C[i] = args[i].ans;
      _C[i]->total_send = 0;
      _C[i]->total_recv = 0;
    }
  }

  for (int i=0; i<NP+NC; i++) {
    NEWA(send_queue[i], char, BUFFER_SIZE);
  }
  //NEWA(send_queue_idx, int, NP);
  for (int i=0; i<NP+NC; i++) {
    send_queue_idx[i] = 0;
  }
}

#if 0
static void mpc_start_old(void)
{
// 乱数初期化
//  unsigned long init[4]={0x123, 0x234, 0x345, 0x456};
//  init_by_array(init, 4);

  if (_party < 0) return;
  _Parties = party_read(3);
  printf("party %d\n", _party);

  if (_party == 0) {
    _C[1] = comm_init_server(_Parties[0]->port + 1);
    _C[2] = comm_init_server(_Parties[0]->port + 2);
    for (int i=3; i<NP; i+=2) {
      _C[i  ] = comm_init_server(_Parties[0]->port + i  );
      _C[i+1] = comm_init_server(_Parties[0]->port + i+1);
    }
  }
  if (_party == 1) {
    _C[1] = comm_init_client(_Parties[0]->addr, _Parties[0]->port + _party); // to server
    _C[2] = comm_init_server(_Parties[1]->port + 2); // to pair
    for (int i=3; i<NP; i+=2) {
      _C[i  ] = comm_init_client(_Parties[0]->addr, _Parties[0]->port + _party + i-1); // to server
      _C[i+1] = comm_init_server(_Parties[1]->port + i+1); // to pair
    }
  }
  if (_party == 2) {
    _C[1] = comm_init_client(_Parties[0]->addr, _Parties[0]->port + _party); // to server
    _C[2] = comm_init_client(_Parties[1]->addr, _Parties[1]->port + _party); // to pair
   for (int i=3; i<NP; i+=2) {
     _C[i  ] = comm_init_client(_Parties[0]->addr, _Parties[0]->port + _party + i-1); // to server
     _C[i+1] = comm_init_client(_Parties[1]->addr, _Parties[1]->port + i+1); // to pair
   }
  }

  _C[1]->total_send = 0;
  _C[1]->total_recv = 0;
  _C[2]->total_send = 0;
  _C[2]->total_recv = 0;
  for (int i=3; i<NP; i++) {
    _C[i]->total_send = 0;
    _C[i]->total_recv = 0;
  }

  for (int i=0; i<NP; i++) {
    NEWA(send_queue[i], char, BUFFER_SIZE);
  }
  //NEWA(send_queue_idx, int, NP);
  for (int i=0; i<NP; i++) {
    send_queue_idx[i] = 0;
  }
}
#endif

static void mpc_end(void)
{
  precomp_tables_free(); 
  if (_party < 0) return;

  long total_send1 = 0, total_send2 = 0, total_send3 = 0;
  long total_recv1 = 0, total_recv2 = 0, total_recv3 = 0;

//  printf("total send %ld + %ld bytes\n", _C[1]->total_send, _C[2]->total_send);
//  printf("total recv %ld + %ld bytes\n", _C[1]->total_recv, _C[2]->total_recv);
  if (_party <= 2) {
    for (int i=1; i<NP; i+=2) {
      total_send1 += _C[i]->total_send;
      total_recv1 += _C[i]->total_recv;
      total_send2 += _C[i+1]->total_send;
      total_recv2 += _C[i+1]->total_recv;
    }
    for (int i=NP; i<NP+NC; i++) {
      if (_C[i] != NULL) {
        total_send3 += _C[i]->total_send;
        total_recv3 += _C[i]->total_recv;
      }
    }
  }

  if (_party == 3) {
    for (int i=1; i<NP; i+=2) {
      total_send1 += _C[i]->total_send;
      total_recv1 += _C[i]->total_recv;
      total_send2 += _C[i+1]->total_send;
      total_recv2 += _C[i+1]->total_recv;
      comm_close(_C[i]);
      comm_close(_C[i+1]);
    }
    comm_close(_C[0]);
  }

  printf("total send %ld + %ld + %ld bytes\n", total_send1, total_send2, total_send3);
  printf("total recv %ld + %ld + %ld bytes\n", total_recv1, total_recv2, total_recv3);

  if (_party <= 2) {
    for (int i=1; i<NP; i++) comm_close(_C[i]);
  }
  if (_party == 0) comm_close(_C[0]);
//  party_free(_Parties, 3);

  for (int i=0; i<NP; i++) {
//    free(send_queue[i]);
  }
}


static void mpc_send(int party_to, void *buf, int size)
{
  if (party_to >= NP+NC*2) {
    printf("mpc_send: party_to %d NP %d\n", party_to, NP);
    exit(1);
  }
  if (_party < 0) return;

//  if (send_queue_idx[party_to]>0) mpc_send_flush(party_to);

  comm c = _C[party_to];

  int s = 0;
  //printf("mpc_send %d bytes\n", size);
#if 0
  printf("mpc_send to party %d\n", party_to);
  for (int i=0; i<size; i++) printf("%02x ", ((unsigned char *)buf)[i]);
  printf("\n");
#endif
  while (s < size) {
    s += comm_send_block(c, buf+s, size-s);
  //  sleep(0.01);
  }
  c->total_send += size;
//  if (_party == 0) printf("total %ld        \r", c->total_send);
}

static void mpc_send_flush(int party_to)
{
  mpc_send(party_to, send_queue[party_to], send_queue_idx[party_to]);
  send_queue_idx[party_to] = 0;
}


static void mpc_send_queue(int party_to, void *buf, int size)
{
  if (send_queue_idx[party_to] + size > BUFFER_SIZE) {
    mpc_send_flush(party_to);
    mpc_send(party_to, buf, size);
    return;
  }
  int p = send_queue_idx[party_to];
  char *b = (char *)buf;
  for (int i=0; i<size; i++) {
    send_queue[party_to][p+i] = b[i];
  }
  send_queue_idx[party_to] += size;
}


static void mpc_recv(int party_from, void *buf, int size)
{
  if (party_from >= NP+NC*2) {
    printf("mpc_recv: party_from %d NP %d\n", party_from, NP);
    exit(1);
  }
  if (_party < 0) return;
  comm c = _C[party_from];
  int r = 0;
  while (r < size) {
    r += comm_recv_block(c, buf+r, size-r);
  //  sleep(0.01);
  }
#if 0
  printf("mpc_recv from party %d\n", party_from);
  for (int i=0; i<size; i++) printf("%02x ", ((unsigned char *)buf)[i]);
  printf("\n");
#endif
  c->total_recv += size;
}


static void mpc_exchange_channel(void *buf_send, void *buf_recv, int size, int channel)
{
  if (_party <= 0) return;
  comm c = _C[channel*2+TO_PAIR];
  int r = 0, s = 0;
  while (r < size || s < size) {
    if (r < size) r += comm_recv_block(c, buf_recv+r, size-r);
    if (s < size) s += comm_send_block(c, buf_send+s, size-s);
  //  sleep(0.01);
  }
  c->total_send += size;
  c->total_recv += size;
}

static void mpc_exchange(void *buf_send, void *buf_recv, int size)
{
  mpc_exchange_channel(buf_send, buf_recv, size, 0);
}





#undef NP


#endif
