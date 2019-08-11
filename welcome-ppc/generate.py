#!/usr/bin/env python3
import secrets
import random as rd

N = 10000       # num transactions
M = 20          # num accounts


def gen_account_number():
    s = str(rd.randint(0000_0000_0000_000, 9999_9999_9999_999)).zfill(15)
    return f'{s[0:4]} {s[4:8]} {s[8:12]} {s[12:15]}'


def main():
    accounts = [gen_account_number() for i in range(M)]
    main = accounts[0]
    mb = 0
    with open('transactions.txt', 'w') as f:
        print('# Формат:', file=f)
        print('# Счёт отправителя -> Счёт получателя (сумма)', file=f)
        for i in range(N):
            p1, p2 = rd.sample(accounts, k=2)
            c = rd.randint(100, 1000000)
            if p1 == main and mb < c:
                p1, p2 = p2, p1
            
            if p1 == main:
                mb -= c
            elif p2 == main:
                mb += c
            assert mb >= 0

            print('{} -> {} ({})'.format(p1, p2, c), file=f)
            if (i + 1) % 100 == 0:
                print('{} / {}'.format(i+1, N))
    print('Done')
    print('Main account: {}'.format(main))
    print('Answer: {}'.format(mb))

if __name__ == '__main__':
    main()
