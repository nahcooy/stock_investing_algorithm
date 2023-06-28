import pandas as pd
import FinanceDataReader as fdr

def save_stock_data_to_csv(stock_name):
    csv_filename = f'{stock_name}_day.csv'

    try:
        # '주식이름_data.csv' 파일이 존재하는 경우
        df = pd.read_csv(csv_filename)
        print(f'CSV 파일에서 그래프 데이터를 불러왔습니다: {csv_filename}')
        return df
    except FileNotFoundError:
        print(f'CSV 파일이 존재하지 않습니다: {csv_filename}')

    # CSV 파일에서 종목 정보를 읽어옴
    stock_codes = pd.read_csv('../stock_codes.csv')

    try:
        # 주식 이름에 해당하는 종목 코드 조회
        stock_code = str(stock_codes[stock_codes['company'] == stock_name]['code'].values[0]).zfill(6)
    except IndexError:
        print('주식 이름에 해당하는 종목 코드를 찾을 수 없습니다.')
        return

    # 해당 주식의 상장일 가져오기
    listing_date = stock_codes[stock_codes['company'] == stock_name]['listing_date'].values[0]

    # FinanceDataReader를 사용하여 주식 데이터 가져오기
    df = fdr.DataReader(stock_code, start=listing_date, end=pd.Timestamp.today().strftime('%Y-%m-%d'))

    # 날짜 정보를 인덱스로 설정
    df = df.reset_index()

    # CSV 파일로 저장
    df.to_csv(csv_filename, index=False)
    print(f'그래프 데이터가 {csv_filename} 파일로 저장되었습니다.')

    return df


def main():
    stock_name = input("일별 주가 정보를 CSV파일로 저장할 주식의 이름을 입력하세요: ")
    df = save_graph_data_to_csv(stock_name)

    if df is not None:
        # 주식 데이터를 활용한 그래프 그리기 등의 작업 수행
        pass

if __name__=="__main__":
    main()