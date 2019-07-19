import contextlib
import sqlite3


db = sqlite3.connect('service.db')


def cursor():
    global db
    return contextlib.closing(db.cursor())
