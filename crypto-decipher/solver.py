#ohaohaoha

import json
import socket
from base64 import b64decode
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import unpad
from time import sleep

HOST = '0.0.0.0'
PORT = 50013

TICK = 0.1
c = ''

def rsa(q):
    #print(q)

    try:
        key = RSA.importKey(q['key'])
        cipher = PKCS1_OAEP.new(key)
        s = cipher.decrypt(b64decode(q['data']))
        print(json.loads(s)['extra'])

    except Exception as e:
        print('RSA_PKCS1_OAEP_2048 error', e)


def aes(q):
    #print(q)

    try:
        key = b64decode(q['key'])
        iv = b64decode(q['iv'])
        cipher = AES.new(key, AES.MODE_CBC, iv)
        s = unpad(cipher.decrypt(b64decode(q['data'])), cipher.block_size)
        s = s.decode('utf-8').strip()
        print(json.loads(s)['extra'])

    except Exception as e:
        print('AES_CBC error', e)


def b64(q):
    #print(q)

    try:
        data = b64decode(q['data'])
        print(json.loads(data)['extra'])

    except Exception as e:
        print('b64 error', e)


def plain(q):
    #print(q)

    try:
        print(q['data']['extra'])

    except Exception as e:
        print('plain', e)


def decipher(j):
    try:
        q = json.loads(j)
        m = q['method']
    except:
        print('invalid json:', j)
        return

    if m == 'RSA_PKCS1_OAEP_2048':
        rsa(q)
    elif m == 'AES_CBC':
        aes(q)
    elif m == 'b64':
        b64(q)
    elif m == 'plain':
        plain(q)
    else:
        print('unsupported method')


def work():
    global c
    i = c.find('\n')

    if i == -1:
        try:
            c += s.recv(1024).decode('utf-8')
        except:
            pass # no data yet
    else:
        nextQuery = ''

        if i != len(c) - 1:
            nextQuery = c[i + 1:]

        decipher(c[0:i])
        c = nextQuery

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
s.connect((HOST, PORT))
s.setblocking(0)

try:
    while True:
        work()
        sleep(TICK)

except KeyboardInterrupt:
    print('finished')

except Exception as e:
    print('error:', e)

s.close()