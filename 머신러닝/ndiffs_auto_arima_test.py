import pmdarima as pm
from pmdarima.arima import ndiffs
import Stock_Info_Crawling
import pandas as pd

def calculate_ARIMA_pdq(data):
    n_diffs = ndiffs(data, alpha=0.05, test='adf', max_d=6)
    print(f"추정된 차수 d = {n_diffs}")  # 결과

    model = pm.auto_arima(
        y=data,
        d=1,
        start_p=0, max_p=3,
        start_q=0, max_q=3,
        m=1, seasonal=False,
        stepwise=True,
        trace=True
    )

    print(model)

def main():
    stock_name = input("주식 이름 입력해주세요: ")
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)
    price_data = pd.Series(df['Close'])
    calculate_ARIMA_pdq(price_data)

if __name__=="__main__":
    main()
