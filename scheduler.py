import requests
import cafeteria

def testing1():
    print ("testing1 - every 5 sec...")
def testing2():
    print ("testing2 - kick off @ 19:00 hours...")

def postCafeteria():
  result = cafeteria.day(cafeteria.currentDay)
  print(result)
  r = requests.post("https://graph.facebook.com/v2.8/1529061383780127/feed",
    params={"access_token": "EAAYi1m8AgjUBAKyZCZACLdFXld4ni5BW81BWYebWN3DZAnjObvZCpZA3EmqOC4IbPLtv71lwj5Kfd1YU4mezgDirZAcmGBmCwVxOZAqjssJzRuUNmWJ7cY3qhsZBckpZC5QlwwLRLbstIZAZBuFwCAc8SCipNcjqqRuTn8MZCsYZBYaeUpAZDZD"},
    data=result,
    headers={'Content-type': 'application/json'})
  
if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(postCafeteria, 'cron', id='run_every_2_min', second='*/5')
    sched.add_job(testing2, 'cron', id='run_at_7_pm', hour='19')
sched.start()
