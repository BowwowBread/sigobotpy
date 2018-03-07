# -*- coding: utf-8 -*- 

from urllib.request import urlopen
from bs4 import BeautifulSoup
import difflib
import datetime
import re 

now = datetime.datetime.now()
currentTime = now.strftime('%Y%m')
CurrentYear = now.strftime('%Y')
currentMonth = now.strftime('%m')
currentDay = now.strftime("%d")

def searchSchedule(month):
  if(int(month) < 10) :
    month = '0' + str(int(month))

  searchurl = "http://stu.sen.go.kr/sts_sci_sf01_001.do?schulCode=B100000599&schulCrseScCode=4&schulKndScCode=04&ay={{year}}&mm={{month}}"
  url = searchurl.replace('{{year}}', CurrentYear).replace('{{month}}', str(month))
  try:
    f = urlopen(url)
  except err:
    if err == 404:
      print("page not found")
    else:
      print(err)
  except err:
    print (err)
  html = f.read()
  soup = BeautifulSoup(html, "html.parser")
  body = soup.tbody
  # print(body)
  return body


def monthSchedule(month):
  result = str(month) + "월 일정 \n\n"
  body = searchSchedule(month)
  for v in body.find_all('div'):
    # 일정 유무 체크
    if(v.find_all('strong')):
      # 날짜
      result += v.em.get_text() + "일\n"
      for title in v.find_all('strong'):
        # 일정 제목
        result += title.get_text() + "\n"
      result += "\n"
  return result