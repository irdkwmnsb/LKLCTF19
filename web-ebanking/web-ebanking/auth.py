import database as db

import hashlib
import json
import os
import secrets
from collections import namedtuple

import pyotp
from loguru import logger


User = namedtuple('User', ['username', 'password_hash', 'two_factor_enabled'])


def generate_session_id():
    return secrets.token_hex()


def initialize_session_cache():
    raw_data = json.loads(os.getenv('SERVICE_SESSIONS', '{}'))
    data = {}
    for session_id, username in raw_data.items():
        data[session_id] = get_user_by_name(username)
    return data


def create_session(user):
    global session_cache
    session_id = generate_session_id()
    session_cache[session_id] = user
    return session_id


def maybe_get_user_by_session(session_id):
    global session_cache
    if session_id is None:
        return None
    return session_cache.get(session_id, None)


def delete_session_if_exists(session_id):
    global session_cache
    session_cache.pop(session_id, None)


def get_user_by_name(username):
    with db.cursor() as cur:
        cur.execute('SELECT username, password_hash, two_factor FROM users WHERE username = ?', [username])
        user_info = cur.fetchone()
    if user_info is None:
        raise Exception(f'User `{username}` not found in the database')
    return User(username=user_info[0], password_hash=user_info[1], two_factor_enabled=(user_info[2] is not None))


def maybe_get_user_by_full_creds(username, password_hash):
    if username is None:
        return None
    with db.cursor() as cur:
        cur.execute(
            (
                'SELECT username, password_hash, two_factor FROM users\n'
                'WHERE password_hash = ? AND username = "' + username + '"'
            ),
            [password_hash]
        )
        user_info = cur.fetchone()
    if user_info is None:
        return None
    return User(username=user_info[0], password_hash=user_info[1], two_factor_enabled=(user_info[2] is not None))


class TwoFactorRequired(Exception):
    pass


def maybe_authorize_user(username, password_hash, otp):
    if username is None:
        return None
    with db.cursor() as cur:
        cur.execute(
            (
                'SELECT username, password_hash, two_factor FROM users\n'
                'WHERE password_hash = ? AND username = ?'
            ),
            [password_hash, username]
        )
        user_info = cur.fetchone()
    if user_info is None:
        return None
    if user_info[2] is not None:
        valid_otp = pyotp.totp.TOTP(user_info[2])
        try:
            if not valid_otp.verify(otp, valid_window=5):
                return None
        except Exception as e:
            logger.error(repr(e))
            return None
    user = User(username=user_info[0], password_hash=user_info[1], two_factor_enabled=(user_info[2] is not None))
    return create_session(user)


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

session_cache = initialize_session_cache()
