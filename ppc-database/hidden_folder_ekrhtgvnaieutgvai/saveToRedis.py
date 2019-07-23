 #ha-ha-ah
import redis as redislib

r = redislib.Redis(host='localhost', port=6379, db=4)

with open('./raw_db.txt', 'r') as f:
    buf = f.read().split('\n')
    buf.pop()

    print('buf len:', len(buf))
    db = {}
    for i in buf:
        login, pwd = i.split(':')
        db[login] = pwd

    r.hmset('users', db)
