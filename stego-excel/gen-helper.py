#!/usr/bin/env python3

import random as rd
import xlsxwriter as xl
from mimesis import Person


def replace(ls, x, seq):
    t = 0
    for i in ls:
        if i == x:
            yield seq[t]
            t += 1
        else:
            yield i


def get_bank_account_number():
    return ''.join(replace('xxxx xxxx xxxx xxxx', 'x', rd.choices('0123456789', k=16)))


def get_base():
    return rd.choice([
        'what you are reading isn\'t a flag',
        'this isn\'t a flag',
        'the flag isn\'t here',
        'no, it is not a flag',
        'it is *not* a flag',
        'no, no flag for you',
        'the flag has never existed here...',
        'do not even try to find a flag here!',
        'wrong way!',
        'this is exactly the place where there aren\'t any flags',
    ]).lower()

TABLE = {
    'e': list('3'),
    'i': list('1'),
    'o': list('0'),
    'a': list('4'),
    's': list('5'),
    'l': list('17'),
    'z': list('7'),
    'b': list('6'),
}

for c in 'qwertyuiopasdfghjklzxcvbnm':
    if c not in TABLE:
        TABLE[c] = []
    TABLE[c].append(c.upper())
    TABLE[c].append(c)


def sub(s):
    def helper():
        for c in s:
            if c not in TABLE:
                yield c
            else:
                yield rd.choice(TABLE[c])

    return ''.join(helper())


def gen_not_a_flag_message():
    base = get_base()
    return sub(base)


def get_transaction():
    p1 = Person()
    p2 = Person()
    a1 = get_bank_account_number()
    a2 = get_bank_account_number()
    money = round(rd.random() * 10_000_000) / 100
    return (p1.full_name(), a1, p2.full_name(), a2, money, f'LKLCTF{{{gen_not_a_flag_message()}}}')


def get_transactions():
    return (
        get_transaction()
        for i in range(5000)
    )


def main():
    with xl.Workbook('Transactions-info.xlsx') as wb:
        ws = wb.add_worksheet()
        bold = wb.add_format({'bold': True})
        #left = wb.add_format({'align': 'left'})
        #center = wb.add_format({'align': 'center'})
        #right = wb.add_format({'align': 'right'})

        transactions = get_transactions()
        for i, row in enumerate(transactions):
            if i % 100 == 0:
                print(f'{i}/5000')
            for j, item in enumerate(row):
                ws.write(i+1, j, item)
        ws.write(0, 0, 'Sent by', bold)
        ws.write(0, 1, 'Sent by (Bank account id)', bold)
        ws.write(0, 2, 'Received by', bold)
        ws.write(0, 3, 'Received by (Bank account id)', bold)
        ws.write(0, 4, 'Amount', bold)
        ws.write(0, 5, 'Comment', bold)

        for _ in range(1000):
            if _ % 100 == 0:
                print(f'{_}/1000')
            col = rd.randint(100, 999)
            row = rd.randint(100, 99999)
            ws.write(row, col, f'LKLCTF{{{gen_not_a_flag_message()}}}')
        ws.set_column(5, 5, width=60)
        ws.set_column(0, 4, width=25)


if __name__ == '__main__':
    main()
