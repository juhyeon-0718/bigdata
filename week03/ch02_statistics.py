""" 통계 분석 기법 이용한 가설 검정  """
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

path = 'C:/Python_Data/Data/'

'''
    기술 통계 : 데이터를 요약해서 설명하는 통계 분석 기법
    추론 통계 : 어떤 값이 발생할 확률을 계산하는 통계 분석 기법
     ex) 성별에 따른 월급 차이가 우연히 발생할 확률 계산
     1. 이런 차가 우연히 나타날 확률이 작다 
        -> 성별에 따른 월급 차이가 통계적으로 유의미함
     2. 이런 차가 우연히 나타날 확률이 작다
        -> 성별에 따른 월급 차이가 통계적으로 유의미하지 않음
        
    - 기술 통계 분석에서 집단 간 차이가 있는 것으로 나타났더라도 이는 우연에 의한 차이일 수 있음
    - 신뢰할 수 있는 결론을 내리려면 유의확률로 게산하는 통계적 가설 검정 절차 필요 
    
    통계적 가설 검정 : 유의확률을 사용해서 가설을 검정하는 방법
        - 유의확률 (p-value) : 실제로는 차이가 없지만 우연히 차이가 있는 데이터가 추출되는 확률
        
        1. 유의확률이 크다 : 
            -> 집단 간 차이가 통계적으로 유의하지 않다
            -> 실제로 차이가 없는데 우연에 의해 이런 정도의 차이가 관찰될 가능성이 크다
            
        2. 유의확률이 작다 :
            -> 집단 간 차이가 통계적으로 유의하다
            -> 실제로 차이가 없는데 우연히 이런 정도의 차이가 관찰될 가능성이 작다
'''

''' 
 T 검정 (T-test) : 두 집단의 평균에 통계적으로 유의한 차이가 있는지 알아볼 때 사용하는 분석 기법
'''
# mpg 데이터 내에서 compact 최대치와 suv 자동차의 도시 연비 t검정

mpg = pd.read_csv(path + 'mpg.csv')

a = mpg.query('category in ["compact", "suv"]')\
     .groupby('category', as_index=False)\
     .agg(n=('category','count'),
          mean = ('cty','mean'))

# print(a)
'''
  category   n      mean
0  compact  47  20.12766
1      suv  62  13.50000
'''

''' 
비교하는 집단의 등분산 여부에 따라 적용하는 공식이 다름
    equal_var = True : 두 집단 간의 분산이 같다
    
'''
compact = mpg.query('category == "compact"')['cty']
suv = mpg.query('category == "suv"')['cty']

# t-test
t = stats.ttest_ind(compact, suv, equal_var = True)
# print(t)
'''
     TtestResult(statistic=np.float64(11.917282584324107), 
     pvalue=np.float64(2.3909550904711282e-21), 
          -> 유의확률이 0.05보다 작으므로 compact와 suv 간의 도시연비 차이는 통계적으로 유의하다
     df=np.float64(107.0))
'''


### 일반 휘발유와 고급 휘발유의 도시 연비 t검정
# 1. 기술 통계
a = mpg.query('fl in ["r", "p"]')\
     .groupby('fl', as_index=False)\
     .agg(n=('category','count'),
          mean = ('cty','mean'))
# print(a)
'''
  fl    n       mean
0  p   52  17.365385
1  r  168  16.738095
'''

# 2. t검증\
regular = mpg.query('fl == "r"')['cty']
premium = mpg.query('fl == "p"')['cty']

t = stats.ttest_ind(regular, premium, equal_var = True)
# print(t)
'''
결과 해석 

TtestResult(statistic=np.float64(-1.066182514588919), 
pvalue=np.float64(0.28752051088667036), 
     -> p-value가 0.05보다 크므로 일반 휘발유와 고급 휘발유 간의 차이는 통계적으로 유의하지 않다. 
df=np.float64(218.0))
'''

'''
     상관분석 : 두 연속 변수가 서로 관련이 있는지 검정하는 통계 분석 기법
          - 상관계수 : 두 변수가 얼마나 관련되어 있는지 정도를 파악 가능
               - -1 ~ 1의 값을 가지며 1에 가까울 수록 관련성이 크다
               - 양수면 정비례, 음수면 반비례 
'''

### 실업자 수와 개인 소비 지출 간의 상관관계 분석
# economics = pd.read_csv(path + 'economics.csv')
#
# # 1. 상관행렬 만들기 : corr
# c = economics[['unemploy', 'pce']].corr()
# # print(c)
#
# stats.pearsonr(economics['unemploy'], economics['pce'])
'''
출력 결과의 첫 번째 값이 상관계수, 두 번째 값이 유의확률
     -> 유의확률이 0.05미만이므로 실업자 수와 개인 소비 지출의 상관관계가 통계적으로 유의하다
     
'''
### 상관행렬 히트맵

''' 
상관행렬 : 모든 변수의 상관관계를 나타낸 행렬
     - 여러 변수이 관련성을 한꺼번에 알아보고 싶을 때 사용
     - 어떤 변수끼리 관련이 크고 작은지 한 눈에 파악 가능
'''
# 1. 상관 행렬 만들기
mtcars = pd.read_csv(path + 'mtcars.csv')
# print(mtcars.head())

car_cor = mtcars.corr()
car_cor = round(car_cor, 2)
# print(car_cor)
'''
결과값
       mpg   cyl  disp    hp  drat    wt  qsec    vs    am  gear  carb
mpg   1.00 -0.85 -0.85 -0.78  0.68 -0.87  0.42  0.66  0.60  0.48 -0.55
cyl  -0.85  1.00  0.90  0.83 -0.70  0.78 -0.59 -0.81 -0.52 -0.49  0.53
disp -0.85  0.90  1.00  0.79 -0.71  0.89 -0.43 -0.71 -0.59 -0.56  0.39
hp   -0.78  0.83  0.79  1.00 -0.45  0.66 -0.71 -0.72 -0.24 -0.13  0.75
drat  0.68 -0.70 -0.71 -0.45  1.00 -0.71  0.09  0.44  0.71  0.70 -0.09
wt   -0.87  0.78  0.89  0.66 -0.71  1.00 -0.17 -0.55 -0.69 -0.58  0.43
qsec  0.42 -0.59 -0.43 -0.71  0.09 -0.17  1.00  0.74 -0.23 -0.21 -0.66
vs    0.66 -0.81 -0.71 -0.72  0.44 -0.55  0.74  1.00  0.17  0.21 -0.57
am    0.60 -0.52 -0.59 -0.24  0.71 -0.69 -0.23  0.17  1.00  0.79  0.06
gear  0.48 -0.49 -0.56 -0.13  0.70 -0.58 -0.21  0.21  0.79  1.00  0.27
carb -0.55  0.53  0.39  0.75 -0.09  0.43 -0.66 -0.57  0.06  0.27  1.00

ex) 
[ 해석 ]  실린더 수가 많을수록 연비가 떨어짐
'''

# 2. 히트맵 생성
'''
     값의 크기를 색깔로 표현한 표를 만들면 변수들 간의 관계 쉽게 파악 가능
'''
plt.rcParams.update({'figure.dpi' : '120',  # 해상도
                    'figure.figsize' : [7.5, 5.5]}) # 가로 세로 크기 지정

# sns.heatmap(car_cor,
#             annot = True, #상관계수 표시
#             cmap = 'RdBu') # 컬러맵

plt.show()
'''
상관계수가 필수로 상자 색깔을 진하게 표현
상관계수가 양수면 파란색, 음수면 빨간색 계열로 표현
상자 색을 보면 상관관계의 정도와 방향을 쉽게 파악 가능
'''

# 3. 대각 행렬 제거
''' 
히트맵을 대각선 기죽으로 왼쪽 아래와 오른쪽 위의 값이 대칭하여 중복
mask를 이용해 중복된 부분 제거 
'''

## 3-1. mask 만들기
mask = np.zeros_like(car_cor)
# print(mask)
'''
[[0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.]]
 '''

mask[np.triu_indices_from(mask)] = 1
# print(mask)
'''
[[1. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
 [0. 1. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
 [0. 0. 1. 1. 1. 1. 1. 1. 1. 1. 1.]
 [0. 0. 0. 1. 1. 1. 1. 1. 1. 1. 1.]
 [0. 0. 0. 0. 1. 1. 1. 1. 1. 1. 1.]
 [0. 0. 0. 0. 0. 1. 1. 1. 1. 1. 1.]
 [0. 0. 0. 0. 0. 0. 1. 1. 1. 1. 1.]
 [0. 0. 0. 0. 0. 0. 0. 1. 1. 1. 1.]
 [0. 0. 0. 0. 0. 0. 0. 0. 1. 1. 1.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 1. 1.]
 [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 1.]]
 '''
# mask의 1에 해당하는 위치값이 적용되어
# sns.heatmap(data =car_cor ,
#             annot=True,
#             cmap="RdBu",
#             mask=mask)
# # plt.show()

# 3-4. 빈 행과 열 제거
mask_new = mask[1:, : -1]
cor_new = car_cor.iloc[1:, :-1]

# sns.heatmap(data=cor_new,
#             annot=True,
#             cmap="RdBu",
#             mask=mask_new)
# plt.show()

# # 4. heat map 의 여러 옵션
# sns.heatmap(data =cor_new, #
#             annot=True, # 상관계수 표시
#             cmap="RdBu", #컬러맵
#             mask=mask_new,  #mask 적용
#             linewidths= .5, # 경계 구분선
#             vmax=1, # 가장 진한 파란색으로 표현할 최댓값
#             vmin=-1, # 가장 진한 빨간색으로 표현할 최솟값
#             cbar_kws={"shrink": .5}) # 범례 크기 줄이기
#
# plt.show()