def testing1():
    print ("testing1 - every 5 sec...")
def testing2():
    print ("testing2 - kick off @ 19:00 hours...")
if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(testing1, 'cron', id='run_every_2_min', second='*/5')
    sched.add_job(testing2, 'cron', id='run_at_7_pm', hour='19')
sched.start()