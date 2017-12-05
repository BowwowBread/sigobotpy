# -*- coding: utf-8 -*- 

from urllib.request import urlopen
from bs4 import BeautifulSoup
import difflib
import datetime
import re 

now = datetime.datetime.now()
currentTime = now.strftime('%Y%m')
currentYear = now.strftime('%Y')
currentMonth = now.strftime('%m')
currentDay = now.strftime("%d")
if(int(currentDay) < 10) :
  currentDay = str(currentDay).replace('0', '')
weekdic = {1: '월', 2: '화', 3: '수', 4: '목', 5: '금'}
def timeReset():
  global currentTime, currentYear, currentMonth, currentDay
  currentTime = now.strftime('%Y%m')
  currentYear = now.strftime('%Y')
  currentMonth = now.strftime('%m')
  currentDay = now.strftime("%d")
  if(int(currentDay) < 10) :
    currentDay = str(currentDay).replace('0', '')
def searchCafeteria():
  global currentDay
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
  return body
def day(date):
    global currentTime      
    global currentMonth
    print(date)
    body = searchCafeteria()
    result = ''    
    for v in body.find_all('td'):
        # 비어있는 날 체크        
        if len(v.div.contents) != 0 :
            # 해당 날짜 찾기            
            if v.div.contents[0] == str(date):
                # 해당 날짜 데이터 체크                
                if len(v.div) != 1 :
                    result += currentMonth + '월' + str(date) + '일 급식 '
                    result += re.sub('[0-9a-zA-Z(\.)<>]','',str(v.div)).replace('/', '\n').replace('[중식]', ' ')
                    return result 
                else :
                    return "\n" + str(date) + "일은 급식을 먹는 날이 아니에요"
    if result == "" :
        endDay = findEndDay(int(currentMonth))
        if(int(date) > endDay):
          currentMonth = str(int(currentMonth)+1)
          if(int(currentMonth) < 10):
              currentMonth = "0"+currentMonth
          currentTime = currentYear + currentMonth
          return day(int(date) - endDay)
        return "\n" + str(date) + "일은 급식을 먹는 날이 아니에요"

def week(state):
    global currentTime      
    global currentMonth
    global currentDay
    body = searchCafeteria()  
    result = ""
    for v in body.find_all('td') :
        # 비어있는 날 체크
        if len(v.div.contents) != 0 :
            # 해당 날짜 찾기
            if v.div.contents[0] == str(currentDay) :
                endDay = findEndDay(int(currentMonth))                                    
                # 이번주
                if state == 1 :
                    result += "이번 주 급식 \n"
                    timeout = 0
                    daycount = 0
                    for i in v.parent.find_all('div') :
                        if len(i) != 1:
                            result += re.sub('[0-9a-zA-Z(\.)<>]', '', str(i)).replace('/', '\n').replace('[중식]', weekdic[daycount] + " " + i.contents[0] )
                        elif daycount != 6 and daycount != 0:
                            if(endDay - int(currentDay) < 7):
                              currentMonth = str(int(currentMonth)+1)
                              if(int(currentMonth) < 10):
                                 currentMonth = "0"+currentMonth
                              currentTime = currentYear + currentMonth
                              currentDay = 1
                              body = searchCafeteria()                              
                              for v in body.find_all('td'):
                                if(len(v.div.contents) != 0) :
                                  if(v.div.contents[0] == str(currentDay)):
                                    for (index,i) in enumerate(v.parent.find_all('div')):
                                      if len(i) > 1:      
                                        result += re.sub('[0-9a-zA-Z(\.)<>]', '', str(i)).replace('/', '\n').replace('[중식]', weekdic[daycount] + " " + i.contents[0] )
                                      elif daycount < 5:
                                        result += "\n" + i.contents[0] + "일 " + weekdic[daycount] + "요일은 급식을 먹는날이 아니에요 \n"
                                        timeout += 1        
                            else:
                              result += "\n" + i.contents[0] + "일 " + weekdic[daycount] + "요일은 급식을 먹는날이 아니에요 \n"
                              timeout += 1                            
                        elif timeout >= 5 :
                            return "\n 이번 주는 급식을 먹는날이 아니에요 \n"
                        daycount += 1
                    return result
                # 다음주
                elif state == 0 :
                    try:
                        result += "다음 주 급식 \n"
                        timeout = 0
                        daycount = 0                    
                        for i in v.parent.find_next_sibling('tr').find_all('div') :
                            if len(i) != 1 :
                                result += re.sub('[0-9a-zA-Z(\.)<>]', '', str(i)).replace('/', '\n').replace('[중식]', weekdic[daycount] + " " + i.contents[0])
                            elif daycount != 6 and daycount != 0:
                                result += "\n" + i.contents[0] + "일 " + weekdic[daycount] + "요일은 급식을 먹는날이 아니에요 \n"
                                timeout += 1                     
                            elif timeout >= 5 :
                                return "\n 다음 주는 급식을 먹는날이 아니에요 \n"
                            daycount += 1
                        return result
                    except:
                        if(endDay - int(currentDay) < 7):
                          currentMonth = str(int(currentMonth)+1)
                          if(int(currentMonth) < 10):
                            currentMonth = "0"+currentMonth
                          currentTime = currentYear + currentMonth
                          currentDay = 1
                          return week(0)
                      
def dayofweek(day):
    global currentTime      
    global currentMonth
    global currentDay
    body = searchCafeteria()  
    result = ""
    for v in body.find_all('td'):
        # 비어있는 날 체크        
        if len(v.div.contents) != 0 :
            # 해당 날짜 찾기            
            if v.div.contents[0] == str(currentDay) :
                daylist = str(v.parent).split('</td>')            
                # 날짜 찾기    
                dayday = re.sub('[a-zA-Z(\/.)(\n)<>]', '',daylist[day].split('<br/>')[0])
                if len(daylist[day]) > 18:
                    result += weekdic[day] + "요일 급식"
                    result += re.sub('[0-9a-zA-Z(\.)<>]', '', daylist[day]).replace('/', '\n').replace('[중식]', dayday)    
                    return result
                elif dayday == " ":
                    endDay = findEndDay(int(currentMonth))                                    
                    if(endDay - int(currentDay) < 8):
                      currentMonth = str(int(currentMonth)+1)
                      if(int(currentMonth) < 10):
                        currentMonth = "0"+currentMonth
                      currentTime = currentYear + currentMonth
                      print(currentTime)
                      currentDay = 1
                      return dayofweek(day)
                    elif(endDay - int(currentDay) > endDay - 7):
                      currentMonth = str(int(currentMonth)-1)
                      currentTime = currentYear + currentMonth
                      currentDay = endDay       
                      return dayofweek(day)                                     
                    else:
                      return weekdic[day] + "요일은 급식을 먹는날이 아니에요"
                else:
                    return weekdic[day] + "요일은 급식을 먹는날이 아니에요"

def findEndDay(month):
  case31 = [1,3,5,7,8,10,12]
  case30 = [4,6,9,11]
  case28 = [2]
  if(month == case28[0]):
      return 28
  for i in case31:
    if(month == i):
      return 31
  for i in case30:
    if(month == i):
      return 30
