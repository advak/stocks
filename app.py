import atexit
from flask_restful import Api
from resources.user import UserSignUp, UserSignIn
from resources.portfolio import Portfolio
from resources.stock import Stock
from app_init_file import app
from daily_report import get_daily_gain
from apscheduler.schedulers.background import BackgroundScheduler


api = Api(app)

scheduler = BackgroundScheduler()
scheduler.add_job(func=get_daily_gain, trigger="cron", hour=23, minute=59)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


api.add_resource(UserSignUp, '/sign_up')
api.add_resource(UserSignIn, '/sign_in')
api.add_resource(Portfolio, '/portfolio')
api.add_resource(Stock, '/stock')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True, use_reloader=False)
