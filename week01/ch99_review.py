import pandas as pd

path = 'C:/JJH_bigdata/Data/'

mpg = pd.read_csv(path + 'midwest.csv')
# print(mpg.info())
# print(mpg)

## 2
mpg_new = mpg.rename(columns={'poptotal' : 'total', 'popasian': 'asian'})
# print(mpg_new.info())

## 3
mpg_new['percent'] = mpg_new['asian'] / mpg_new['total']
count_test = mpg_new['percent']
his = count_test.hist()
print(his)