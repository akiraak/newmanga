from .db import db


class Setting(db.Model):
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True)
    fetchLastPage = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Setting id={} fetchLastPage={}>'.format(self.id, self.fetchLastPage)

    def __init__(self, **kwargs):
        super(Setting, self).__init__(**kwargs)
        self.fetchLastPage = 1

    @classmethod
    def get(cls):
        s = Setting.query.first()
        if not s:
            s = Setting()
            db.session.add(s)
            db.session.commit()
        return s