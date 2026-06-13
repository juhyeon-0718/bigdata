""" 텍스트 마이닝 (Text Mining) : 문자로 된 데이터에서 유의미한 정보를 가져오는 분석 기법
    - 형태소 분석 : 문장을 구성하는 어절들의 품사를 분석, 텍스트 마이닝시 가장 먼저 하는 작업
        -> 명사, 동사, 형용사 등 의미를 지닌 품사를 추출해 빈도를 확인

    실습데이터에 있는 문재인 대통령의 출마 선언문을 활용한다
    -> 대통령 연설문은 문법 오류 없이 문장이 정제되어 있음
    -> 전처리 작업을 많이 하지 않아도 텍스트 마이닝을 익히는데 적합

"""
# 1. KoNLPy 패키지 설치 : 한글 텍스트 마이닝 패키지
## 1) Java 설치 : 운영 체제 버전에 맞는 설치 파일 다운로드 (x64)

## 2) 시스템 환경변수 편집

## 3) 패키지 설치

## 4) Konlpy 의존성 패키지 설치: pip install jpype1 ->  pip install konlpy

import konlpy
han = konlpy.tag.Hannanum()
# print(han.nouns('대한민국의 영토는 한반도와 그 부속도서로 한다. '))

## 가장 많이 사용된 단어 알아보기 - 연설문
### 1. 연설문 불러오기
'''
open()으로 텍스트 파일을 열고 read()로 불러옴
encoding = UTF8:  불러올 파일의 인코딩을 UTF-8로 지정
만약 깨지는 경우 -> EUC-KR, cp949 등 인코딩을 바꿔보며 파일을 읽어줌 
'''

path = 'C:/bigdata/Data/'
moon = open(path + 'speech_moon.txt', encoding = 'UTF-8').read()

### 2. 불필요한 문자 제거
'''
- 특수문자, 한주, 공백은 분석대상이 아니므로 제거
- re.sub()으로 한글이 아닌 모든 문자를 공백으로 치환
- [^가-힣] : 한글이 아닌 모든 문자를 의미하는 정규 표현식
'''

import re
moon = re.sub('[^가-힣]', ' ', moon)
# print(moon)

### 3. 명사 추출
hannanum = konlpy.tag.Hannanum()
nouns = hannanum.nouns(moon)

### 리스트를 다루기 쉽게 데이터 프레임으로 변환
import pandas as pd
df_word = pd.DataFrame({'word': nouns})
# print(df_word)

### 4. 단어 빈도표 생성
# str.len() ; 글자수 세기
# 글자수 변수 추가
df_word['count'] = df_word['word'].str.len()
# print(df_word)

#### 두글자 이상 단어만 남기기
df_word = df_word.query('count>=2')
# print(df_word.sort_values('count'))

#### 단어 빈도 구하기
df_word = df_word.groupby('word', as_index = False)\
    .agg(n=('word', 'count'))\
    .sort_values('n',ascending = False)

# print(df_word)

### 5. 단어 빈도 막대 그래프 생성 - 단어 빈도 상위 20개 추출
top20 = df_word.head()
# print(top20)

import seaborn as sns
import matplotlib.pyplot as plt

plt.rcParams.update({'font.family':'Malgun Gothic',
                     'figure.dpi' : '120',
                     'figure.figsize':[6.5, 6]})
sns.barplot(data=top20, y='word', x='n')

''' 
    워드 클라우드 (Word Cloud) : 단어의 빈도를 구름 모양으로 시각화하는 그래프   
    - 단어의 빈도에 따라 글자의 크기와 색깔을 다르게 표현
    - 어떤 단어가 얼마나 많이 사용되었는지 한눈에 파악 가능
    pip install wordcloud
'''

font = 'C:/Windows/Fonts/HMKMMAG.TTF'

### 단어와 빈도를 담은 딕셔너리 생성 : 워드 클라우드의 입력값은 딕셔너리로 받음
# 단어는 KEY, VALUE로 구성된 딕셔너리 생성

dic_word = df_word.set_index('word').to_dict()['n']

from wordcloud import WordCloud
# wc = wordCloud(random_state=1234,
#                font_path=font,
#                width=400,
#                height=400,
#                background_color='white')

# img_wordcloud = wc.generate_fron_frequencies(dic_word)
plt.figure(figsize=(10,10)) #가로 세로 크기 설정
plt.axis('off') # 그래프 테두리선 없애기
plt.imshow(img_wordcloud) #워드 클라우드 출력
# plt.show()

### 워드클라우드 모양 바꾸기
# 1. mask 만들기 - 이미지 파일 불러오기
import PIL
icon = PIL.Image.open(path + 'cloud.png') # 흑과 백으로 구성되어있는 마스킹 이미지

import numpy as np
img = PIL.Image.new('RGB', icon.size, (255,255,255))
img.paste(icon, icon)
img = np.array(img)

# 2. 워드 클라우드 만들기 - mask = img
# wc = WordCloud(random_state = 1234,
#                font_path = font,
#                width=400,
#                height=400,
#                background_color='white',
#                mask=img,
#                colormap = 'inferno')
# img_wordcloud = wc.generated_from_frequencies(dic_word)
# plt.figsize(figsize=(10,10))
# plt.axis('off')
# plt.imshow(img_wordcloud)
# plt.show