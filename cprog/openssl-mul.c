#include <openssl/bn.h>
#include <stdio.h>
#include <string.h>
#include "common.h"

#define N 8000000
#define M 1600
int main(int argc, char **argv)
{
    int i;

    BN_CTX *ctx = BN_CTX_new();
    BN_MONT_CTX *mont = BN_MONT_CTX_new();
    BIGNUM *res = BN_a2bn( rand2_2048);
    BIGNUM *r = BN_a2bn( rand2_2048);
    BIGNUM *m = BN_a2bn( rand_2048);
    BIGNUM *arg = BN_a2bn( argv[1]);

    BN_MONT_CTX_set(mont, m, ctx);

    //Dummyoperationen
    for ( i=0; i < N; i++) i ^= 0;

    //res = res * arg
    for (i = 0; i < M; i++) BN_mod_mul(res, res, arg, m, ctx);
    //for (i = 0; i < M; i++) BN_mod_mul_montgomery(res, res, arg, mont, ctx);

    //Dummyoperationen
    for ( i=0; i < N; i++) i ^= 0;
}
