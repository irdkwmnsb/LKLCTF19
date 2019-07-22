/*
* @Author: m4drat
* @Date:   2019-07-18 15:19:34
* compile: gcc -shared -fPIC -o libtime.so solve.c -ldl
*/

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

static int hm = 0;

time_t time(time_t *tloc)
{
    if (hm < 1338)
    {
        hm += 1;
        return 0;
    } else {
        return 124;
    }
}