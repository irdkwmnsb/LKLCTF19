#!/usr/bin/env python3

import contextlib
import hashlib
import os
import secrets
import sqlite3


QUERY = '''
BEGIN;
CREATE TABLE users (
    username        VARCHAR,
    password_hash   VARCHAR
);

INSERT INTO users VALUES
    ("user1", "{user1_passhash}"),
    ("admin", "{admin_passhash}"),
    ("smart_bot", "{smart_bot_passhash}");


CREATE TABLE transactions (
    user            VARCHAR,
    sender          VARCHAR,
    amount          REAL,
    comment         VARCHAR
);

INSERT INTO transactions VALUES
    ("user1", "9371 5018 5919 142", 3000.0, "Зарплата за полгода работы с нами"),
    ("user1", "1111 1111 1111 111", 12.34, "Тестовый перевод"),
    ("admin", "4914 1948 1844 743", 200.0, "Пожертвование на развитие сайта"),
    ("admin", "1039 1854 0149 291", 13.37, "{flag}"),
    ("smart_bot", "1111 1111 1111 111", 0.0, "На случай, если забуду пароль: {admin_pass}. admin.");

COMMIT;
'''

user1_pass = b'simplicity'
admin_pass = secrets.token_hex(16).encode()
smart_bot_pass = secrets.token_hex(16).encode()

user1_passhash = hashlib.sha256(user1_pass).hexdigest()
admin_passhash = hashlib.sha256(admin_pass).hexdigest()
smart_bot_passhash = hashlib.sha256(smart_bot_pass).hexdigest()

try:
    os.remove('service.db')
except FileNotFoundError:
    pass

with contextlib.closing(sqlite3.connect('service.db')) as db:
    with contextlib.closing(db.cursor()) as cur:
        cur.executescript(
            QUERY.format(
                user1_passhash = user1_passhash,
                admin_passhash = admin_passhash,
                smart_bot_passhash = smart_bot_passhash,
                flag = 'LKLCTF{mock_flag}',
                admin_pass = admin_pass,
            )
        )
        db.commit()
