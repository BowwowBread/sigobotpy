from flask import Flask, request
import json
import requests

app = Flask(__name__)

access_token = 'EAAYi1m8AgjUBADYuPKYc2A3G8AC4XOpXmtUxBRtRYaDQe3kUeBSnbmytUb46ZBZCnYdDtqUPZBmZA3uEukBCtgKgRJtdZBamIDKBljwVjeqzsfOmAf52gxZCjbyOWjPc5ld1JkplAKIWM1OIolZAUq5YVwTJpZBZCUrD2UIM76UHWRwZDZD'
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

# @app.route('/webhook', methods=['POST'])
# def handle_messages():
#   data = request.get_json()
#   if data["object"] == "page":
#       for entry in data["entry"]:
#           for messaging_event in entry["messaging"]:
#               print(messaging_event)
#               if messaging_event.get("message"): 
#                   sender_id = messaging_event["sender"]["id"]   
#                   recipient_id = messaging_event["recipient"]["id"] 
#                   message_text = messaging_event["message"]["text"]  
#                   send_message(access_token, sender_id, message_text)
#               if messaging_event.get("postback"):
#                   print("postback")
#                   pass
#   return "ok"

@app.route('/', methods=['POST'])
def handle_messages():
  print "Handling Messages"
  payload = request.get_data()
  print payload
  for sender, message in messaging_events(payload):
    print "Incoming from %s: %s" % (sender, message)
    send_message(access_token, sender, message)
  return "ok"
def messaging_events(payload):
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"

def send_message(token, recipient, text):
  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print(r.text)

if __name__ == '__main__':
  app.run()