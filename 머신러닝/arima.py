import matplotlib.pyplot as plt
import pandas as pd
import Stock_Info_Crawling
from statsmodels.tsa.arima_model import ARIMA
import numpy as np
import pmdarima as pm
from pmdarima.arima import ndiffs

stock_name = input("주식 이름 입력해주세요: ")
df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)
data = pd.Series(df['Close'])

train_data, test_data = data[:int(len(data) * 0.9)], data[int(len(data) * 0.9):]

n_diffs = ndiffs(data, alpha=0.05, test='adf', max_d=6)

model_fit = pm.auto_arima(
    y=train_data,
    d=n_diffs,
    start_p=0, max_p=2,
    start_q=0, max_q=2,
    m=1, seasonal=False,  # 계절성이 없음!
    stepwise=True,
    trace=True
)
print(model_fit.summary())


def forecast_n_step(model, n=1):
    fc, conf_int = model.predict(n_periods=n, return_conf_int=True)
    # print("fc", fc,"conf_int", conf_int)
    return (
        fc.tolist()[0:n], np.asarray(conf_int).tolist()[0:n]
    )


def forecast(len, model, index, data=None):
    y_pred = []
    pred_upper = []
    pred_lower = []

    if data is not None:
        for new_ob in data:
            fc, conf = forecast_n_step(model)
            y_pred.append(fc[0])
            pred_upper.append(conf[0][1])
            pred_lower.append(conf[0][0])
            model.update(new_ob)
    else:
        for i in range(len):
            fc, conf = forecast_n_step(model)
            y_pred.append(fc[0])
            pred_upper.append(conf[0][1])
            pred_lower.append(conf[0][0])
            model.update(fc[0])
    return pd.Series(y_pred, index=index), pred_upper, pred_lower

# Forecast
fc, upper, lower = forecast(len(test_data), model_fit, test_data.index, data=test_data)

# pandas series 생성
# fc # 예측결과
lower_series = pd.Series(lower, index=test_data.index)  # 예측결과의 하한 바운드
upper_series = pd.Series(upper, index=test_data.index)  # 예측결과의 상한 바운드

# Plot 전체 데이터
plt.figure(figsize=(20, 6))
plt.plot(train_data, label='train_data')
plt.plot(test_data, c='b', label='test_data (actual price)')
plt.plot(fc, c='r', label='predicted price')
plt.fill_between(lower_series.index, lower_series, upper_series, color='k', alpha=.10)
plt.legend(loc='upper left')
plt.savefig(f"{stock_name}_all.png")
plt.show()

# Plot 테스트 데이터 부분 확대
plt.figure(figsize=(20, 6))
plt.plot(test_data, c='b', label='test_data (actual price)')
plt.plot(fc, c='r', label='predicted price')
plt.fill_between(lower_series.index, lower_series, upper_series, color='k', alpha=.10)
plt.xlim(test_data.index[0], test_data.index[-1])
plt.legend(loc='upper left')
plt.savefig(f"{stock_name}_test.png")
plt.show()

# def main():
#     pass
#
# if __name__=="__main__":
#     main()