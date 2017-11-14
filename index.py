from flask import Flask, request
import json
import requests

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
              print(messaging_event)
              if messaging_event.get("message"): 
                  sender_id = messaging_event["sender"]["id"]   
                  message_text = messaging_event["message"]["text"]  
                  send_text(sender_id, message_text)
                  #text_match
              if messaging_event.get("postback"):
                  sender_id = messaging_event["sender"]["id"]   
                  payload = messaging_event["postback"]["payload"]
                  payload_match(sender_id, payload)
  return "ok"


def payload_match(sender_id, payload):
  if(payload == "STARTED"):
    send_text(sender_id, "안녕하세요 SIGO 봇입니다. 메뉴에서 도움말 버튼을 누르시면 사용법을 확인하실 수 있습니다.")
    get_userProfile(sender_id)
  elif(payload == "CAFETERIA"):
    print(payload)
  elif(payload == "SCHEDULE"):
    print(payload)
  elif(payload == "ENDTOEND"):
    print(payload)
  else:
    print("payload error")

# def send_buttton(sender_id, message_text, title, payload):
#   data = json.dumps({
#     "recipient": {"id": sender_id},
#     "message": {
#       "attachment": {
#         "type": "postback",
#         "text": 
#       }
#     }
#   })
#   send_message(data)
  
def get_userProfile(sender_id):
  r = request.post("https://graph.facebook.com/v2.6/<PSID>?fields=first_name,last_name",
    params={"access_token": access_token})
  if(r.status_code == 200):
    print(r.text)

def send_text(sender_id, message_text):
  data = json.dumps({
    "recipient": {"id": sender_id},
    "message": {"text": message_text}
  })
  send_message(data)
def send_message(data):
  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": access_token},
    data=data,
    headers={'Content-type': 'application/json'})

if __name__ == '__main__':
  app.run()