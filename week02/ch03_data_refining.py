import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


path = 'C:/JJH_bigdata/Data/'


'''
데이터 정제 : 빠진 데이터(결측치) , 이상한 데이터가 존재하면 제거하는 과정
    - 결측치 (Missing Value) : 누락되거나 비어있는 값
        - 데이터 수집 과정에서 발생한 오류로 포함될 가능성 有
        - 함수가 적용되지 않거나 결과가 왜곡 
        - 실제 데이터 분석시 결측치 확인, 제거 후 분석해야 함
        
    - 이상치(anomaly) : 정상 범위에서 크게 벗어나는 값
        - 실제 데이터에 대부분 이상치가 있음
        - 제거하지 않으면 분석 결과를 왜곡하므로 분석 전 제거 작업 필요
         
'''

# 결측치 찾는 방법 -> numpy의 nan (파이썬에선 결측치를 NaN으로 표기 -> 불러온 데이터에 결측치 존재하면 자동 NaN)
df = pd.DataFrame({'sex': ['M', 'F', np.nan, 'M', 'F'],
                   'score': [5,4,3,4,np.nan]})
# print(df['score'] + 1) # 결측치에 연산을 해도 결측치가 나옴

# 결측치 확인
# print(pd.isna(df))
# print(pd.isna(df).sum()) # 합계

# 결측치 제거
## 1. 결측치 제거하는 행 제거
# print(df.dropna(subset='score'))

## 2. 여러 변수에 결측치 없는 데이터 추출
df_nomiss = df.dropna(subset=['score', 'sex'])
# print(df_nomiss)

## 3. 결측치가 하나라도 있으면 제거
### df.dropna() -> 아무 변수도 지정하지 않음, 간편하지만 분석에 사용할 수 있는 데이터까지 제거 가능성 있음
df_nomiss2 = df.dropna()
# print(df_nomiss2)
''' 분석에 사용할 변수 직접 지정하여 결측치 제거하는 과정을 권장 -> 데이터 손실이 적어짐 '''

## 4. 결측치 대체
### 결측치가 적고 데이터가 크면 결측치 제거 후 분석 가능
### 데이터가 적고 결측치가 많으면 데이터 손실로 인한 분석 결과 왜곡 발생
### 결측치 대체법을 이용하면 보완이 가능

'''
결측치 대체법 : 결측치를 제거하는 대신 다른 값을 채워넣는 방법
    - 대표값 (평균값, 최빈값) 을 구해서 일괄 대체
    - 통계 분석 기법으로 결측치의 예측값 추정 후 대체 
'''
## 평균값으로 대체
exam = pd.read_csv(path+'exam.csv')
exam.loc[[2, 7, 14], ['math']] = np.nan

### 수학 평균
# print(exam['math'].mean())

### 결측치 -> 평균 값
exam['math'] = exam['math'].fillna(55)
# print(exam)

### 결측치 빈도 확인
a = exam['math'].isna().sum()
# print(a) # 결과값 0 -> 결측치 없음

'''
이상치 제거법 
    1. 존재할 수 없는 값: 논리적으로 존재할 수 없는 값이 있을 경우 결측치로 변환 후 제거
        ex) 성별 변수에 1(남),2(여), 3이 있다면 NaN
    2. 극단치 (Outliner) : 논리적으로 존재할 수 잇지만 극단적으로 너무 크거나 작은 값
        - 극단치가 있으면 분석 결과를 왜곡하므로 제거 후 분석해야 함
        - 기준 정하기    
            1. 논리적 판단 (ex: 성인 몸무게 40 ~ 150kg를 벗어나는 것은 드문 경우이므로 극단치로 간주) 
            2. 통계적 기준 (ex: 상하위 0.3% 또는 +-3 표준편차 벗어나면 극단치로 간주)
            3. 상자 그림을 이용해 중심에서 크게 벗어난 값을 극단치로 간주
'''

df = pd.DataFrame({'sex' : [1,2,1,3,2,1],
                   'score' : [5,4,3,2,6,4]})
# print(df)

##  1. 존재할 수 없는 값
## 이상치 확인 - 빈도표를 만들어 존재할 수 없는 값이 있는지 확인
a = df['sex'].value_counts(sort=False).sort_index()
# print(a)
b = df['score'].value_counts(sort=False).sort_index()
# print(b)

## 결측 처리하기 - 이상치일 경우 NaN 부여
df['sex'] = np.where(df['sex'] == 3, np.nan, df['sex'])
# print(df)

df['score'] = np.where(df['score'] > 5, np.nan, df['score'])
# print(df)

## 결측치 제거 후 분석
a = df.dropna(subset=['sex', 'score'])\
    .groupby('sex')\
    .agg(mean_score = ('score', 'mean'))
# print(a)

## 2. 극단적인 값
### 1) Box-plot으로 기준 정하기
mpg = pd.read_csv(path + 'mpg.csv')

# sns.boxplot(data = mpg, y = 'hwy') # 고속도로의 연비에 대한 boxplot
# plt.show()
'''
박스(IQR): Q1~Q3 구간, 전체 데이터의 중간 50% 포함
중앙값: 박스 안의 굵은 선, 50번째 백분위수
수염: Q1/Q3에서 IQR×1.5 이내의 최솟/최댓값까지
이상치: 수염 바깥에 찍히는 동그라미, 제거 기준으로 많이 씀
'''
## 극단치 기준값 구하기
### 1. 1사분위수 3사분위수 구하기
pct25 = mpg['hwy'].quantile(.25)
pct75 = mpg['hwy'].quantile(.75)
# print(pct25, pct75) # 결과값 : 18.0, 27.0

### 2. IQR 구하기
iqr = pct75 - pct25
# print(iqr) # 결과값: 9.0

### 3. 상한 , 하한 구하기
min = pct25 - 1.5*iqr
max = pct75 + 1.5*iqr
# print(min, max) # 결과값: 4.5 , 40.5 -> 이 값을 넘어가면 이상치

### 4. 극단치 결측 처리
mpg['hwy'] = np.where((mpg['hwy'] < 4.5) | (mpg['hwy'] > 40.5), np.nan, mpg['hwy'])

### 5. 결측치 빈도 확인
# print(mpg['hwy'].isna().sum())

### 6. 결측치 제거 후 분석
a = mpg.dropna(subset = ['hwy'])\
    .groupby('drv')\
    .agg(mean_hwy= ('hwy', 'mean'))
# print(a)

# ================================================================
'''
시각화 : 주제와 경향성이 드러나 데이터의 특징을 쉽게 이해할 수 있게 도움
    - 새로운 패턴 발견, 데이터의 특징을 잘 전더ㅏㄹ
    - 종류 
        1. 2차원 그래프, 3차원 그래프
        2. 지도 그래프
        3. 네트워크 그래프
        4. 모션 차트
        5. 인터렉티브 그래프

seaborn 패키지 : 그래프를 만들 때 자주 사용되는 패키지
    -> matplotlib보다 코드가 쉽고 간결
'''

## 1. 산점도 (Scatter Plot) : 데이터를 x축과 y축에 점으로 표현한 그래프
### 나이와 소득처럼 연속값으로 된 두 변수의 관계를 표현할 때 사용

mpg = pd.read_csv(path + 'mpg.csv')
### x축은 대기량 , y축은 고속도로 연비를 나타내는 산점도 생성
# sns.scatterplot(data=mpg, x = 'displ', y = 'hwy')
# plt.show()

## 축 범위 설정
# sns.scatterplot(data=mpg, x = 'displ', y='hwy')\
    # .set(xlim = [3, 6])
# plt.show()

### x축 범위 3-6 , y축 범위 10 - 30
# sns.scatterplot(data=mpg, x='displ', y='hwy')\
#     .set(xlim = [3, 6], ylim= [10,30])
# plt.show()

## 종류별로 표시 색 바꾸기
### drv별로 표시
# sns.scatterplot(data=mpg, x='displ', y='hwy', hue='drv')
# plt.show()

'''
막대 그래프 (Bar Chart) : 데이터의 크기를 막대의 길이로 표현
    - 성별, 소득 차이처럼 집단 간 차이를 표현할 때 사용
        1. 평균 막대 그래프
        2. 빈도 막대 그래프
'''
## 평균 막대 그래프
# ### 1. 집단별 평균표 생성  - drv 별 hwy
# df_mpg = mpg.groupby('drv')\
#     .agg(mean_hwy = ('hwy', 'mean'))
# print(df_mpg)
'''
as_index = False : 변수를 인덱스로 바꾸지 않고 원래대로 유지
- 위 코드의 출력 결과를 보면 집단을 나타낸 변수 drv가 인덱스로 바뀌어서 mean_hwy보다 아래에 위치
- seaborn으로 그래프를 만들려면 값이 변수에 담겨있어야 함
# '''
# df_mpg = mpg.groupby('drv', as_index = False)\
#     .agg(mean_hwy=('hwy','mean'))
# # print(df_mpg)

## 2. 그래프 생성
# sns.barplot(data=df_mpg, x = 'drv', y='mean_hwy')
# plt.show()

## 3. 크기순 정렬
### 데이터 프레임 정렬
# df_mpg = df_mpg.sort_values('mean_hwy', ascending=False)

## 막대그래프
# sns.boxplot(data=df_mpg, x='drv', y='mean_hwy')
# plt.show()

## 빈도 막대 그래프
### 값의 빈도 (개수)를 막대 길이로 표현
### 여러 집단의 빈도를 비교할 때 사용

## 1. 집단별 빈도표 만들기
# df_mpg = mpg.groupby('drv', as_index=False)\
#     .agg(n = ('drv', 'count'))
# print(df_mpg)

## 2. 그래프 만들기
# sns.barplot(data=df_mpg, x='drv', y='n')
# plt.show()

### 빈도그래프는 원자료에서 갯수만 세면 되기 때문에 countplot 사용 -> 집단별 빈도표 만드는 작업이 필요 없음
# sns.countplot(data=mpg, x= 'drv') # 빈도 기준 정렬됨
# plt.show()

### 막대 정렬 -> 4, f, r순으로
# sns.countplot(data=mpg, x='drv', order=['4','f','r'])
# plt.show()

'''
선 그래프 (Line Chart) : 데이터를 선으로 표현한 그래프
    - 시간에 따라 달라지는 데이터 표현할 때 사용 ( ex: 환율, 주가지수 등 경제지표가 시간에 따라 달라지는 양상)
    - 시계열 데이터 (Time Series Data) : 일별 환율처럼, 일정 시간 간격을 두고 나열된 데이터
    - 시계열 그래프 : 시계열 데이터를 선으로 표현한 그래프
'''
## 1. 데이터 로드
economics = pd.read_csv(path + 'economics.csv')
# print(economics.head())

# sns.lineplot(data=economics, x='date', y='unemploy')
# plt.show()

## x축에 연도 표시
### 1.
economics['date2'] = pd.to_datetime(economics['date'])
# print(economics.info()) # 날짜 타입 변수가 생성되었는지 확인
# print(economics[['date', 'date2']])

## 연도만 추출
y = economics['date2'].dt.year
# print(y)

## 월만 추출
y = economics['date2'].dt.month
# print(y)

## 일만 추출
y = economics['date2'].dt.day
# print(y)

# 5. 연도 변수 추가
economics['year'] = economics['date2'].dt.year

# 6. x축에 연도만 추가
sns.lineplot(data=economics, x='year', y='unemploy')
# plt.show()

# 7. 신뢰구간 제거
sns.lineplot(data=economics, x='year', y='unemploy', errorbar=None)
# plt.show()

'''
상자 그림 (box plot) : 데이터의 분포 또는 퍼져있는 형태를 직사각형 상자 모형으로 표현한 그래프 
 - 데이터가 어떻게 분포하는지 알 수 있고
 - 평균값만 볼 때보다 데이터의 특징을 더 자세히 알 수 있음
 
'''
sns.boxplot(data=mpg, x='drv', y='hwy')
plt.show()