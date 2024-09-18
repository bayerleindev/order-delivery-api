import datetime
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
scheduler.start()


def schedule(action, minutes: int = 5, *args):
    run_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes)

    scheduler.add_job(
        action,
        "date",
        run_date=run_time,
        args=[*args],
    )
