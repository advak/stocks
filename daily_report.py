from models.stock import StockModel
from models.portfolio import PortfolioModel
from app_init_file import app
from db import db
import requests


def fill_stock_yesterday_and_today():
    with app.app_context():
        if not db.engine.dialect.has_table(db.engine.connect(), "stocks"):
            return
        all_stocks = StockModel.get_all_stocks()
        for stock in all_stocks:
            yesterday, today = get_stocks_info(stock.symbol)
            stock.previous_close = yesterday
            stock.current_close = today
            stock.save_to_db()


def get_stocks_info(symbol=None):
    # api-endpoint
    url = "https://www.alphavantage.co/query"

    # defining a params dict for the parameters to be sent to the API
    params = {'function': "TIME_SERIES_DAILY", 'symbol': symbol, 'apikey': "TKQ09SLGB2F86QGB" }

    # sending get request and saving the response as response object
    r = requests.get(url=url, params=params)

    # extracting data in json format
    data = r.json()
    time_series_daily = data["Time Series (Daily)"]
    sorted_dates = sorted(time_series_daily.keys())
    today = str(sorted_dates[-1])
    yesterday = str(sorted_dates[-2])
    return float(time_series_daily[yesterday]["4. close"]), float(time_series_daily[today]["4. close"])
