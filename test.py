import lxml.html
import re
import requests
import sqlite3
from server.db.db import createTable
from server.db import Book
DATABASE = '/mnt/c/Users/akira/Programs/newmanga/var/db.sqlite'
db = sqlite3.connect(DATABASE)
Book.createTable(db, True)


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
    #print(tree.text_content())
    text = tree.text_content()
    r = re.search(r'\d{4}/\d{1,2}/\d{1,2}', text)
    if r:
        return r.group(0)
    return None



def booksFromHtml(tree):
    books = []
    bookTypes = tree.xpath(".//h3")
    for bookType in bookTypes:
        book = {'tag': bookType.text, 'url': ''}
        #print(bookType.text)
        link = bookType.xpath("..")
        if len(link) > 0 and link[0].tag == 'a':
            book['url'] = link[0].attrib['href']
            #print(link[0].attrib['href'])
            books.append(book)
    return books


def testdb():
    db = sqlite3.connect(DATABASE)
    c = db.cursor()
    createTable(db)
    #params = ("aaaa", "ttttt", "uuuuuuu", "dd", "hhhhhhh")
    #c.execute('''
    #    INSERT INTO books (asin, title, url, date, html)
    #        VALUES (?, ?, ?, ?, ?)
    #''', params)
    db.commit()
    db.close()


def saveBook(title, titleUrl, image, asin, date, books, html):
    c = db.cursor()
    params = (
        asin,
        title,
        titleUrl,
        image,
        date,
        books[0]['tag'] if len(books) > 0 else None,
        books[0]['url'] if len(books) > 0 else None,
        books[1]['tag'] if len(books) > 1 else None,
        books[1]['url'] if len(books) > 1 else None,
        books[2]['tag'] if len(books) > 2 else None,
        books[2]['url'] if len(books) > 2 else None,
        books[3]['tag'] if len(books) > 3 else None,
        books[3]['url'] if len(books) > 3 else None,
        html)
    c.execute('''
        INSERT INTO books (
            asin,
            title,
            url,
            image,
            date,
            tag1,
            tag1url,
            tag2,
            tag2url,
            tag3,
            tag3url,
            tag4,
            tag4url,
            html)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', params)
    db.commit()


def testhtml():
    url = 'https://www.amazon.co.jp/s/ref=sr_nr_p_n_publication_date_3?fst=as%3Aoff&rh=n%3A465392%2Cn%3A%21465610%2Cn%3A466280%2Cn%3A2278488051%2Cp_n_publication_date%3A2315442051%7C2285539051&bbn=2278488051&ie=UTF8&qid=1495328200&page=1'
    page = requests.get(url)
    tree = lxml.html.fromstring(page.content)
    books = tree.xpath("//li[contains(@class, 's-result-item')]")
    for book in books:
        title, titleUrl, image, asin, date, books = bookInfoFromHtml(book)
        if asin:
            html = lxml.html.tostring(book)
            saveBook(title, titleUrl, image, asin, date, books, html)


def main():
    testhtml()
    #testdb()
    #book = Book.oneFromAsin(db, '4065138663')
    #print(book.title)
    db.close()


if __name__ == '__main__':
    main()