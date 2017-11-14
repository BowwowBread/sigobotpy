from urllib.request import urlopen
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import difflib
import datetime
import re 

now = datetime.datetime.now()
currentTime = now.strftime('%Y%m')
currentMonth = now.strftime('%m')
currentDay = now.strftime("%d")
if(int(currentDay) < 10) :
  currentDay = str(currentDay).replace('0', '')
searchurl = "http://stu.sen.go.kr/sts_sci_md00_001.do?schulCode=B100000599&schulCrseScCode=4&schulKndScCode=04&schMmealScCode=2&schYm={{date}}"
url = searchurl.replace('{{date}}', currentTime)
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

def day(day):
    result = ""
    for v in body.find_all('td'):
        # 비어있는 날 체크        
        if len(v.div.contents) != 0 :
            # 해당 날짜 찾기            
            if v.div.contents[0] == str(day):
                # 해당 날짜 데이터 체크                
                if len(v.div) != 1 :
                    result += currentMonth + '월' + str(day) + '일 급식 \n'
                    result += re.sub('[0-9a-zA-Z(\.)<>]','',str(v.div)).replace('/', '\n').replace('[중식]', str(day))
                    return result 
                else :
                    return "\n" + str(day) + "일은 급식을 먹는 날이 아니에요"
    if result == "" :
        return "\n" + str(day) + "일은 급식을 먹는 날이 아니에요"

def week(state):
    result = ""
    for v in body.find_all('td') :
        # 비어있는 날 체크
        if len(v.div.contents) != 0 :
            # 해당 날짜 찾기
            if v.div.contents[0] == str(currentDay) :
                # 이번주
                if state == 1 :
                    result += "이번 주 급식 \n"
                    timeout = 0
                    daycount = 0
                    for i in v.parent.find_all('div') :
                        if len(i) != 1:
                            result += re.sub('[0-9a-zA-Z(\.)<>]', '', str(i)).replace('/', '\n').replace('[중식]', i.contents[0])
                        elif daycount != 6 and daycount != 0:
                            result += "\n" + i.contents[0] + "일은 급식을 먹는날이 아니에요 \n"
                            timeout += 1                            
                        elif timeout >= 5 :
                            return "\n 이번 주는 급식을 먹는날이 아니에요 \n"
                        daycount += 1
                    return result
                # 다음주
                elif state == 0 :
                    result += "다음 주 급식 \n"
                    timeout = 0
                    daycount = 0                    
                    for i in v.parent.find_next_sibling('tr').find_all('div') :
                        if len(i) != 1 :
                            result += re.sub('[0-9a-zA-Z(\.)<>]', '', str(i)).replace('/', '\n').replace('[중식]', i.contents[0])
                        elif len(i) != 1 and daycount != 6 and daycount != 0:
                            result += "\n" + i.contents[0] + "일은 급식을 먹는날이 아니에요 \n"
                            timeout += 1                           
                        elif timeout >= 5 :
                            return "\n 다음 주는 급식을 먹는날이 아니에요 \n"
                        daycount += 1
                    return result
def dayofweek(day):
    result = ""
    weekdic = {1: '월', 2: '화', 3: '수', 4: '목', 5: '금'}
    for v in body.find_all('td'):
        # 비어있는 날 체크        
        if len(v.div.contents) != 0 :
            # 해당 날짜 찾기            
            if v.div.contents[0] == str(currentDay) :
                daylist = str(v.parent).split('</td>')            
                # 날짜 찾기    
                dayday = re.sub('[a-zA-Z(\.)(\n)<>]', '',daylist[day].split('<br/>')[0])
                if len(daylist[day]) > 18:
                    result += weekdic[day] + "요일 급식"
                    result += re.sub('[0-9a-zA-Z(\.)<>]', '', daylist[day]).replace('/', '\n').replace('[중식]', dayday)    
                    return result
                elif dayday != ' ' :
                    return str(dayday).replace('/', '') +"일 " + weekdic[day] + "요일은 급식을 먹는날이 아니에요"
                else:
                    return str(dayday).replace('/', '') +"일 " + weekdic[day] + "요일은 급식을 먹는날이 아니에요"

# print('------------------day test---------------')
# for i in range(1,32) :
#     print(day(i))
# print('------------------week test---------------')
# print(week(1))
# print(week(0))
# print('------------------dayofweek test---------------')
# for i in range(1,6) :
#     print(dayofweek(i))

#--------------test--------------
def messageMatching(message):
  dayCount = 0
  message = message.replace(' ', '')
  if(textMatching(message, ["급식", "점심", "밥"], 0.3)):
    if(textMatching(message, ["내일", "낼"], 0.4)):
      return day(int(currentDay) + 1)
    elif(textMatching(message, ["이번주", "요번주"], 0.5)):
      return week(1)
    elif(textMatching(message, ["다음주", "담주"], 0.5)):
      return week(0)
    elif(textMatching(message, ["요일", "욜", "여일"], 0.2)):
      if(textMatching(message, ["월"], 0.1)):
        return dayofweek(1)
      elif(textMatching(message, ["화"], 0.1)):
        return dayofweek(2)
      elif(textMatching(message, ["수"], 0.1)):
        return dayofweek(3)
      elif(textMatching(message, ["목"], 0.1)):
        return dayofweek(4)
      elif(textMatching(message, ["금"], 0.1)):
        return dayofweek(5)
    elif(textMatching(message, ["일"], 0.2)):
      date = re.sub('[^0-9]', '', message)
      if(int(date) >= 1 and int(date) <= 31):
        return day(int(date))
      else:
        return "정확한 날짜를 입력해줘요"
    else:
      return day(currentDay)
  else:
    return message

def textMatching(message, matchText, ratio):
  for text in matchText:
    if(SequenceMatcher(None, text, message).ratio() > ratio):
      return True

print(messageMatching("금요일급식"))