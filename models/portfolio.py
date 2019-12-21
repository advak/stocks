import datetime
from db import db


class PortfolioModel(db.Model):
    __tablename__ = 'portfolios'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, portfolio_name, owner):
        self.owner = owner
        self.name = portfolio_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, email):
        return cls.query.filter_by(email=email).first()
