#include <cstdio>
#include "int2048.h"
#include "key.h"

using namespace std;

typedef bigint<128> int2048;

void load_number(int2048& num, unsigned char* buf)
{
    num = 0;
    for(int i = 0; i < 64; i++)
        num.data[63 - i] = (((unsigned short)buf[2*i])<<8)|buf[2*i+1];
}

void store_number(int2048& num, unsigned char* buf)
{
    for(int i = 0; i < 64; i++)
    {
        buf[2 * i] = num.data[63 - i] >> 8;
        buf[2 * i + 1] = num.data[63 - i];
    }
}

int2048 fastpow(const int2048& a, int b, const int2048& mod)
{
    if(b == 0)
        return 1;
    else if(b % 2 == 0)
        return fastpow((a * a) % mod, b / 2, mod);
    else
        return (fastpow(a, b - 1, mod) * a) % mod;
}

int main()
{
    asm volatile(".byte 0xeb, 0xfe");
    int2048 n, flag;
    load_number(n, (unsigned char*)N);
    load_number(flag, (unsigned char*)FLAG);
    flag = fastpow(flag, D, n);
    char ans[129];
    store_number(flag, (unsigned char*)ans);
    ans[128] = 0;
    char* p = ans;
    while(!*p)
        p++;
    puts(p);
    return 0;
}
