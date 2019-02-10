import datetime
import lxml.html
import re
import requests
from sqlalchemy import or_
import time
from .db import db, Book, User, UserBook, Setting


def bookInfoFromHtml(tree):
    title, titleUrl = titleFromHtml(tree)
    image = imageFromHtml(tree)
    asin = asinFromUrl(titleUrl)
    date = dateFromHtml(tree)
    if title and titleUrl and date:
        books = booksFromHtml(tree)
        return title, titleUrl, image, asin, date, books
    return None, None, None, None, None, None


def titleFromHtml(tree):
    title = ''
    url = ''
    titles = tree.xpath(".//h2")
    if len(titles) > 0:
        titleTree = titles[0]
        title = titleTree.text
        link = titleTree.xpath("..")
        if len(link) > 0 and link[0].tag == 'a':
            url = link[0].attrib['href']
    return title, url


def imageFromHtml(tree):
    images = tree.xpath(".//img")
    if len(images) > 0:
        return images[0].attrib['src']
    return None


def asinFromUrl(url):
    asin = None
    r = re.search(r'/dp/(\w+)', url)
    if r:
        asin = r.group(1)
    return asin


def dateFromHtml(tree):
    text = tree.text_content()
    r = re.search(r'(\d{4})/(\d{1,2})/(\d{1,2})', text)
    if r:
        return datetime.date(int(r.group(1)), int(r.group(2)), int(r.group(3)))
    return None


def booksFromHtml(tree):
    books = []
    bookTypes = tree.xpath(".//h3")
    for bookType in bookTypes:
        book = {'tag': bookType.text, 'url': ''}
        link = bookType.xpath("..")
        if len(link) > 0 and link[0].tag == 'a':
            book['url'] = link[0].attrib['href']
            books.append(book)
    return books


def fetchBooksFomrUrl(url):
    books = []
    try:
        page = requests.get(url)
        tree = lxml.html.fromstring(page.content)
        domBooks = tree.xpath("//li[contains(@class, 's-result-item')]")
        for domBook in domBooks:
            title, titleUrl, image, asin, date, tags = bookInfoFromHtml(domBook)
            if not (title and titleUrl and image and asin and date):
                continue
            book = Book()
            book.asin = asin
            book.title = title
            book.url = titleUrl
            book.image = image
            book.date = date
            book.tag1 = tags[0]['tag'] if len(tags) > 0 else None
            book.tag1url = tags[0]['url'] if len(tags) > 0 else None
            book.tag2 = tags[1]['tag'] if len(tags) > 1 else None
            book.tag2url = tags[1]['url'] if len(tags) > 1 else None
            book.tag3 = tags[2]['tag'] if len(tags) > 2 else None
            book.tag3url = tags[2]['url'] if len(tags) > 2 else None
            book.tag4 = tags[3]['tag'] if len(tags) > 3 else None
            book.tag4url = tags[3]['url'] if len(tags) > 3 else None
            book.html = lxml.html.tostring(domBook)
            books.append(book)
    except:
        pass
    return books


def updateBooks():
    setting = Setting.get()
    updateBookCount = 0
    for (i, pageNo) in enumerate(range(setting.fetchLastPage, 200)):
        time.sleep(10)
        url = 'https://www.amazon.co.jp/gp/search/?rh=n%3A465392%2Cn%3A%21465610%2Cn%3A466280%2Cp_n_publication_date%3A2315442051%7C2285539051&page={}&bbn=466280&ie=UTF8&qid=1549690134'.format(pageNo)
        books = fetchBooksFomrUrl(url)
        print(i, pageNo, len(books))
        if len(books) == 0:
            if i == 0:
                setting.fetchLastPage = 1
            else:
                setting.fetchLastPage = pageNo
            db.session.commit()
            break
        for book in books:
            existBook = Book.query.filter_by(asin = book.asin).first()
            if existBook:
                existBook.title = book.title
                existBook.url = book.url
                existBook.image = book.image
                existBook.date = book.date
                existBook.tag1 = book.tag1
                existBook.tag1url = book.tag1url
                existBook.tag2 = book.tag2
                existBook.tag2url = book.tag2url
                existBook.tag3 = book.tag3
                existBook.tag3url = book.tag3url
                existBook.tag4 = book.tag4
                existBook.tag4url = book.tag4url
                existBook.html = book.html
            else:
                db.session.add(book)
            updateBookCount += 1
        db.session.commit()
    updateUserbook()
    return updateBookCount


keywords = [
    "HUNTER×HUNTER",
    "ヴィンランド・サガ",
    "落日のパトス",
    "狼と香辛料",
    "食戟のソーマ",
    "小説家になる方法",
    "重版出来",
    "山と食欲と私",
    "釣り船御前丸",
    "木根さんの1人でキネマ",
    "インベスターZ",
    "波よ聞いてくれ",
    "食戟のソーマ",
    "アルキメデスの大戦",
    "ふらいんぐうぃっち",
    "亜人",
    "宇宙兄弟",
    "BLUE GIANT",
    "ベイビーステップ",
    "ハイスコアガール",
    "蛇蔵",
    "僕らはみんな河合荘",
    "のの湯",
    "百姓貴族",
    "ドロヘドロ",
    "からかい上手の高木さん",
    "乙嫁語り",
    "ばらかもん",
    "君に届け",
    "のんのんびより",
    "海街diary",
    "後遺症ラジオ",
    "ワンパンマン",
    "いぶり暮らし",
    "ヒストリエ",
    "つれづれダイアリー",
    "ダンジョン飯",
    "メイドインアビス",
    "ドメスティックな彼女",
    "東京喰種",
    "進撃の巨人",
    "アオバ自転車店",
    "ちはやふる",
    "甘々と稲妻",
    "ろんぐらいだぁす",
    "はたらく細胞",
    "猫のお寺の知恩さん",
    "ウーパ",
    "ゆるキャン",
    "平方イコルスン",
    "山賊ダイアリー",
    "銀の匙",
    "味噌汁でカンパイ",
    "放課後さいころ倶楽部",
    "ふしぎの国のバード",
    "レイリ",
    "3月のライオン",
    "コウノドリ",
    "南鎌倉高校女子自転車部",
    "あげくの果てのカノン",
    "徒然チルドレン",
    "ぐらんぶる",
    "ドラゴン桜",
    "おひ釣りさま",
    "放課後ていぼう日誌",
    "MISS CAST",
    "MFゴースト",
    "首都高SPL",
    "あまんちゅ！",
    "ガタガール",
]


def updateUserbook():
    UserBook.query.delete()
    user = User.query.first()
    if user:
        books = Book.query.filter(or_(Book.title.like('%{}%'.format(k)) for k in keywords)).all()
        for book in books:
            userBook = UserBook(user_id=user.id, book_id=book.id)
            db.session.add(userBook)
            db.session.commit()
