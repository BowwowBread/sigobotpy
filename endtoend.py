import requests
import json

def wordSearch(word):
  r = requests.post("http://0xf.kr:2580/wordchain/next",
    data= json.dumps({
      "char": word[0]
    })
  )
  if(r.status_code == "200"):
    print(r.text)
  else:
    print(r.text)


wordSearch("바나나")