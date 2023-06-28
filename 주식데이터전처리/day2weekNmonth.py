import pandas as pd
import Stock_Info_Crawling

def day2weekNmonth(stock_name):
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)

    # 주별 주가 데이터 생성
    weekly_data = df.resample('W', on='Date').agg({
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
    monthly_data = df.resample('M', on='Date').agg({
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
    df = day2weekNmonth(stock_name)

    if df is not None:
        # 주식 데이터를 활용한 그래프 그리기 등의 작업 수행
        pass

if __name__=="__main__":
    main()