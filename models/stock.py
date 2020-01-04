import datetime
from db import db


class StockModel(db.Model):
    __tablename__ = 'stocks'
    id = db.Column(db.Integer, primary_key=True)
    portfolio_id = db.Column(db.Integer, db.ForeignKey('portfolios.id'))
    symbol = db.Column(db.String(10))
    purchase_price = db.Column(db.Float)
    buy = db.Column(db.Boolean)
    quantity = db.Column(db.Integer)
    date = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    current_close = db.Column(db.Float)
    previous_close = db.Column(db.Float)

    def __init__(self, portfolio_id, symbol, purchase_price, buy, quantity, date):
        self.portfolio_id = portfolio_id
        self.symbol = symbol
        self.purchase_price = purchase_price
        self.buy = buy
        self.quantity = quantity
        self.date = date

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_all_stocks(cls):
        return cls.query.all()

