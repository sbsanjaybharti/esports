from .. import db, flask_bcrypt
import uuid
import datetime


class Tournament(db.Model):
    __tablename__ = 'tournament'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), index=True)

    def save(self):
        db.session.add(self)
        db.session.commit()
