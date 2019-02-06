"""
import sqlite3
from flask import g


DATABASE = '/mnt/c/Users/akira/Programs/newmanga/var/db.sqlite'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def close_db():
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
"""

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

def createTable(db):
    c = db.cursor()
    c.execute("DROP TABLE books")
    rows = c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='books'")
    if not rows.fetchone():
        c.execute('''
            CREATE TABLE IF NOT EXISTS books
            (
                id INTEGER PRIMARY KEY,
                asin TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                url TEXT NOT NULL,
                image TEXT NOT NULL,
                date TEXT NOT NULL,
                tag1 TEXT,
                tag1url TEXT,
                tag2 TEXT,
                tag2url TEXT,
                tag3 TEXT,
                tag3url TEXT,
                tag4 TEXT,
                tag4url TEXT,
                html TEXT
            )
        ''')
        db.commit()
    else:
        print('Not create books table. Exist books table.')
        #c.execute("DROP TABLE books")
