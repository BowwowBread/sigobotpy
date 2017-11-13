from flask import Flask, request
import json
import requests

app = Flask(__name__)

# This needs to be filled with the Page Access Token that will be provided
# by the Facebook App that will be created.
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

@app.route('/webhook', methods=['POST'])
def handle_messages():
  data = request.get_json()
  if data["object"] == "page":
      for entry in data["entry"]:
          for messaging_event in entry["messaging"]:
              if messaging_event.get("message"):  # someone sent us a message
                  sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                  recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                  message_text = messaging_event["message"]["text"]  # the message's text
                  send_message(access_token, sender_id, message_text)
              if messaging_event.get("delivery"):  # delivery confirmation
                  pass
              if messaging_event.get("optin"):  # optin confirmation
                  pass
              if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                  pass
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
  """Send the message text to recipient with id recipient.
  """

  r = requests.post("https://graph.facebook.com/v2.6/me/messages",
    params={"access_token": access_token},
    data=json.dumps({
      "recipient": {"id": recipient},
      "message": {"text": text}
    }),
    headers={'Content-type': 'application/json'})
  if r.status_code != requests.codes.ok:
    print(r.text)

if __name__ == '__main__':
  app.run()