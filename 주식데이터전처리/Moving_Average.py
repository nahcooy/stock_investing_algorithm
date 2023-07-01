import pandas as pd
import Stock_Info_Crawling


def caculate_moving_average(df, period):
    # 이동평균 계산
    moving_average = df.rolling(window=period).mean()

    return moving_average

def create_moving_average(stock_name, period):
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)
    price_data = pd.Series(df['Close'])

    moving_average = caculate_moving_average(price_data, period)

    try:
        macd_csv = pd.read_csv(f'{stock_name}_ma.csv')
    except:
        create_basic_moving_average(stock_name)
        macd_csv = pd.read_csv(f'{stock_name}_ma.csv')

    macd_csv[f'ma_{period:03d}'] = moving_average

    macd_csv.to_csv(f'{stock_name}_ma.csv', index=False)

    return

def create_basic_moving_average(stock_name):
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)
    price_data = pd.Series(df['Close'])
    date_data = pd.Series(df['Date'])

    periods = [5, 10, 20, 60, 120, 240]
    ma_data = list()
    for period in periods:
        ma_data.append(caculate_moving_average(price_data, period))

    # 데이터프레임 생성
    df_ma = pd.DataFrame({'Date':date_data, 'ma_005': ma_data[0], 'ma_010': ma_data[1], 'ma_020': ma_data[2], 'ma_060': ma_data[3], 'ma_120': ma_data[4], 'ma_240': ma_data[5]})

    # CSV 파일로 저장
    df_ma.to_csv(f'{stock_name}_ma.csv', index=False)

    return

def main():
    stock_name = input("이동평균 csv 파일을 생성할 주식 이름을 입력해주세요: ").strip()
    create_basic_moving_average(stock_name)

if __name__=="__main__":
    main()