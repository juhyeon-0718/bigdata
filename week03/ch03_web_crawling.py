"""
웹 크롤링 : 인터넷 사이트 같은 웹에서 유의미한 정보를 긁어오는 행위
HTML : 웹페이지의 표시를 위해 개발된 지배적 마크업 언어
"""
'''
HTML 기본 구조
<!DOCTYPE html>
<html>
    <head>  
        <title> 웹 페이지 제목 </title>
    </head>
    <body>
        <h1> 웹페이지 제목 </h1>
        <p> 내용 </p>
    </body>
</html>
'''
import requests
url = "https://www.daangn.com/kr/buy-sell/s/?in=%EB%B6%80%EC%A0%84%EC%A0%9C2%EB%8F%99-504"
response = requests.get(url)
# print(response.text)
'''
    [당근마켓 매물 크롤링하기]
    
    BeautifulSoup : html 문서에서 원하는 부분만 추출할 수 있도록 도와줌
    - 파싱 : html 또는 xml 문서를 구문 분석하여 파이썬 객체로 변환
'''
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.content, 'html.parser')
# print(soup.h1) # <h1 class="sprinkles_fontSize_400_base__1byufe8v2 sprinkles_fontSize_500_medium__1byufe8v8 sprinkles_fontWeight_bold__1byufe81z sprinkles_lineHeight_heading.large_base__1byufe8vm sprinkles_lineHeight_heading.xlarge_medium__1byufe8vs" level="1">부산광역시 부산진구 부전제2동 중고거래</h1>

# 필요한 텍스트만 추출
## 1. 반복문 사용
import time # 파이썬 시간 관련 기능 제공
### case 1) ul 태그 하위 항목을 모두 뽑아오고 싶을 때
for child in soup.ul.children:
    print(child.get_text())
    time.sleep(2) #5초 간격
'''
결과값
    중고거래
    부동산
    중고차
    알바/과외/레슨
    동네업체
    동네생활
    모임
    카페
'''
