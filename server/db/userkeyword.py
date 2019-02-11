from sqlalchemy.orm import relationship
from .db import db


class UserKeyword(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.Text(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship("User", back_populates="userKeywords")

    def __repr__(self):
        return '<UserKeyword {}: {}>'.format(self.user_id, self.keyword)