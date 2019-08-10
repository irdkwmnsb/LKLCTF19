import contextlib
import sqlite3

from loguru import logger


logger.info('Setting up database')
file_db = sqlite3.connect('file:service.db?mode=ro', uri=True)
db = sqlite3.connect(':memory:')
db.executescript(''.join((s for s in file_db.iterdump())))
file_db.close()
del file_db


def cursor():
    global db
    return contextlib.closing(db.cursor())
