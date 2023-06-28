import pandas as pd
import Stock_Info_Crawling

def day2weekNmonth(stock_name):
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)

    # 날짜 정보를 datetime 형식으로 변환하여 인덱스로 설정
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    # 주별 주가 데이터 생성
    weekly_data = df.resample('W').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum',
        'Change': 'sum'
    })

    # 주별 주가 데이터를 CSV 파일로 저장
    weekly_data.to_csv(f'{stock_name}_week.csv', index=True)

    # 월별 주가 데이터 생성
    monthly_data = df.resample('M').agg({
        'Open': 'first',
        'High': 'max',
        'Low': 'min',
        'Close': 'last',
        'Volume': 'sum',
        'Change': 'sum'
    })

    # 월별 주가 데이터를 CSV 파일로 저장
    monthly_data.to_csv(f'{stock_name}_month.csv', index=True)

def main():
    stock_name = input("일, 주, 월별 주가 정보를 CSV파일로 저장할 주식의 이름을 입력하세요: ")
    day2weekNmonth(stock_name)

if __name__=="__main__":
    main()
