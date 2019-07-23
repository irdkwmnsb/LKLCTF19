#!/usr/bin/env python3
import sys


def main():
    if len(sys.argv) != 2:
        print('Usage: ./solve.py "<main_account>"')
        sys.exit(1)

    with open('transactions.txt') as f:
        f.readline()
        f.readline()
        mb = 0
        while True:
            s = f.readline().strip()
            if not s:
                break
            p1 = s[0:18]
            p2 = s[22:40]
            c = int(s[42:-1])
            if p1 == sys.argv[1]:
                mb -= c
            elif p2 == sys.argv[1]:
                mb += c
            assert mb >= 0
        print(f'LKLCTF{{{mb}}}')


if __name__ == '__main__':
    main()
