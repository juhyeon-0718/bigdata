import pandas as pd

df = pd.DataFrame({'name' : ['김지훈', '이유진','박동현','김민지'],
                   'english': [90, 80, 70, 60],
                   'math': [50, 60, 70, 80]}) #dic 구조

# print(df)

## 특정 변수의 값 추출
# print(df['english']) # key값 입력

## 변수의 값으로 합계 구하기
# a = sum(df['english'])
# print(a)
#
# b = sum(df['math'])
# print(b)
#
# # 변수의 값으로 평균 구하기
# c = sum(df['english']) / len(df['english'])
# print(c)

## 외부 데이터 이용하기
### 엑셀 파일 이용
path = 'C:/JJH_bigdata/Data/'
df_exam = pd.read_excel(path + 'excel_exam.xlsx') # 문자열의 덧셈은 문자열을 이어줌
# print(df_exam)

### 분석
english_average = sum(df_exam['english']) / len(df_exam['english'])
# print(english_average)

math_average = sum(df_exam['math']) / len(df_exam['math'])
# print(math_average)

### 첫 번째 행이 변수명이 아니라면
# df_exam_no = pd.read_excel(path + 'excel_exam_novar.xlsx')
df_exam_no = pd.read_excel(path + 'excel_exam_novar.xlsx', header=None)
# print(df_exam_no)

### 시트가 여러개라면 ?
# Sheet2 에서 데이터 불러오기
# df_exam = pd.read_excel(path + 'excel_exam_novar.xlsx', sheet_name='Sheet1')

## CSV 파일 불러오기
'''
    CSV: 모든 값들이 줄바꿈과 수미표로 구분되어 있음
        - 모든 프로그램에서 동작
        - 용량이 작음 
'''

csv_exam = pd.read_csv(path + 'exam.csv')
# print(csv_exam)

### 예제
df_midterm = pd.DataFrame({'english': [90, 80, 70, 60],
                           'math': [50, 60, 70, 80],
                           'nclass' : [1, 1, 2, 2]})

# print(df_midterm)

### 저장하기
# df_midterm.to_csv(path + '전송용.csv')

### 데이터 분석 기초
