import matplotlib.pyplot as plt
import seaborn

# var = ['a', 'a', 'b', 'c', 'd', 'd', 'd']
# print(var)
#
# seaborn.countplot(x = var)
# plt.show() # 그래프 출력 함수
# sns.countplot(x = var)
# plt.show()

import seaborn as sns

### seaborn의 titanic
df = sns.load_dataset('titanic')
# print(df)

# sns.countplot(data=df, x='sex')
# plt.show()
#
# sns.countplot(data=df, x='class')
# plt.show()

# sns.countplot(data=df, x='class', hue='alive')
# plt.show()

# sns.countplot(data=df, y='class', hue='alive')
# plt.show()

#===================================
### 모듈

# import sklearn.metrics
# sklearn.metrics.accuracy_score()
#
# #'모둘명.함수명()'으로 함수 사용
# from sklearn import metrics
# metrics.accuracy_score()
#
# # '함수명()'으로 함수 사용
# from sklearn.metrics import accuracy_score
# accuracy_score

# ========================================
import pydataset
# print(pydataset.data())

### 패키지 함수 사용
df = pydataset.data('mtcars')
# print(df)
