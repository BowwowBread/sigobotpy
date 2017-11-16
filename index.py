from flask import Flask, request
from difflib import SequenceMatcher
import json
import requests
import time
import bot

app = Flask(__name__)

access_token = 'EAAYi1m8AgjUBAKyZCZACLdFXld4ni5BW81BWYebWN3DZAnjObvZCpZA3EmqOC4IbPLtv71lwj5Kfd1YU4mezgDirZAcmGBmCwVxOZAqjssJzRuUNmWJ7cY3qhsZBckpZC5QlwwLRLbstIZAZBuFwCAc8SCipNcjqqRuTn8MZCsYZBYaeUpAZDZD'
@app.route('/', methods=['GET'])
def handle_main():
  print('main')
  return("main")


@app.route('/webhook', methods=['GET'])
def handle_verification():
  print('Handling Verification.')
  if request.args.get('hub.verify_token', '') == 'SIGO':
    print('Verification successful!')
    return request.args.get('hub.challenge', '')
  else:
    print('Verification failed!')
    return 'Error, wrong validation token'

@app.route('/webhook', methods=['POST'])
def handle_messages():
  data = request.get_json()
  if data["object"] == "page":
      for entry in data["entry"]:
          for messaging_event in entry["messaging"]:
              if messaging_event.get("message"): 
                  sender_id = messaging_event["sender"]["id"]   
                  message_text = messaging_event["message"]["text"]  
                  text_match(sender_id, message_text)
                  #text_match
              if messaging_event.get("postback"):
                  sender_id = messaging_event["sender"]["id"]   
                  payload = messaging_event["postback"]["payload"]
                  payload_match(sender_id, payload)
  return "ok"


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
  elif(payload == "ENDTOEND"):
    print(payload)
  else:
    print("payload error")

def send_buttton(sender_id, attachment):
  send_action(sender_id, "typing_on")                        
  data = json.dumps({
    "recipient": {"id": sender_id},
    "message": {
      "attachment": attachment
    }
  })
  print(data)
  send_message(data)
  
# def get_userProfile(sender_id):
#   r = requests.get("https://graph.facebook.com/v2.6/"+sender_id+"?fields=first_name,last_name",
#     params={"access_token": access_token})
#   if(r.status_code == 200):
#     print(r.text)

def text_match(sender_id, message_text):
  result = bot.messageMatching(message_text)
  if(result == message_text):
    send_text(sender_id, message_text)
  else:
    send_api(sender_id, result)    

def send_text(sender_id, message_text):
  send_action(sender_id, "typing_on")                        
  time.sleep(len(message_text)/15)
  data = json.dumps({
    "recipient": {"id": sender_id},
    "message": {"text": message_text},
  })
  send_message(data)
  send_action(sender_id, "typing_off")                          

def send_api(sender_id, result):
  send_action(sender_id, "typing_on")                        
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
  app.run()


