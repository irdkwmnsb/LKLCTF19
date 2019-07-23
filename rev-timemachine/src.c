/*
* @Author: m4drat
* @Date:   2019-07-17 13:12:17
* compile: gcc -no-pie -masm=intel src.c -o time_machine
* flag: Th4t_w4s_3asy_d0esnt_1t
*/

#include <stdlib.h>
#include <string.h>
#include <stdio.h>

#define junk __asm__ \
( \
    "push rax; \
    mov rax, 0x0; \
    add rax, 0x1337; \
    push rdx; \
    mov rdx, 0x133; \
    xor rax, rdx; \
    cmp rax, 0x0; \
    jz 0x0; \
    pop rdx; \
    pop rax;" \
);

char *gen_flag(size_t passcode, int diff) // 1338, 32
{
    junk;
    int data[] = {345787, 338619, 321211, 337595, 343483, 337339, 321211, 336315, 343483, 319931, 340923, 336315, 334779, 343483, 341691, 320187, 341947, 336315, 339131, 337595, 343483, 320443, 337595};
    junk;
    char *flag = (char *)malloc(sizeof(data) / sizeof(data[0]));

    for (int i = 0; i < sizeof(data) / sizeof(data[0]); ++i)
    {
        flag[i] = (char)(((((data[i] + 13125) << diff) >> 12) - 12) ^ passcode); // 32, 1338
    }
    flag[sizeof(data) / sizeof(data[0])] = 0;

    return flag;
}

int check_time(size_t ct)
{
    junk;
    if (((((ct ^ 123) << 2) >> 1) << 5) == 7872)
    {
        junk;
        return 1;
    } 
    else {
        junk;
        return 0;
    }
}

int main(int argc, const char *argv[])
{
    junk;
    size_t pass = 0;
    int cnt = 0;

    junk;
    for (;;)
    {
        junk;
        printf("Do it!\n");
        if (check_time(time(NULL))) // 1338 times here
        {
            junk;
            pass++;
            junk;
        }
        else { // 4 times here
            junk;
            cnt++;
            junk;
            if (((((((((pass << 3) << 2) >> 1) << 7) ^ 832515) ^ 763) ^ 6125124) << 2) == 31474416 && ((((cnt << 7) ^ 3) >> 4) >> 1) == 16)
            {
                printf("[+] Your flag is: %s\n", gen_flag(pass, cnt));
                break;
            }
        }

        junk;
        usleep(10000);
    }

    return 0;
}