import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


path = 'C:/Python_Data/Data/'

raw_welfare = pd.read_spss(path + 'Koweps_hpwc14_2019_beta2.sav')
welfare = raw_welfare.copy()

welfare = welfare.rename(columns={
    'h14_g3'    : 'sex',
    'h14_g4'    : 'birth',
    'h14_g11'   : 'religion',
    'p1402_8aq1': 'income',
    'h14_eco9'  : 'code_job',
    'h14_reg7'  : 'code_region',
    'h14_g10' : 'marriage_type'
})

''' 성별에 따른 월급 차이 '''

''' 
데이터 분석 절차
    1단계 : 변수 검토 및 전처리
        => 분석에 활용할 변수를 각각 전처리 : 변수 특징 파악, 이상치와 결측치 정제
        => 변수의 값을 다루기 편하게 바뀍
    2단계 : 변수 간 관계 분석
        -> 데이터 요약표, 그래프 (시각화)
        -> 분석 결과 해석 **
    
'''

## 1. 성별 변수 검토 및 전처리
### 1) 변수 검토
# print(welfare['sex'].dtypes) # 결과값 float64
# print(welfare['sex'].value_counts()) # 2.0 7913 ,  1.0    6505 -> 이상치 확인

### 2) 성별 항목에 이름 부여
welfare['sex'] = np.where(welfare['sex'] == 1, 'male', 'female')
# print(welfare['sex'].value_counts()) ### sex female    7913 male      6505
# sns.countplot(data=welfare, x= 'sex')
# plt.show()

## 2. 월급 변수 검토 및 전처리
### 1) 변수 검토
# print(welfare['income'].dtypes) # 결과값 : float
# print(welfare['income'].describe())
# sns.histplot(data=welfare, x ='income')
# plt.show()

### 2) 전처리
# print(welfare['income'].describe()) # 이상치 확인
# print(welfare['income'].isna().sum()) # 결과값: 9884

## 3. 성별에 따른 월급 차이 분석
### 1) 성별 월급 평균표 만들기
sex_income = welfare.dropna(subset='income')\
    .groupby('sex', as_index=False)\
    .agg(mean_income =  ('income', 'mean'))

# print(sex_income)

## 3. 그래프 시각화
# sns.barplot(data = sex_income, x = 'sex', y='mean_income', hue='sex')
# plt.show()

'''
나이와 월급의 관계 - 몇 살에 월급을 가장 많이 받을까
'''
## 1. 나이 변수 검토 및 전처리
### 1) 변수 검토
# print(welfare['birth'].dtypes) # float64
# print(welfare['birth'].describe()) # 1900~2019 이외의 값 -> 없음 (최소 1907, 최대 2018)
# sns.histplot(data=welfare, x='birth')
# plt.show()


### 2) 전처리 - 나이
# print(welfare['birth'].isna().sum()) # 결과값 0

### 3) 파생변수 -> 나이 생성
welfare = welfare.assign(
    age = 2019 - welfare['birth'] + 1
)

# print(welfare['age'].describe())

## 2. 관계 분석
### 1. 나이에 따른 월급 평균표 만들기
age_income = welfare.dropna(subset = 'income')\
    .groupby('age')\
    .agg(mean_income = ('income', 'mean'))
# print(age_income.head())

## 3. 시각화
# sns.lineplot(data = age_income, x = 'age', y = 'mean_income')
# plt.show()

## 4. 해석
''' 
40대 후반에서 50대 초반에 가장 많은 월급을 받는다 
20대부터 월급이 점차 올며 60대쯤에는 20대보다 낮은 월급을 받는다
'''

''' 
    연령대에 따른 월급 차이 = 어떤 연령대의 월급이 가장 많을까
        30살 미만: 초년층
        30 - 59 : 중년층
        60세 이상 : 장년층      
'''

# 1. 나이 변수 살펴보기
# print(welfare['age'].head())

# 2. 연령대 변수 생성
welfare = welfare.assign(ageg = np.where(welfare['age'] < 30, 'young',
                                         np.where(welfare['age'] <= 59, 'middle', 'old')))

# 3. 빈도 확인
# print(welfare['ageg'].value_counts())

# 4. 빈도 막대 그래프 생성
# sns.countplot(data = welfare, x='ageg')
# plt.show()

# 연령대에 다른 월급 차이 분석
ageg_income = welfare.dropna(subset='income')\
    .groupby('ageg', as_index=False)\
    .agg(mean_income = ('income', 'mean'))

# sns.barplot(data=ageg_income, x='ageg', y='mean_income')
# plt.show()

# sns.barplot(data=ageg_income, x='ageg', y='mean_income',
#             order=['young', 'middle', 'old'])
# plt.show()

''' 연령대 및 성별 월급 차이 -  성별 월급 차이에는 연령대별로 어떨까'''
### 연령대 및 성별 월급 평균표 생성
sex_income = welfare.dropna(subset='income')\
    .groupby(['ageg', 'sex'], as_index = False)\
    .agg(mean_income = ('income', 'mean'))

# print(sex_income)

## 시각화
# sns.barplot(data = sex_income, x = 'ageg', y = 'mean_income',hue = 'sex',
#             order=['young', 'middle', 'old'])
# plt.show()

## 해석
''' 초년층에는 차이가 크게 나지 않고 중년층에서부터 차이가 많이남 '''

''' 나이 및 성별 월급 차이 분석  '''
### 1. 나이 및 성별 월급 평균표
### 2. 시각화 (선그래프)
sex_income = welfare.dropna(subset='income')\
    .groupby(['age', 'sex'], as_index = False)\
    .agg(mean_income = ('income', 'mean'))
# print(sex_income)

# sns.lineplot(data = sex_income, x = 'age', y  = 'mean_income', hue = 'sex')
# plt.show()

''' 직업별 월급 차이 : 어떤 직업이 월급을 가장 많이 받았을까 '''
### 작업 변수 검토 및 전처리
# 1. 변수 검토
# print(welfare['code_job'].dtypes) # float
# print(welfare['code_job'].value_counts()) # code_job 611.0(작물재배)   962

# 2. 전처리 - 매칭
list_job = pd.read_excel(path + 'Koweps_Codebook_2019.xlsx', sheet_name='직종코드')
# print(list_job.head()) #  111  의회 의원∙고위 공무원 및 공공단체 임원

# 3. merge
welfare = welfare.merge(list_job, how='left', on='code_job')

# code_job  결측치 제거하고 code-job , job 변수 출력
a = welfare.dropna(subset=['code_job'])[['code_job', 'job']].head()
# print(a)


# 직업별 월급 차이 붅석
##1. 직업별 월급 평균표 생성
job_income = welfare.dropna(subset=['job', 'income'])\
    .groupby('job', as_index = False)\
    .agg(mean_income = ('income','mean'))

# print(job_income.head())

## 2. 월급이 많은 직업 상위 10개
top10 = job_income.sort_values('mean_income', ascending = False).head(10)
# print(top10) # 결과값 :  의료 진료 전문가   781.000000

## 3. 시각화
''' 파이썬에서 한글을 그래프에 넣으려면 한글 폰트 지정 필요함 '''
### 맑은 고딕 폰트 설정
import matplotlib.pyplot as plt
plt.rcParams.update({'font.family': 'Malgun Gothic'})

# sns.barplot(data = top10, y = 'job', x = 'mean_income')
# ''' y축을 먼저 작성하면 그래프는 누운 그래프가 됨 (job의 길이가 길기 때문에 현재 적절)'''
# plt.show()

## 4. 월급이 적은 직업 하위 10개
bottom10 = job_income.sort_values('mean_income', ascending=True).head(10)
# print(bottom10)

# sns.barplot(data = bottom10, y = 'job', x = 'mean_income')\
#     .set(xlim = [0, 800]) # 상위 10과 명시적으로 차이를 보여주기 위해 범위 설정
# plt.show()

''' 종교 유무에 따른 이혼율 - 종교가 있다면 이혼을 더 했을까 ? '''
## 데이터 파악
# print(welfare['religion'].dtypes)
# print(welfare['religion'].value_counts())

## 전처리
### 1. 종교 유무에 따른 이름 분리
welfare['religion'] = np.where(welfare['religion'] == 1, 'Yes', 'No')
# print(welfare['religion'].value_counts())\

### 2. 혼인 상태 변수 검토
# print(welfare['marriage_type'].dtypes) # float64
# print(welfare['marriage_type'].describe())

welfare['marriage'] = np.where(welfare['marriage_type'] == 1, 'marriage',
                               np.where(welfare['marriage_type'] == 3, 'divorce', 'etc'))

n_divorce = welfare.groupby('marriage', as_index = False)\
    .agg(n = ('marriage', 'count'))

# print(n_divorce)

## 종교 유무에 따른 이혼율 분석

### 3. 종교 유무에 따른 이혼율표
rel_div = welfare.query('marriage != "etc"')\
    .groupby('religion', as_index=False)\
    ['marriage']\
    .value_counts(normalize = True) # 비율 구하기

# print(rel_div)
'''  결과 
    religion  marriage  proportion
0       No  marriage    0.905045
1       No   divorce    0.094955
2      Yes  marriage    0.920469
3      Yes   divorce    0.079531
'''
### 4. 시각화
rel_div = \
    rel_div.query('marriage == "divorce"')\
    .assign(proportion = rel_div['proportion'] * 100 ) \
    .round(1) # 반올림
# print(rel_div)
''' 결과 

  religion marriage  proportion
1       No  divorce         9.5
3      Yes  divorce         8.0

종교 유무에 따라 이혼율이 1.5정도 차이가 남
-> 표본의 크기가 커질수록 1.5%의 차이는 유의미해질 수 있음

'''

### 5. 막대 그래프 그리기
# sns.barplot(data=rel_div, x='religion', y = 'proportion')
# plt.show()

''' 지역별 연령대 비율 - 어느 지역에 노년층이 많을까 '''
## 1. 변수 검토
# print(welfare['code_region'].dtypes) # float
# print(welfare['code_region'].value_counts())

## 2.
list_region = pd.DataFrame({'code_region' : [1,2,3,4,5,6,7],
                            'region' : ['서울',
                                        '수도권(인천/경기)',
                                        '부산/경남/울산',
                                        '대구/경북',
                                        '대전/충남',
                                        '강원/충북',
                                        '광주/전남/전북,제주도']})

# print(list_region)
'''결과값 
0            1            서울
1            2    수도권(인천/경기)
2            3      부산/경남/울산
3            4         대구/경북
4            5         대전/충남
5            6         강원/충북
6            7  광주/전남/전북,제주도
'''

## 3. 지역명 변수 추가
welfare = welfare.merge(list_region, how='left', on='code_region')
# print(welfare[['code_region','region']].head(20))
'''
    code_region      region
0           1.0          서울
1           1.0          서울
2           1.0          서울
3           1.0          서울
4           1.0          서울
5           1.0          서울
6           1.0          서울
7           1.0          서울
8           2.0  수도권(인천/경기)
9           1.0          서울
'''


### 4. 지역별 연령대 비율 분석
region_ageg = welfare.groupby('region', as_index=False)\
    ['ageg']\
    .value_counts(normalize = True)
# print(region_ageg)

### 5. 데이터 시각화
region_ageg = \
    region_ageg.assign(proportion = region_ageg['proportion'] * 100)\
    .round(1)

# sns.barplot(data=region_ageg, y = 'region', x = 'proportion', hue = 'ageg')
# plt.show()

### 누적 비율 막대 그래프 생성
# 1. pivot
pivot_df = region_ageg[['region', 'ageg','proportion']].pivot(index = 'region',
                                                              columns = 'ageg',
                                                              values = 'proportion')
# print(pivot_df)
'''
ageg          middle   old  young
region                           
강원/충북           30.9  45.9   23.2
광주/전남/전북,제주도    31.8  44.9   23.3
대구/경북           29.6  50.4   20.0
대전/충남           33.6  41.3   25.0
부산/경남/울산        33.4  43.8   22.9
서울              38.5  37.6   23.9
수도권(인천/경기)      38.8  32.5   28.7
'''

# 데이터 시각화
## 2. 가로 막대 그래프
# pivot_df.plot.barh(stacked=True)
# plt.show()
'''좀 더 직관적인 그래프 '''

## 3. 막대 정렬 = 노년층 비율 기준으로 정렬 변수 순서 바꾸기
reorder_df = pivot_df.sort_values('old')[['young', 'middle','old']]
# print(reorder_df)

# reorder_df.plot.barh(stacked=True)
# plt.show()
