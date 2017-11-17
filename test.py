import requests
import cafeteria
import json

def danbeeAi(message):
  r = requests.post("https://danbee.Ai/chatflow/engine.do",
    data = json.dumps({
      "chatbot_id" : "bc17a2c2-85b4-4d71-9c0f-ef77d71a3de9",
      "input_sentence": "hi"
    }),
    headers={'Content-type': 'application/json;charset=UTF-8'})
  data = r.json()
  return data['responseSet']['result']['result'][0]['message']


def postCafeteria():
  result = cafeteria.day(cafeteria.currentDay)

  r = requests.post("https://graph.facebook.com/v2.11/325920784549338/feed",
    params={"access_token": "EAAYi1m8AgjUBAP7O4UlHQ0oLo4ySlbJadak2lZCw3Bx5vmg2q6JAX4RFWE3FrguEQE3mMg9plZBjZBQ7PDnST4dnGFoS4UuonM3dZCrwblBlRfjTQHlOwLjhhFZAWYREuSGiACV9oSJkyIYzK7oM3uyyZBB1QGtV7gJRwjZA9XD3gZDZD"},
    data={
      "message" : result,
    }
  )
  if(r.status_code == "200"):
    print("success")
    print(r.text)  
  else:
    print(r.text)

postCafeteria()