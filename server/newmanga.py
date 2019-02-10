from flask import Flask, render_template, send_from_directory, g, request
from flask_sqlalchemy import SQLAlchemy
import math
import os
from .db import init_db, db, User, Book, UserBook, Setting, Log
from .fetchbooks import fetchBooksFomrUrl, updateBooks


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
init_db(app)

ADMIN_ROOT_PARH = os.environ['ADMIN_ROOT_PARH']


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


@app.route('/userbooks')
def userbooks():
    page = getPage()
    user = User.query.first()
    books = Book.query.join(UserBook).filter(UserBook.user_id==user.id)
    bookAllCount = books.count()
    bookCountPage = 50
    pageMax = math.ceil(bookAllCount / bookCountPage)
    if page > pageMax:
        page = pageMax


    books = books.order_by(Book.date.desc()).limit(bookCountPage).offset(bookCountPage * (page - 1)).all()
    return render_template('index.html',
        books=books,
        page=page,
        pageMax=pageMax)


@app.cli.command()
def fetchbooks():
    updateBookCount = updateBooks()
    Log.add('Fetch {} books.'.format(updateBookCount))


@app.route('/{}/'.format(ADMIN_ROOT_PARH))
@app.route('/{}/settings'.format(ADMIN_ROOT_PARH))
def adminSettings():
    return render_template('settings.html',
        adminRootPath=ADMIN_ROOT_PARH,
        setting=Setting.get(),
        bookCount=Book.query.count())


@app.route('/{}/createtable'.format(ADMIN_ROOT_PARH))
def adminCreatetable():
    db.create_all()
    return "create table"


@app.route('/{}/useradd'.format(ADMIN_ROOT_PARH))
def adminUseradd():
    user = User.query.first()
    if not user:
        user = User(
            name = 'akiraak',
            password = 'akiraak'
        )
        db.session.add(user)
        db.session.commit()
    return "fetchbooks"


@app.route('/{}/logtest'.format(ADMIN_ROOT_PARH))
def adminLogtest():
    Log.add("logtestlogtestlogtestlogtest")
    return "logtest"


@app.route('/{}/logs'.format(ADMIN_ROOT_PARH))
def adminLogs():
    page = getPage()
    logAllCount = Log.query.count()
    countPage = 200
    pageMax = math.ceil(logAllCount / countPage)
    if page > pageMax:
        page = pageMax
    logs = Log.query.order_by(Log.id.desc()).limit(countPage).offset(countPage * (page - 1)).all()
    return render_template('logs.html',
        adminRootPath=ADMIN_ROOT_PARH,
        logs=logs,
        page=page,
        pageMax=pageMax)


@app.route('/{}/fetchtest'.format(ADMIN_ROOT_PARH), methods=['GET', 'POST'])
def adminFetchtest():
    books = []
    if request.method == 'POST':
        url = request.form.get('url')
        print(url)
        books = fetchBooksFomrUrl(url)
        print(len(books))
    return render_template('admin_fetchtest.html',
        adminRootPath=ADMIN_ROOT_PARH,
        books=books)
