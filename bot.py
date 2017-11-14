
from difflib import SequenceMatcher
import re
import cafeteria
import schedule



def messageMatching(message):
  message = message.replace('\n', '').replace(' ', '')
  if(textMatching(message, ["급식", "점심", "밥"], 0.3)):
    return cafeteriaMatching(message)
  elif(textMatching(message, ["일정", "스케줄"], 0.3)):
    return scheduleMatching(message)
  else:
    return message


def scheduleMatching(message):
  if(textMatching(message, ["다음달, 담달"], 0.3)):
    return schedule.monthSchedule(int(schedule.currentMonth) + 1)
  if(textMatching(message, ["이번달", "요번달"], 0.3)):
    return schedule.monthSchedule(schedule.currentMonth)
  elif(textMatching(message, ["달", "월"], 0.2)):
    month = re.sub('[^0-9]', '', message)
    if(int(month) >= 1 and int(month) <= 12):
      return schedule.monthSchedule(int(month))
    else:
      return "정확한 날짜를 입력해줘요"
  else:
    return schedule.monthSchedule(schedule.currentMonth)

def cafeteriaMatching(message):
  if(textMatching(message, ["내일", "낼"], 0.4)):
      return cafeteria.day(int(cafeteria.currentDay) + 1)
  elif(textMatching(message, ["이번주", "요번주"], 0.5)):
    return cafeteria.week(1)
  elif(textMatching(message, ["다음주", "담주"], 0.5)):
    return cafeteria.week(0)
  elif(textMatching(message, ["요일", "욜", "여일"], 0.2)):
    if(textMatching(message, ["월"], 0.1)):
      return cafeteria.dayofweek(1)
    elif(textMatching(message, ["화"], 0.1)):
      return cafeteria.dayofweek(2)
    elif(textMatching(message, ["수"], 0.1)):
      return cafeteria.dayofweek(3)
    elif(textMatching(message, ["목"], 0.1)):
      return cafeteria.dayofweek(4)
    elif(textMatching(message, ["금"], 0.1)):
      return cafeteria.dayofweek(5)
  elif(textMatching(message, ["일"], 0.2)):
    date = re.sub('[^0-9]', '', message)
    if(int(date) >= 1 and int(date) <= 31):
      return cafeteria.day(int(date))
    else:
      return "정확한 날짜를 입력해줘요"
  else:
    return cafeteria.day(cafeteria.currentDay)


def textMatching(message, matchText, ratio):
  for text in matchText:
    if(SequenceMatcher(None, text, message).ratio() > ratio):
      return True


### test

print(messageMatching("다음달일정"))