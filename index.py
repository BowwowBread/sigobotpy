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
                  recipient_id = messaging_event["recipient"]["id"] 
                  message_text = messaging_event["message"]["text"]  
                  send_text(sender_id, message_text)
              if messaging_event.get("postback"):
                  print("postback")
                  pass
  return "ok"

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