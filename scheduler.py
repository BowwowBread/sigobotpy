from apscheduler.schedulers.blocking import BlockingScheduler

import pytz

sched = BlockingScheduler()
timezone = pytz.timezone('Asia/Seoul')

@sched.scheduled_job('cron', day_of_week='mon-fri', minute=41)
def main():
  print("hi")

sched.start()
print("aa")