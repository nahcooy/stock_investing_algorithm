import pandas as pd

def stock_code_crawling():
    stock_code = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]
    stock_code.sort_values(['상장일'], ascending=True, inplace=True)  # inplace=True로 설정하여 원본 DataFrame을 정렬합니다.
    stock_code = stock_code[['회사명', '종목코드', '상장일']]  # '상장일' 열을 포함하여 DataFrame을 다시 할당합니다.
    stock_code = stock_code.rename(columns={'회사명': 'company', '종목코드': 'code', '상장일': 'listing_date'})  # 열 이름을 변경합니다.
    stock_code.code = stock_code.code.map('{:06d}'.format)

    # CSV 파일로 저장
    stock_code.to_csv('stock_codes.csv', index=False)

    return

def stock_name_checker(stockname):
    stock_codes = pd.read_csv('../stock_codes.csv')
    if stockname not in stock_codes['company'].values:
        return False
    else:
        return True

def find_stock_code(stock_name):
    stock_codes = pd.read_csv('../stock_codes.csv')
    code = stock_codes.loc[stock_codes['company'] == stock_name, 'code'].iloc[0]
    return code