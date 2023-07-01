import pandas as pd
import numpy as np
import Stock_Info_Crawling


def calculate_bollinger_bands(data, period=20, num_std=2):
    # 이동평균 계산
    ma = data.rolling(window=period).mean()
    # 표준편차 계산
    std = data.rolling(window=period).std()
    # 상단 볼린저 밴드 계산
    upper_band = ma + (num_std * std)
    # 하단 볼린저 밴드 계산
    lower_band = ma - (num_std * std)

    return upper_band, lower_band

def create_basic_bollinger_bands(stock_name):
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)
    price_data = pd.Series(df['Close'])
    date_data = pd.Series(df['Date'])

    # 볼린저 밴드 계산
    upper_band, lower_band = calculate_bollinger_bands(price_data)

    # 데이터프레임 생성
    df = pd.DataFrame()
    df['Date'] = date_data
    df['Close'] = price_data
    df['Upper_Band'] = upper_band
    df['Lower_Band'] = lower_band

    # CSV 파일로 저장
    df.to_csv(f'{stock_name}_bollinger.csv', index=False)

    return

def create_bollinger_bands(stock_name, period, num_std):
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)
    price_data = pd.Series(df['Close'])

    # 볼린저 밴드 계산
    upper_band, lower_band = calculate_bollinger_bands(price_data, period, num_std)

    try:
        bollinger_csv = pd.read_csv(f'{stock_name}_bollinger.csv')
    except:
        create_basic_bollinger_bands(stock_name)
        bollinger_csv = pd.read_csv(f'{stock_name}_bollinger.csv')

    bollinger_csv[f'upper_band_{period:03d}_{num_std}'] = upper_band
    bollinger_csv[f'lower_band_{period:03d}_{num_std}'] = lower_band

    bollinger_csv.to_csv(f'{stock_name}_bollinger.csv', index=False)

    return

def main():
    stock_name = input("볼린저밴드 csv 파일을 생성할 주식 이름을 입력해주세요: ").strip()
    create_basic_bollinger_bands(stock_name)

if __name__=="__main__":
    main()
