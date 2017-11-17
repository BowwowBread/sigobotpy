import requests
import cafeteria
from apscheduler.schedulers.blocking import BlockingScheduler

def postCafeteria():
  result = cafeteria.day(cafeteria.currentDay)

  r = requests.post("https://graph.facebook.com/v2.11/325920784549338/feed",
    params={"access_token": "EAAYi1m8AgjUBAP7O4UlHQ0oLo4ySlbJadak2lZCw3Bx5vmg2q6JAX4RFWE3FrguEQE3mMg9plZBjZBQ7PDnST4dnGFoS4UuonM3dZCrwblBlRfjTQHlOwLjhhFZAWYREuSGiACV9oSJkyIYzK7oM3uyyZBB1QGtV7gJRwjZA9XD3gZDZD"},
    data={
      "message" : result,
    }
  )
  if(r.status_code == "200"):
    print("success")
    print(r.text)  
  else:
    print(r.text)

  
sched = BlockingScheduler()
sched.add_job(postCafeteria, 'cron', id='run_every_10_hour', day_of_week='0-4', hour=10,)
sched.start()



  