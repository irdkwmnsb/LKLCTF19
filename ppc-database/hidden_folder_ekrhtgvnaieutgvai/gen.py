#ha-ha-ha
import requests
import random
import string
import time
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
table = []

raw_headers = \
'''Host: 104.236.237.27
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/60.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3
Accept-Encoding: gzip, deflate, br
X-Requested-With: XMLHttpRequest
DNT: 1
Connection: keep-alive'''.split('\n')

headers = {}

for i in raw_headers:
    j = i.split(': ')
    headers[j[0]] = j[1]


pass_len_min = 4
pass_len_max = 16
count = 10000

pass_alphabet = string.ascii_lowercase

def pass_gen():
    length = random.randint(pass_len_min, pass_len_max)
    res = []

    for i in range(length):
        res.append(random.choice(pass_alphabet))

    return ''.join(res)


def verify_login(login):
    for i in login:
        if i not in login_alphabet:
            return False
    return True


def generate():
    response = requests.post('https://104.236.237.27/generator-nikov-online/generate.php', verify=False, data={}, headers=headers)

    if response.status_code != requests.codes.ok:
        print('error code:', response.status_code)
        sys.exit(1)

    login = response.json()['va'].replace('?', 'e')
    password = pass_gen()

    print('status:', len(table) + 1, 'of', count)
    table.append((login, password))
    print(login)


#random.seed(time.time())
#random.shuffle(login_alphabet)
#random.shuffle(pass_alphabet)

for i in range(count - 1):
    generate()


random.shuffle(table)
print('should be saved...')

with open('./raw_db1.txt', 'w') as f:
    for i in table:
        f.write(i[0] + ":" + i[1] + "\n")
