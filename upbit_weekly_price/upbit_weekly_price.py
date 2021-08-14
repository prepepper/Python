# 업비트 모듈 설치
!pip install pyupbit

# 모듈 불러오기
import pyupbit
import datetime
from pandas import DataFrame

# 종목 설정
ticker = "KRW-BTC"

# BTC 전체 데이터 가져오기
coindata = pyupbit.get_ohlcv(ticker, interval="day", count=200)

# 시간, 종가 가져오기
coindata = coindata.reset_index()
coindata['Date'] = coindata['index']
coindata['Price'] = coindata['close']
coindata = coindata[['Date','Price']]

df = DataFrame(coindata)

filter = df['Date'] >= '2021-01-01'                 # 필터 내용
filtered_df = df.loc[filter]        

                # 필터 적용
filtered_df = filtered_df.reset_index(drop=True)    # 초기화

filtered_price = filtered_df["Price"]
filtered_date = filtered_df["Date"]

priceList = filtered_price.tolist()
dateList = filtered_date.tolist()

# 사용 변수 초기화
pstrList = []
index = -1
first = 0
second = 0

for price in priceList:  
  index += 1
    
  if index == 0:
    # 초기화    
    first = price
    second = price    
  elif index % 7 == 0:
    first = second
    second = price    

    # 변화 비율
    rate = ((second / first) - 1) * 100
    rate = round(rate, 2)

    # 변화 가격
    diff = second - first
    diff = round(diff)

    pstr = " 가격변동: " + str(diff) + " KRW / " + str(rate) + "%"    

    pstrList.append(pstr)


dstrList = []
first = 0
second = 0
lastMonth = 1
weekinMonth = 0

for dt in dateList:
  index += 1  
    
  if index == 0:    
    # 초기화    
    first = dt.day
    second = dt.day
  elif index % 7 == 0:
    
    if dt.month == lastMonth:
      weekinMonth += 1
    else:
      weekinMonth = 1
      lastMonth += 1
    
    first = second
    second = dt.day

    dstr =  str(dt.month) + "월 " + str(weekinMonth) + "주차 " + ticker + " (" + str(dt.month) + "." + str(first) + "~" + month + "." + str(second) + " 오전 9시 기준)"    
    dstrList.append(dstr)    


result = DataFrame([x for x in zip(dstrList, pstrList)])
result.columns = ['날짜', '변동내역']

# 엑셀 저장
result.to_excel('result_data.xlsx', index=False, encoding='cp949')