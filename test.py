import cafeteria
import datetime
import bot
cafeteria.timeReset()
result = cafeteria.day(cafeteria.currentDay)
if(len(result) <= 20):
  pass
else:
  result = "좋은 아침입니다 \n" + cafeteria.day(cafeteria.currentDay)

print(result)