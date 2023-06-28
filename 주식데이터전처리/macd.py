import pandas as pd
import numpy as np
import Stock_Info_Crawling

def calculate_macd(data, short_period=12, long_period=26, signal_period=9):
    # 단기 이동평균 계산
    short_ema = data.ewm(span=short_period, adjust=False).mean()

    # 장기 이동평균 계산
    long_ema = data.ewm(span=long_period, adjust=False).mean()

    # MACD Line 계산
    macd_line = short_ema - long_ema

    # Signal Line 계산
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()

    # MACD Histogram 계산
    macd_histogram = macd_line - signal_line

    return macd_line, signal_line, macd_histogram

def create_macd_data(stock_name):
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)
    price_data = pd.Series(df['Close'])

    # MACD 계산
    macd, signal, histogram = calculate_macd(price_data)

    # 데이터프레임 생성
    df_macd = pd.DataFrame({'macd': macd, 'signal': signal, 'histogram': histogram})

    # CSV 파일로 저장
    df_macd.to_csv(f'{stock_name}_macd.csv', index=False)

def main():
    stock_name = input("macd 정보를 추가할 주식 이름을 입력해주세요: ")
    create_macd_data(stock_name)

if __name__=="__main__":
    main()