import datetime
from db import db


class StockModel(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'))
    symbol = db.Column(db.String(10))
    price = db.Column(db.Float)
    buy = db.Column(db.Boolean)
    quantity = db.Column(db.Integer)
    date = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, portfolio_id, symbol, price, buy, quantity, date):
        self.portfolio_id = portfolio_id
        self.symbol = symbol
        self.price = price
        self.buy = buy
        self.quantity = quantity
        self.date = date

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

