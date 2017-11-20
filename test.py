import requests
import cafeteria
import json
import schedule

def danbeeAi(message):
  r = requests.post("https://danbee.Ai/chatflow/engine.do",
    data = json.dumps({
      "chatbot_id" : "bc17a2c2-85b4-4d71-9c0f-ef77d71a3de9",
      "input_sentence": message
    }),
    headers={'Content-type': 'application/json;charset=UTF-8'})
  data = r.json()
  botResult = {
    "sentence" : data['responseSet']['result']['input_sentence'],
    "intent": data['responseSet']['result']['ref_intent_id'],
    "message" : data['responseSet']['result']['result'][0]['message'],
    "param": data['responseSet']['result']['parameters']
  }
  return botResult


botResult = danbeeAi("12월 일정정정정")
print(botResult)
def match(botResult):
  if(botResult['intent'] == "급식"):
    if(botResult['param']['급식'] == "급식"):
      if(botResult['param']['일'] != "Null"):
        print(cafeteria.day(int(cafeteria.currentDay) + int(botResult['param']['일'])))
      elif(botResult['param']['날짜'] != "Null"):
        if(botResult['param']['날짜'] == "이번주"):
          print(cafeteria.week(1))
        elif(botResult['param']['날짜'] == "다음주"):
          print(cafeteria.week(0))
        elif(botResult['param']['날짜'] == "월"):
          print(cafeteria.dayofweek(1))
        elif(botResult['param']['날짜'] == "화"):
          print(cafeteria.dayofweek(2))        
        elif(botResult['param']['날짜'] == "수"):
          print(cafeteria.dayofweek(3))        
        elif(botResult['param']['날짜'] == "목"):
          print(cafeteria.dayofweek(4))        
        elif(botResult['param']['날짜'] == "금"):
          print(cafeteria.dayofweek(5))        
      else:
        print(cafeteria.day(int(cafeteria.currentDay)))
  elif(botResult['intent'] == "일정"):
    if(botResult['param']['단어'] == "일정"):
      print(schedule.monthSchedule(int(schedule.currentMonth) + int(botResult['param']['날짜'])))
  else:
    print(botResult['message'])

match(botResult)
        
      