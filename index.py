from flask import Flask, request
from difflib import SequenceMatcher
import json
import requests

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
PAT = 'EAAYi1m8AgjUBAPf0iePgkrD2GPNmCz0CMO59Cqyl6UZCR2VUZCOtU06rE6FphSwv4xrrenP4NF1eIuQQUQalH6naTr4fiXnFd0rN6HTgb03VpZAhYQs2MAQeGqZBqCskOZA7uTeHwzLsJGmmaqQVco8MmmbCJu1N9I2rNtZAEEZCAZDZD'
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
  print('Handling Messages')
  payload = request.get_data()
  for sender, message in messaging_events(payload):
    print(message.decode('unicode_escape'))
    send_message(PAT, sender, message)
  return "ok"

def messaging_events(payload):
  """Generate tuples of (sender_id, message_text) from the
  provided payload.
  """
  data = json.loads(payload)
  messaging_events = data["entry"][0]["messaging"]
  for event in messaging_events:
    if "message" in event and "text" in event["message"]:
      yield event["sender"]["id"], event["message"]["text"].encode('unicode_escape')
    else:
      yield event["sender"]["id"], "I can't echo this"


def send_message(token, recipient, text):
  message = text.decode('unicode_escape')
  print(message_matching(message))
  if(message):
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
      params={"access_token": token},
      data=json.dumps({
        "recipient": {"id": recipient},
        "message": {"text": message}
      }),
      headers={'Content-type': 'application/json'})


def message_matching(message):
  if(message.SequenceMatcher(Nonde, '급식', message).ratio() > 0.5):
    print(message)
    
if __name__ == '__main__':
  app.run()