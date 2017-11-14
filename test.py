import json

attachment = {
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":"날짜를 선택해주세요.",
        "buttons":[
          {
            "type":"postback",
            "title":"오늘 급식",
            "payload":"TODAY_CAFETERIA"
          },
          {
            "type":"postback",
            "title":"내일 급식",
            "payload":"TOMORROW_CAFETERIA"
          },
          {
            "type":"postback",
            "title":"요일 선택",
            "payload":"DAYOFWEEK_CAFETERIA"
          },
          {
            "type":"postback",
            "title":"이번 주 급식",
            "payload":"WEEK_CAFETERIA"
          },
          {
            "type":"postback",
            "title":"다음 주 급식",
            "payload":"NEXTWEEK_CAFETERIA"
          },
        ]
      }
    }
data = json.dumps({
  "recipient": {"id": "sender_id"},
  "message": {
    "attachment": attachment
  }
})

print(data)