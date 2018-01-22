# -*- coding: utf-8 -*- 

from flask import Flask, request
from difflib import SequenceMatcher
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import json
import requests
import time
import atexit
import bot
import cafeteria
import datetime
import ssl

now = datetime.datetime.now()

app = Flask(__name__)
access_token = 'EAAHGoGpG0ZCMBAHo12tOy9AeQH0creyGZBVRz7nHf1F8JvUBVDJEiYwUOt8msaARTgZATWj9MEXzJ5ukIV2vHFAggE3OeUXKcyOmSqlPK6U0uNUI0nHri8EfcCxmZCXdalYvZA8w7V66Pm5wUnFDsCbGB5Mwt5KLKGq6fQ8UHGgZDZD'
@app.route('/', methods=['GET'])
def handle_main():
  print('main')
  print(now)
  return("main")

@app.route('/webhook', methods=['GET'])
def handle_verification():
  print('Handling Verification.')
  if request.args.get('hub.verify_token', '') == 'sigo':
    print('Verification successful!')
    return request.args.get('hub.challenge', '')
  else:
    print('Verification failed!')
    return 'Error, wrong validation token'

@app.route('/webhook', methods=['POST'])
def handle_messages():
  try:
    data = request.get_json()
    if data["object"] == "page":
        for entry in data["entry"]:
            if("messaging" in entry):
              for messaging_event in entry["messaging"]:
                  if messaging_event.get("message"): 
                      if "is_echo" in messaging_event["message"]:
                        pass
                      else:
                        sender_id = messaging_event["sender"]["id"]   
                        message_text = messaging_event["message"]["text"]  
                        print("receip message :" + message_text + " , time : " + str(datetime.datetime.now()))
                        text_match(sender_id, message_text)
                  if messaging_event.get("postback"):
                      sender_id = messaging_event["sender"]["id"]   
                      payload = messaging_event["postback"]["payload"]
                      payload_match(sender_id, payload)
    return "ok", 200
  except:
    return "ok", 200

def payload_match(sender_id, payload):
  if(payload == "STARTED"):
    send_text(sender_id, "안녕 나는 시고야")
    send_text(sender_id, "메뉴에서 버튼을 누르면 도움말을 볼 수 있어")
  elif(payload == "CAFETERIA"):
    send_text(sender_id, "급식 사용법을 알려줄게")
    send_text(sender_id, "먼저 오늘 급식과 내일 급식을 알 수 있어")
    send_text(sender_id, "예를들면 급식, 점심, 밥, 내일급식 이렇게 말이야")
    send_text(sender_id, "그리고 이번 주 급식과 다음 주 급식을 알 수 있고,")
    send_text(sender_id, "월요일 급식, 목요일 급식, 8일 급식 이런식으로도 알 수 있어")
  elif(payload == "SCHEDULE"):
    send_text(sender_id, "일정 사용법을 알려줄게")
    send_text(sender_id, "먼저 이번 달 일정과 다음 달 일정을 알 수 있어")
    send_text(sender_id, "예를들면 일정, 스케줄, 이번달 일정, 다음달 일정 이렇게 말이야")
    send_text(sender_id, "그리고 12월 일정 이런식으로 직접 날짜를 입력해도 돼")
  else:
    send_text(sender_id, "뭐")

def send_buttton(sender_id, attachment):
  send_action(sender_id, "typing_on")                        
  data = json.dumps({
    "recipient": {"id": sender_id},
    "message": {
      "attachment": attachment
    }
  })
  send_message(data)

def text_match(sender_id, message_text):
  send_action(sender_id, "typing_on")                          
  result = bot.messageMatching(message_text)
  if(result == message_text):
    send_text(sender_id, message_text)
  else:
    send_api(sender_id, result)    

def send_text(sender_id, message_text):
  print("send text")  
  send_action(sender_id, "typing_on")                        
  time.sleep(len(message_text)/15)
  data = json.dumps({
    "recipient": {"id": sender_id},
    "message": {"text": message_text},
  })
  send_message(data)
  send_action(sender_id, "typing_off")                          

def send_api(sender_id, result):
  print("send api")
  send_action(sender_id, "typing_on")                       
  cafeteria.timeReset()                 
  data = json.dumps({
    "recipient": {"id": sender_id},
    "message": {"text": result},
  })
  send_message(data)
  send_action(sender_id, "typing_off")           

def send_action(sender_id, action):
  data = json.dumps({
    "recipient": {"id": sender_id},
    "sender_action": action
  })
  send_message(data)
def send_message(data):
  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": access_token},
    data=data,
    headers={'Content-type': 'application/json'})

if __name__ == '__main__':
  ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
  ssl_context.load_cert_chain(certfile='public.pem', keyfile='private.pem', password='secret')
  print("test")
  app.run(host='0.0.0.0', port=80, debug = False, ssl_context=ssl_context)
