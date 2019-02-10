from sqlalchemy.orm import relationship
from .db import db


class UserBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
    user = relationship("User", back_populates="userBooks")
    book = relationship("Book", back_populates="userBooks")

    def __repr__(self):
        return '<UserBook {}: {}>'.format(self.user_id, self.book_id)