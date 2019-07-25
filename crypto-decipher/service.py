#ohoho

import json
import socket
import random
import string
from base64 import b64encode
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
from datetime import datetime
from time import sleep

HOST = '0.0.0.0'
PORT = 44500

CLIENTS_LIMIT = 500
BROADCAST_INTERVAL = 300 # should be >=60
CONN_TIMEOUT = BROADCAST_INTERVAL * 2 + 30
BROADCAST_PACKETS_COUNT = 25
TICK = 0.01

# enable if flag shouldn't be a plaintext or base64 encoded
# however, it won't be encrypted if an error occurred
FLAG_IS_ALWAYS_ENCRYPTED = True

CLIENTS_LIMIT_REACHED = 'max_clients reached, wait some time and try again'
TIMEOUT_REACHED = 'timeout reached, disconnected'

HELLO_MSG1 = 'MyLittleHack software v0.9 connected'
HELLO_MSG2 = '%d seconds before the next transaction starts'


last_broadcast = 0
methods = ['plain', 'aes', 'base64', 'rsa']
clients = []

fake_flags = [
    'LKLСTF{th15_15_n0t_th3_c0rr3ct_fl49}', # russian С in LKLСTF
    'LKLСTF{th15_15_n0t_th3_c0rr3ct_fl49_t00}', # russian С in LKLСTF
    'no flag there',
    'see next transaction',
    'no more there',
    'do you see anything?',
    'emptiness',
    'you have skipped the flag!',
    'this is a joke',
    "the flag doesn't exist!",
    'flag is a lie',
    'Designed by LKL-Bank',
    'LKL-Bank auth system v3453455134',
    'i hate my job',
    'i love my job',
    "Let's meet tomorrow, baby?",
    'thanks for meow-meow',
    'PING',
    'PONG',
    "Oh, it's saturday night",
    'Never gonna give you up',
    'Never gonna let you down',
    'flag is here! https://vk.cc/9CQ7g0',
    'Lorem ipsum dolor sit amet',
    '<script>alert("xss")</script>',
    "aliens, evacuate!",
    'i have seen HL3 yesterday',
    'i hope it will be easy to solve this task!',
    'Also try Terraria!',
    'here we go again'
]

correct_flag = 'LKLCTF{y0ur_m1tm_5ucc355}'

def notify(conn, s):
    try:
        conn.send((s + '\n').encode('utf-8'))
    except:
        pass


def notifyAndKill(conn, s):
    try:
        notify(conn, s)
        conn.close()
    except:
        try:
            conn.close()
        except:
            pass


def getDate():
    return "[" + datetime.now().strftime('%H:%M:%S %d.%m.%Y') + "]"


def timeUntilTransaction():
    return BROADCAST_INTERVAL - (now() % BROADCAST_INTERVAL)


def _print(t):
    print(getDate(), t)


def clientsCount():
    _print('connections: %d' % len(clients)) # load status


def now():
    return int(datetime.now().timestamp())


def sendto(conn, obj): # it throws exception
    s = json.dumps(obj) if type(obj) != 'str' else obj
    conn.send((s + '\n').encode('utf-8'))


def accept_conn():
    global clients

    try:
        conn, addr = s.accept()
        conn.setsockopt(socket.SOL_TCP, socket.TCP_NODELAY, 1)
        conn.setblocking(0)

        if len(clients) >= CLIENTS_LIMIT:
            notifyAndKill(conn, CLIENTS_LIMIT_REACHED)
        else:
            try:
                sendto(conn, HELLO_MSG1)
                sendto(conn, HELLO_MSG2 % timeUntilTransaction())
                clients.append((conn, now() + CONN_TIMEOUT))
                clientsCount()
            except:
                pass
    except:
        pass


def invalidator():
    global clients

    has_timeouted = False

    while len(clients) > 0 and clients[0][1] < now():
        notifyAndKill(clients[0][0], TIMEOUT_REACHED)
        has_timeouted = True
        clients.pop(0)

    if has_timeouted:
        clientsCount()


def generate_table():
    table = []

    for i in range(BROADCAST_PACKETS_COUNT - 1):
        table.append(create_fake())

    table.append(create_true())
    random.shuffle(table)
    return table


def create_aes_container(obj):
    j = json.dumps(obj).encode('utf-8')
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    try:
        cipher = AES.new(key, AES.MODE_CBC, iv)
        data = pad(j, cipher.block_size)
        encrypted = cipher.encrypt(data)

    except Exception as e:
        print('create_aes_container:', e)
        return create_plain_container(obj)

    return {
        'method': 'AES_CBC',
        'key': b64encode(key).decode('utf-8'),
        'iv': b64encode(iv).decode('utf-8'),
        'data': b64encode(encrypted).decode('utf-8'),
        #'debug': obj
    }


def create_rsa_container(obj):
    j = json.dumps(obj).encode('utf-8')
    pair = RSA.generate(2048)
    private_key = pair.export_key()

    try:
        cipher = PKCS1_OAEP.new(pair.publickey())
        encrypted = cipher.encrypt(j)

    except Exception as e:
        print('create_rsa_container:', e)
        return create_plain_container(obj)

    return {
        'method': 'RSA_PKCS1_OAEP_2048',
        'key': private_key.decode('utf-8'),
        'data': b64encode(encrypted).decode('utf-8'),
        #'debug': obj
    }


def create_b64_container(obj):
    j = json.dumps(obj).encode('utf-8')

    return {
        'method': 'b64',
        'data': b64encode(j).decode('utf-8'),
        #'debug': obj
    }


def create_plain_container(obj):
    return {
        'method': 'plain',
        'data': obj
    }


def create_container(obj, enc = False):
    method = random.choice(methods)

    while enc and (method == 'plain' or method == 'base64'):
        method = random.choice(methods)

    if method == 'aes':
        return create_aes_container(obj)
    elif method == 'rsa':
        return create_rsa_container(obj)
    elif method == 'base64':
        return create_b64_container(obj)
    else:
        return create_plain_container(obj)


def gen_address():
    s = ''
    for i in range(9):
        s += random.choice(string.digits)
    return int(s)


def create_generic_obj(flag):
    return {
        'value': random.randint(1, 1000000),
        'to': gen_address(),
        'date': now() - random.randint(0, BROADCAST_INTERVAL),
        'expiresAt': now() + random.randint(300, 567209),
        'extra': flag
    }


def create_fake():
    obj = create_generic_obj(random.choice(fake_flags))
    return create_container(obj)


def create_true():
    obj = create_generic_obj(correct_flag)
    return create_container(obj, FLAG_IS_ALWAYS_ENCRYPTED)


def broadcast():
    global last_broadcast, clients

    if now() < last_broadcast + BROADCAST_INTERVAL:
        return

    last_broadcast = now()
    c2 = clients[:]

    if len(c2) == 0:
        _print('no clients, aborted')
        sync_time()
        return

    _print('table generating...')

    table = generate_table()
    broken = 0

    _print('done!')

    for i in table:
        for j in range(len(c2)):
            if c2[j][1] == -1:
                continue

            try:
                sendto(c2[j][0], i)
            except:
                try:
                    c2[j][1].close() # kill broken socket
                except:
                    pass
                c2[j] = (None, -1)
                clients.pop(j - broken)
                broken += 1

    if len(clients) > 0:
        _print('sent')

    if broken > 0:
        clientsCount()

    sync_time()


def sync_time():
    global last_broadcast
    last_broadcast -= last_broadcast % BROADCAST_INTERVAL


def cycle():
    accept_conn()
    invalidator()
    broadcast()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(CLIENTS_LIMIT)
s.setblocking(0)

# sync time

last_broadcast = now()
sync_time()

try:
    while True:
        cycle()
        sleep(TICK)

except KeyboardInterrupt:
    _print('finished')

except Exception as e:
    _print('caught an exception', e)

s.close()