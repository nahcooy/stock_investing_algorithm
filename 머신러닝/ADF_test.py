import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import Stock_Info_Crawling
import pandas as pd

def adf_test(data):
    result = adfuller(data.values)
    print('ADF Statistics: %f' % result[0])
    print('p-value: %f' % result[1])
    print('num of lags: %f' % result[2])
    print('num of observations: %f' % result[3])
    print('Critical values:', end='')
    for k, v in result[4].items():
        print('\t%s: %.3f' % (k, v))

def main():
    stock_name = input("주식 이름 입력해주세요: ")
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)
    price_data = pd.Series(df['Close'])
    print('원본 데이터 ADF TEST 결과')
    adf_test(price_data)

    dff1 = price_data.diff().dropna()
    dff1.plot(figsize=(15, 5))
    plt.show()

    print('차분 데이터 ADF TEST 결과')
    adf_test(dff1)

if __name__ == "__main__":
    main()