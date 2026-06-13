from itertools import groupby

import pandas as pd
import numpy as np
from numpy.testing import print_coercion_tables

'''
데이터 가공 , 데이터 전처리
분석에 적합하게 데이터를 가공하는 작업
- pandas : 전처리 작업에 가장 많이 사용되는 패키지
    1. query() : 행 추출
    2. df[] : 열 추출
    3. sort_values() : 정렬
    4. groupby() : 집단별로 나누기 (군집화)
    5. assign() : 변수 추가 (파생변수)
    6. agg() : 통계치 구하기
    7. merge() : 데이터 합치기 (열) 
    8. concat() : 데이터 합치기 (행)
'''

path = 'C:/JJH_bigdata/Data/'

# 1. 조건에 맞는 데이터만 추출하기 ( 행 추출 ) : df.query()
exam = pd.read_csv(path + 'exam.csv')
# print(exam)

### 데이터에서 1반만 추출 -> query('조건문')
a = exam.query('nclass == 1')
# print(a)

### 데이터에서 1반 빼고 추출 -> query('반대조건')
a = exam.query('nclass !=1')
# print(a)

## 초과와 미만, 이상, 이하 조건 걸기
### 수학 점수가 50점을 초과한 학생
a = exam.query('math > 50')
# print(a)

### 영어 점수가 60점 이상인 학생
a = exam.query('english >= 60')
#print(a)

### 1반이면서 수학 점수가 50점 이상인 경우
a = exam.query('(nclass == 1) & (math >= 50)')
# print(a)

### 수학 점수가 90점 이상이거나 영어 점수가 90점 이상인 경우
a = exam.query('(math >= 90) | (english >= 90)')
# print(a)

## 목록에 해당하는 행 추출
### 1, 3, 5반에 해당하면 추출
b = exam.query('nclass in [1,3,5]')
# print(b)

## 문자변수를 이용해서 조건에 맞는 행 추출
### '전체 조건'과 '추출할 문자'에 서로 다른 모양의 따옴표 입력
df = pd.DataFrame({'sex' : ['F', 'M', 'F','M'],
                  'country' : ['Korea', 'China', 'Japan', 'USA']})

a = df.query('sex == "F" & country == "Korea"')
# print(a)

''' 
연산자
in: 매칭 확인 (포함 연산자)
// : 나눗셈의 몫
/ : 나눗셈
% : 나머지
'''

## 변수 추출하기 : 데이터명['변수명'] **변수명까지 출력하려면 [[]] -> 데이터 프레임으로 추출
# print(exam['math'])
# print(exam[['math']])
# print(exam[['nclass','math', 'english']])

## 변수 제거하기 : .drop(columns = ['제거 변수명']
a = exam.drop(columns=['math'])
# print(a)

## pandas 함수 조합
### 1반 학생의 영어 점수 추출
a = exam.query('nclass == 1')['english']

### 수학 점수 50점 이상인 학생만 아이디, 수학 앞부분 5
a = exam.query('math >= 50')[['id', 'math']].head(5)
# print(a)

### 가독성 있게 바꾸기 -> \ + enter 로 줄바꿈
a = (exam.query('math>- 50') \
    [['id','math']] \
     .head(5))
# print(a)

##  순서대로 정렬하기
### 오름차순
a = exam.sort_values('math')
# print(a)

### 내림차순
a = exam.sort_values('math', ascending=False)
# print(a)

## 여러 정렬 기준 적용
### 반 별 정렬, 수학 점수 -> 오름차순 정렬
a = exam.sort_values(['nclass', 'math'])
# print(a)

### 반 별 -> 오름차순, 수학 점수 -> 내림차순
a = exam.sort_values(['nclass', 'math'], ascending=[True, False])
# print(a)

# 5.파생변수 추가 - assign() : 해당 함수가 실행될 때만 파생변수가 생섣 (원본데이터에 영향을 주지 않음)
###  총점 변수 추가
total = exam.assign(total = exam['math'] + exam['english'] + exam['science'])
# print(total)
# print ('-' * 100)
# print(exam) # 원본 데이터에는 total 파생 변수가 없음

### 원본 데이터에 파생 변수 생성
# exam = exam.assign(total = exam['math'] + exam['english'] + exam['science'])
# print(exam)

### 여러가지 파생 변수 추가
a = exam.assign(
    total = exam['math'] + exam['english'] + exam['science'],
    mean= exam['math'] +  exam['english'] + exam['science'] /3
)
# print(a)

## assign + np.where
result = exam.assign(result = np.where(exam['science'] >= 60, 'PASS', 'FAIL'))
# print(result)

### 추가한 변수를 바로 함수에서 사용
a = exam.assign(total = exam['math'] + exam['english'] + exam['science'])\
    .sort_values('total')
# print(a)

## 4. .groupby(), .agg(): 집단 별로 요약하기
### .agg(변수명 = (적용대상 변수명, 함수명))
a = exam.groupby('nclass')

### 수학 평균 구하기
b = exam.agg(math_mean = ('math', 'mean'))
# print(b) # 결과값: 57.45

### 집단별 요약 통계량
a = (exam.groupby('nclass') \
     .agg(math_mean = ('math', 'mean')))

# print(a)

### 여러가지 요약 통계량
a = exam.groupby('nclass')\
    .agg(math_mean = ('math', 'mean'),
         math_sum= ('math', 'sum'),
         math_median = ('math', 'median'),
         count = ('nclass', 'count'))
# print(a)

'''
agg에서 자주 사용하는 요약 통계량 : mean(평균), std(표준편차), median(중앙값), min/max(최솟값/최댓값), sum(합계), count(빈도, 개수)
'''

## 집단별로 다시 집단 나누기 (ex: 대분류 -> 중분류 -> 소분류)
mpg = pd.read_csv(path + 'mpg.csv')
# print(mpg.info())
# print(mpg)
### 제조사 및 구동 방식
a = mpg.groupby(['manufacturer', 'drv'])\
    .agg(mean_cty = ('cty', 'mean'))
# print(a)

### 제조회사별로 suv 자동차의 도시 및 고속도로 합산 연비 평균 구하고 내림차순 정렬
# a = mpg.query('category== "suv"')\
#     .groupby('manufacturer')\
#     .assign(
#          mean_cty = (mpg['cty'] + mpg['hwy']) / 3
#          )

a = mpg.query('category== "suv"')\
    .assign(total = (mpg['cty'] + mpg['hwy']) / 2)\
    .groupby('manufacturer')\
    .agg(mean_total = ('total', 'mean'))\
    .sort_values('mean_total', ascending=False)\
    .head()
# print(a)


# 데이터 합치기
## df.merge : 데이터 가로로 병합
test1 =pd.DataFrame()
test2 = pd.DataFrame({'id' : [1,2,3,4,5],
                      'final' : [60, 80, 70, 90, 95]})

'''
1. pd.merge() 에 결합할 데이터 프레임명 나열
2. how = 'left' : 오른쪽에 입력한 데이터 프레임을 왼쪽 데이터 프레임에 결합
3. on : 데이터를 합칠 때 기준 삼을 변수명 입력 
'''
# total  = pd.merge(test1,test2, how = 'left', on = 'id')
# print(total)

## 다른 데이터를 활용해서 새로운 변수 추가 -> 매칭
name = pd.DataFrame({'nclass': [1,2,3,4,5],
                     'teacher': ['kim', 'lee', 'park', 'choi', 'jung']})
# print(name)

### nclass  기준으로 합쳐서 exam_new에 할당
exam_new = pd.merge(exam, name, how="left", on='nclass')

## 세로로 합치기
### 면접자 1-5
group_a = pd.DataFrame({'id ': [1, 2,3, 4,5],
                        'test' : [90, 80, 96, 90, 82]})

group_b = pd.DataFrame({'id ': [6,7,8,9,10],
                        'test' : [100, 80, 86, 90, 92]})

### 데이터 합쳐서 group_all에 할당
group_all = pd.concat([group_a, group_b], ignore_index=True)
print(group_all)

### 인덱스가 중복되지 않도록 새로 부여하려면 pd.contcat()에 ignore_index = True