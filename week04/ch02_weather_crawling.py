""" 국내 주요 도시 네이버날씨 요약 프로그래밍 """
import datetime # 날짜 , 시간 관련
from bs4 import BeautifulSoup
import urllib.request
import requests

# 현재 시간을 출력하고 스타일에 맞게 출력문 수정
now = datetime.datetime.now() # 현재시간
nowDate =  now.strftime('%Y년 %m월 %H시 %M분 입니다. ')

print('■' * 100)
print('\t\t\t\t\t\t\t ※ Python Web Crawling Project ※' )
print('\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t ※ ID : Juhyeon' )
print('■' * 100)
print('반갑습니다. 현재 시간은' , nowDate, '\n')
print("\t Let Me Summarize Today's Weather Info")

print('#오늘의 #날씨 #요약 \n')
## 서울 날씨 가져오기
webpage_s = urllib.request.urlopen('https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8&ackey=xg5flzav')
soup = BeautifulSoup(webpage_s, 'html.parser')
temps = soup.find_all('strong')
cast = soup.find('p', 'summary')
print('🌡️ 서울 날씨 : ', temps[5].get_text(), cast.get_text())

webpage_b = urllib.request.urlopen('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=%EB%B6%80%EC%82%B0%EB%82%A0%EC%94%A8&oquery=%EC%84%9C%EC%9A%B8+%EB%82%A0%EC%94%A8&tqi=jAzNrdqostGssNgzby0-381156&ackey=26i49gyb')
soup_b = BeautifulSoup(webpage_b, 'html.parser')
temps_b = soup_b.find_all('strong')
cast_b = soup_b.find('p', 'summary')
print('🌡️ 부산 날씨 : ', temps_b[5].get_text(), cast_b.get_text())


webpage_j = urllib.request.urlopen('https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&ssc=tab.nx.all&query=%EC%A0%9C%EC%A3%BC%EB%82%A0%EC%94%A8&oquery=%EB%B6%80%EC%82%B0%EB%82%A0%EC%94%A8&tqi=jAzPWwqostGssNgzUlK-303485&ackey=cnwn5fl8')
soup_j = BeautifulSoup(webpage_j, 'html.parser')
temps_j = soup_j.find_all('strong')
cast_j = soup_j.find('p', 'summary')
print('🌡️ 제주 날씨 : ', temps_j[5].get_text(), cast_j.get_text())

#-------------------------------------------------------------------------------

