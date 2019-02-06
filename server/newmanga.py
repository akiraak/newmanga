from flask import Flask, render_template, send_from_directory, g, request
from flask_sqlalchemy import SQLAlchemy
import math
import os
from .db import init_db, db, Book, Setting
from .fetchbooks import fetchBooks


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////mnt/c/Users/akira/Programs/newmanga/var/db.sqlite'
init_db(app)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
        'favicon.ico', mimetype='image/vnd.microsoft.icon')


def getPage():
    n = request.args.get('p', '1')
    if n.isdigit():
            return int(n)
    return 1


@app.route('/')
def index():
    page = getPage()
    bookAllCount = Book.query.count()
    bookCountPage = 50
    pageMax = math.ceil(bookAllCount / bookCountPage)
    if page > pageMax:
        page = pageMax
    books = Book.query.order_by(Book.date.desc()).limit(bookCountPage).offset(bookCountPage * (page - 1)).all()
    return render_template('index.html',
        books=books,
        page=page,
        pageMax=pageMax)


@app.route('/createtable')
def createtable():
    db.create_all()
    return "create table"


@app.route('/book')
def book():
    #books = []#Book.loadBooks(get_db())
    return "Hello"


@app.route('/fetchbooks')
def fetchbooks():
    fetchBooks()
    return "fetchbooks"


@app.route('/settingtest')
def settingtest():
    s = Setting.get()
    s.fetchLastPage = 1
    db.session.commit()
    print(s.id, s.fetchLastPage)
    return "settingtest"


@app.route('/setting')
def setting():
    s = Setting.get()
    return """
id: {}<br>
fetchLastPage: {}<br>
""".format(s.id, s.fetchLastPage)
