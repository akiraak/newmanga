from sqlalchemy.orm import relationship
from .db import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asin = db.Column(db.String(40), unique=True, nullable=False)
    title = db.Column(db.Text(), nullable=False)
    url = db.Column(db.Text(), nullable=False)
    image = db.Column(db.Text(), nullable=False)
    date = db.Column(db.Date, index=True, nullable=False)
    tag1 = db.Column(db.Text(), nullable=True)
    tag1url = db.Column(db.Text(), nullable=True)
    tag2 = db.Column(db.Text(), nullable=True)
    tag2url = db.Column(db.Text(), nullable=True)
    tag3 = db.Column(db.Text(), nullable=True)
    tag3url = db.Column(db.Text(), nullable=True)
    tag4 = db.Column(db.Text(), nullable=True)
    tag4url = db.Column(db.Text(), nullable=True)
    html = db.Column(db.Text(), nullable=True)
    userBooks = relationship("UserBook", back_populates="book")

    def __repr__(self):
        return '<Book {}:{}>'.format(self.asin, self.title)

    """
    def __init__(**kwargs):
        super(Book, self).__init__(**kwargs)
    """