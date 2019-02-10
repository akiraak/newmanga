from sqlalchemy.orm import relationship
from .db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String(40), nullable=False)
    userBooks = relationship("UserBook", back_populates="user")

    def __repr__(self):
        return '<User {}:{}>'.format(self.id, self.name)
