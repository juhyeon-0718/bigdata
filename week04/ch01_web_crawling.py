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
import time  # 파이썬 시간 관련 기능 제공

### case 1) ul 태그 하위 항목을 모두 뽑아오고 싶을 때
# for child in soup.ul.children:
#     print(child.get_text())
#     time.sleep(2)  # 5초 간격

### case 2) find_all: 괄호 안에 지정한 태그의 모든 값을 가져오는 함수
# print(soup.find_all('div'))

# for f in soup.find_all('div'):
#     print(f.get_text())

### case 3) 정규식 활용 : <ol>, <ul>든 다 포함된 리스트를 긁어오고 싶을 때
import re
# re.compile('') : 정규식 개체를 return 해주는 함수
# for f in soup.find_all(re.compile('[ou]l')) :
#     print(f)

### case 4) List 활용 : 원하는 태그를 직접 지정해서 뽑는 경우
#### ex: h1, a 태그만 보고 싶을 때
# for f in soup.find_all(['h1', 'a']):
#     print(f.get_text())

### case 5) CSS 선택자를 통해 원하는 부분을 가져올 때
'''css : 웹 페이지의 레이아웃 스타일을 디자인하고 정의하는데 사용하는 스타일 시트 언어
    HTML과 함께 사용'''
a = soup.select('a:nth-child(1)')
# print(a)

# for f in a :
    # print(f.get_text())

### case 6 ) TEXT만 가지고 오고 싶을 때 : range() 활용
for x in range (0, 10):
    print('현재 X : ' , x)
    print(soup.select('li')[x].get_text())
    time.sleep(2)

'''
결과값
현재 X :  0
중고거래
현재 X :  1
부동산
현재 X :  2
중고차
...

'''

