import pyupbit
import numpy as np


def get_ror(k=0.5):
    df = pyupbit.get_ohlcv("KRW-BTC", count=7)  # ex) count=7  7일간 데이터 가져오기
    df['range'] = (df['high'] - df['low']) * k
    df['target'] = df['open'] + df['range'].shift(1)

    # 수수료까지 계산
    # fee = 0.0032
    # df['ror'] = np.where(df['high'] > df['target'],
    #                      df['close'] / df['target'] - fee,
    #                      1)
    
    # 수수료 미포함 k값 구하기
    df['ror'] = np.where(df['high'] > df['target'],
                         df['close'] / df['target'],
                         1)

    ror = df['ror'].cumprod()[-2]
    return ror


for k in np.arange(0.1, 1.0, 0.1):
    ror = get_ror(k)
    print("%.1f %f" % (k, ror))
