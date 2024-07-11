import sqlite3
from flask import g

DATABASE = 'clothing_db.sqlite3'


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
