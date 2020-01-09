from rq import Queue
from worker import conn
from daily_report import get_daily_gain
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

q = Queue(connection=conn)


@sched.scheduled_job('cron', day_of_week='mon-fri', hour=23, minute=59)
def scheduled_job():
    print('Sending emails to all portfolio owners')
    get_daily_gain()


sched.start()
