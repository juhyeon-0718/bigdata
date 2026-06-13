#데이터 분석 기초
## 데이터 파악
### 데이터 파악 함수
'''
head() 데이터의 앞 부분 출력

tail() 데이터의 뒷 부분 출력

shape 행, 열 개수 출력

info() 변수 속성 출력

describe() 요약 통계량 출력
'''

import pandas as pd
from setuptools.command import rotate

path = 'C:/JJH_bigdata/Data/'
exam = pd.read_csv(path + 'exam.csv')
# print(exam)
# print(exam.head())
# print(exam.head(10))
# print(exam.tail(10))
# print(exam.shape)
# print(exam.info())
# print(exam.describe())


## mpg 데이터 파악
mpg = pd.read_csv(path + 'mpg.csv')
# print(mpg.info())


df_raw = pd.DataFrame({'var1': [1, 2, 1],
                       'var2': [3, 4, 5]})
# print(df_raw)

### 복사
df_new = df_raw.copy()
# print(df_new)

### 변수명 수정
df_new = df_new.rename(columns={'var2' : 'v2'})
# print(df_new)


#### 파생 변수
df = pd.DataFrame({'var1': [1, 2, 3],
                   'var2': [3, 4, 5]})
#### 변수를 조합하여 파생변수 생성
df['var_sum'] = df['var1'] + df['var2']
# print(df)


df['var_mean'] = (df['var1'] + df['var2']) / 2
# print(df)

mpg['total'] = (mpg['cty']+ mpg['hwy'] ) /2
# print(mpg.head())
# print(mpg.tail())

# 당시 미국차들의 통합 연비가 평균적으로 얼마인가
a = sum(mpg['total']) / len(mpg)
# print(a)

import matplotlib.pyplot as plt

### 조건문을 활용하여 파생변수 생성하기
# 1. 기준값 정하기
# print(mpg['total'].describe())

# 2. 합격 판정 변수 생성
import numpy as np
### 기준이 20 이상이면 pass, 아니면 fail
mpg['test'] = np.where(mpg['total'] >= 20, 'pass', 'fail')

# 3. 빈도표로 합격 판정 자동차 수 알아보기
a = mpg['test'].value_counts() # 빈도표 생성 함수
# print(a)

# 4. 막대 그래프로 빈도 표현
count_test = mpg['test'].value_counts()
count_test.plot.bar(rot = 0)
plt.show()

## 중첩 조건문 활용
'''
A: 30이상
B: 20 ~ 29
C: 20 미만 
'''

#1. 연비 등급 변수 만들기
### TOTAL 기준으로 a,b,c 등급 부여
mpg['grade'] = np.where(mpg['total'] >= 30, 'A',
                        np.where(mpg['total'] >= 20, 'B', 'C'))

print(mpg.tail(10))

### 2. 빈도표 막대로 연비 등급 살펴보기
count_grade = mpg['grade'].value_counts()
print(count_grade)

count_grade.plot.bar(rot = 0)
plt.show()