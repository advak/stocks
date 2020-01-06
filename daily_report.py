from models.stock import StockModel
from models.portfolio import PortfolioModel
from models.user import UserModel
from app_init_file import app
from db import db
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def fill_stock_yesterday_and_today():
    with app.app_context():
        if not db.engine.dialect.has_table(db.engine.connect(), "stocks"):
            return False
        all_stocks = StockModel.get_all_stocks()
        for stock in all_stocks:
            yesterday, today = get_stocks_info(stock.symbol)
            stock.previous_close = yesterday
            stock.current_close = today
            stock.save_to_db()
    return True


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


def get_daily_gain():
    fill_stock = fill_stock_yesterday_and_today()
    if not fill_stock:
        return
    gain_per_portfolio = dict()
    with app.app_context():
        all_stocks = StockModel.get_all_stocks()
        for stock in all_stocks:
            portfolio_id = stock.portfolio_id
            portfolio = PortfolioModel.find_by_portfolio_id(portfolio_id)
            user_id = portfolio.user_id
            user = UserModel.find_by_id(user_id)
            email = user.email
            if portfolio_id not in gain_per_portfolio:
                gain_per_portfolio[portfolio_id] = dict()
                gain_per_portfolio[portfolio_id]["email"] = email
                gain_per_portfolio[portfolio_id]["total_daily_gain"] = 0
            current_gain = (stock.current_close - stock.previous_close) * stock.quantity
            gain_per_portfolio[portfolio_id]["total_daily_gain"] += current_gain
    for portfolio_id in gain_per_portfolio:
        send_email(gain_per_portfolio[portfolio_id]["email"],
                   gain_per_portfolio[portfolio_id]["total_daily_gain"],
                   portfolio_id)


def send_email(send_to_email, total_gain, portfolio_id):
    email = 'great.stocker.app@gmail.com'
    password = 'greatstocks100'
    send_to_email = send_to_email
    subject = 'Your daily report from Stocker'
    message = 'Your total gain in portfolio {} for today is {} USD'.format(portfolio_id, total_gain)

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = send_to_email
    msg['Subject'] = subject

    # Attach the message to the MIMEMultipart object
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
    server.sendmail(email, send_to_email, text)
    server.quit()
