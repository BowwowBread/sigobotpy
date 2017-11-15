import requests
import cafeteria

def postCafeteria():
  result = cafeteria.day(cafeteria.currentDay)

  r = requests.post("https://graph.facebook.com/v2.11/325920784549338/feed",
    params={"access_token": "EAAYi1m8AgjUBAMcHHghuZADWw3AGoAms52PK7NXugmON4BOGeNrNRexBZBfH5qcRCWT5dLL6tlv3xDX89oWYXg6LJkfgc3SQ1sGra42ZBcgyGsHIsyCRbM9jJovEf5SHZCPZAQFTcGhUfvDZBFFdx4kP0ZCFOvhLAggFi7x0H7p7CKyFx1ctzzAtALknQg1cbEOkueIFx2CBAZDZD"},
    data={
      "message" : result,
    }
  )
  if(r.status_code == "200"):
    print("success")
    print(r.text)  
  else:
    print(r.text)

  
if __name__ == '__main__':
    from apscheduler.schedulers.blocking import BlockingScheduler
    sched = BlockingScheduler()
    sched.add_job(postCafeteria, 'cron', id='run_every_10_hour', day_of_week='0-4', hour=16,)
sched.start()



  