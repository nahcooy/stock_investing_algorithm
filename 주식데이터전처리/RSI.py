import pandas as pd
import Stock_Info_Crawling
import talib

def calculate_rsi(df, rsi_period):
    # RSI 계산
    df['RSI'] = talib.RSI(df['Close'], timeperiod=rsi_period)
    return df

def create_RSI(stock_name, rsi_period = 14):
    try:
        # 주어진 CSV 파일 읽기
        df = pd.read_csv(f'{stock_name}_day.csv')
    except:
        Stock_Info_Crawling.save_stock_data_to_csv(stock_name)
        df = pd.read_csv(f'{stock_name}_day.csv')

    # RSI 계산
    df = calculate_rsi(df, rsi_period)

    # 결과를 새로운 CSV 파일로 저장
    df.to_csv(f'{stock_name}_RSI.csv', index=False)

def main():
    stock_name = input("RSI CSV 파일을 생성할 주식의 이름을 입력해주세요: ")
    create_RSI(stock_name)

if __name__ == "__main__":
    main()
