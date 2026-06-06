'''
한국 복지 패널 데이터
- 한국 보건 사회 연구언 발간 조사 자료
- 전국 7천여가구 선정, 2006년도 매년 추적 조사 자료
- 경제활동, 생활실태, 복지욕구 등 천여 개 변수로 구성
- 다양한 분야의 연구자, 정책전문가들이 정책반영에 활동
- 엄밀한 절차로 수집, 다양한 변수가 있으므로 데이터 분석 연습에 용이
'''

''' .sav : 통계 분석 소프트웨어 SPSS 전용 파일 '''

# pip install pyreadstat

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

path = 'C:/JJH_bigdata/Data/'
# 1. 패키지 설치 및 로드
# 2. 데이터 불러오기
raw_welfare = pd.read_spss(path + 'Koweps_hpwc14_2019_beta2.sav')

# 3. 복사본 만들기
welfare = raw_welfare.copy()

# 4. 데이터 검토 (파악)
# print(welfare)
# print(welfare.info())
# print(welfare.describe())
'''
규모가 큰 데이터는 변수명을 쉬운 단어로 바꾸고 분석할 변수를 하나씩 살펴야함

코드북에 코드로 된 변수명과 값의 의미가 설명되어 있음
데이터의 특징을 잘 알 수 잇고 분석 방향의 아이디어를 코드북에서 얻을 수 있음
'''
welfare = welfare.rename(columns={'h14_g3' :'sex', # 성별
                                  'h14_g4' : 'birth', # 생년월일
                                  'h13_g10' : 'marriage_type', # 혼인 상태
                                  'h14_g11' : 'religion', # 종교
                                  'h1402_8aq1': 'income', # 월급
                                  'h14_eco9': 'code_job', # 직업 코드
                                  'h13_reg7': 'region'}) # 지역 코드

print(welfare.describe())