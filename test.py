import json

attachment = {
  "type": "postback"
}
data = json.dumps({
  "recipient": {"id": "sender_id"},
  "message": {
    "attachment": attachment
  }
})

print(data)