import pandas as pd
from distributed import sizeof

path = 'C:/JJH_bigdata/Data/'

''' 
Method Chaining 
    : `.`을 이용하여 계속 이어서 작성하는 방법
    - 변수에 여러 메서드를 왼쪽부터 순서대로 적용
    - 출력 결과를 변수에 할당하고 다시 불러오는 작업 반복하지 않아도 됨 
'''

mpg = pd.read_csv(path + 'mpg.csv')
# df = mpg['grade']
# df = df.value_counts() # 빈도표
# df = df.sort_index()

# Method Chaining 적용
# df = mpg['grade'].value_counts().sort_index()
# print(df)

### 목록에 해당하는 행으로 변수 만들기 - 파생변수
import numpy as np
### 조건문 형식 : np.where(조건문, 부합할 때, 부합하지 않을 때)
mpg['size'] = np.where(( mpg['category'] == 'compact' ) |
                       ( mpg['category'] == 'subcompact' ) |
                       ( mpg['category'] == '2seater' ), 'small', 'large')
a = mpg['size'].value_counts()
print(a) # 결과값 : large 147, small 87

### df.isin() 사용하기
b = ['compact', 'subcompact','2seater']
mpg['size'] = np.where(mpg['category'].isin(b), 'small', 'large' )
print(mpg['size'].value_counts()) # 결과값 : large 147, small 87
