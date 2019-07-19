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
            )
        )
        db.commit()
