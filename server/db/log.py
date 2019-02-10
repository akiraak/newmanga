from datetime import datetime
from pytz import timezone, utc
from .db import db


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text(), nullable=False)
    createAt = db.Column(db.DateTime(), default=datetime.utcnow)

    def __repr__(self):
        return '<Log {}:{} {}>'.format(self.id, self.creatAt, self.text)

    @classmethod
    def add(cls, text):
        log = Log(text=text)
        db.session.add(log)
        db.session.commit()

    @property
    def createAtLocal(self):
        return self.createAt.replace(tzinfo=utc).astimezone(timezone('America/Los_Angeles'))
