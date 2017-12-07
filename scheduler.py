import requests
import cafeteria
from apscheduler.schedulers.blocking import BlockingScheduler

def postCafeteria():
  cafeteria.timeReset()
  result = cafeteria.day(cafeteria.currentDay)
  if(len(result) <= 20):
    pass
  else:
    result = "좋은 아침입니다 \n" + cafeteria.day(cafeteria.currentDay)
    r = requests.post("https://graph.facebook.com/v2.11/1529061383780127/feed",
      params={"access_token": "EAAHGoGpG0ZCMBAHbsZCP5ZBw89T3c8M2zJavUx0s8ZCbksx7pO0NA6P9nQ0XlWBTZAsKK7VfMhD3kg7NSSDJkYS0ZAssJsZB26UqnlwF27HRAQmffwXy1BOVTUQ5cN4BxvL1GNnSr3AOttCmnjbSVRzSSs6iBkgIN6uFLcCgklUpgZDZD"},
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
sched.add_job(postCafeteria, 'cron', hour=10)

sched.start()



  