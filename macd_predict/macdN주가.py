import pandas as pd
import os
import macd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import Stock_Info_Crawling
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

import csv

def evaluate_predictions(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    return mse, mae, r2

def calculate_macd_slope(stock_name):
    filename = f'{stock_name}_macd.csv'
    if not os.path.isfile(filename):
        print(f"{filename} 파일이 존재하지 않습니다. create_macd_data 함수로 {filename}를 생성합니다")
        macd.create_macd_data(stock_name)

    macd_data = pd.read_csv(f'{stock_name}_macd.csv')

    if 'macd_slope' not in macd_data.columns:
        macd_slope = macd_data['macd'].diff()  # 이전 값과의 차이 계산
        macd_data['macd_slope'] = macd_slope  # 새로운 열로 슬로프 추가
        macd_data.to_csv(f'{stock_name}_macd.csv', index=False)  # 덮어쓰기
    else:
        macd_slope = macd_data['macd_slope']

    return macd_slope

def predict_stock_price(stock_name):
    close_prices = Stock_Info_Crawling.return_close(stock_name) # 종가 모두 가져오기
    macd_slope = calculate_macd_slope(stock_name)

    # MACD 슬로프를 입력 변수로, 15일 뒤의 주식 수익률을 타겟 변수로 사용하여 회귀 모델 학습
    X = macd_slope[1:-15].values.reshape(-1, 1)
    close_prices_back = close_prices[16:].reset_index(drop=True)  # 16번 인덱스부터 끝까지의 데이터, 인덱스 재설정
    close_prices_front = close_prices[1:-15].reset_index(drop=True)  # 인덱스 재설정
    y = (close_prices_back - close_prices_front) / close_prices_front * 100

    Xy = pd.DataFrame({'X': X.flatten(), 'y': y.values})
    Xy.to_csv(f'{stock_name}_Xy.csv', index=False)

    # 선형 회귀 모델 생성 및 학습
    model = LinearRegression()
    model.fit(X, y)

    # 실제 데이터 포인트의 산점도
    plt.scatter(X, y, color='blue', label='실제 데이터')

    # 회귀선의 선 그래프
    plt.plot(X, model.predict(X), color='red', label='회귀선')

    # 그래프의 레이블과 제목 설정
    plt.xlabel('X')
    plt.ylabel('y')
    plt.title('선형 회귀')

    # 범례 추가
    plt.legend()
    plt.savefig(f'{stock_name}_선형회귀.png')
    # 그래프 표시
    plt.show()

    # 모든 날짜에 대한 주식 수익률 예측
    predicted_returns = model.predict(macd_slope[1:].values.reshape(-1, 1))
    print("macd_slope, close 선형회귀 끝!")

    # 15일 뒤의 주식 예상 가격 계산
    current_prices = close_prices[1:].reset_index(drop=True)
    predicted_prices = current_prices * (1 + predicted_returns / 100)

    actual_returns = (close_prices_back - close_prices_front) / close_prices_front * 100
    predicted_returns_for_actual_returns = predicted_returns[:-15]
    mse, mae, r2 = evaluate_predictions(actual_returns, predicted_returns_for_actual_returns)

    print("MSE:", mse)
    print("MAE:", mae)
    print("R^2:", r2)
    print(predicted_prices)

    return predicted_prices

def create_macd_predict_data(stock_name):
    filename = f'{stock_name}_macd.csv'
    predict_filename = f'{stock_name}_macd_predict.csv'

    macd_data = pd.read_csv(filename)
    close_prices = Stock_Info_Crawling.return_close(stock_name)
    predicted_prices = predict_stock_price(stock_name)
    print(len(macd_data), len(close_prices), len(predicted_prices))

    df = pd.DataFrame(columns=['Date', 'close_prices', 'predicted_prices'])
    df['Date'] = macd_data['Date']
    df['close_prices'] = close_prices

    # df의 길이를 1485로 맞추기 위해 추가된 부분입니다.
    df = df.reindex(range(1485))

    start_index = 16
    for i, price in enumerate(predicted_prices):
        df.loc[start_index + i, 'predicted_prices'] = price

    df['macd_slope'] = macd_data['macd_slope']

    df.to_csv(predict_filename, index=False)

    return

def plot_all_stock_price_with_predictions(stock_name):
    # CSV 파일에서 데이터 로드
    data = pd.read_csv(f'{stock_name}_macd_predict.csv')

    # 그래프 설정
    plt.figure(figsize=(12, 8))

    # 첫 번째 그래프: close_prices와 predicted_prices
    plt.subplot(2, 1, 1)  # 2개의 서브플롯 중 첫 번째
    x = range(len(data))
    plt.plot(x, data["predicted_prices"], label="Predicted Prices")
    plt.plot(x, data["close_prices"], label="Close Prices")

    plt.xlabel("Index")
    plt.ylabel("Price")
    plt.title("Close Prices vs Predicted Prices")
    plt.legend()

    # 두 번째 그래프: macd_slope
    plt.subplot(2, 1, 2)  # 2개의 서브플롯 중 두 번째
    plt.plot(x, data["macd_slope"], color="red")
    plt.xlabel("Index")
    plt.ylabel("MACD Slope")
    plt.title("MACD Slope")

    # 그래프 표시
    plt.tight_layout()
    plt.savefig(f'{stock_name}_graph.png')
    plt.show()

def plot_stock_price_with_predictions(stock_name, period=120):
    # CSV 파일에서 데이터 로드
    data = pd.read_csv(f'{stock_name}_macd_predict.csv')

    # 데이터를 period 길이로 나누어 그래프 표시
    num_periods = len(data) // period
    remainder = len(data) % period

    for i in range(num_periods):
        start = i * period
        end = (i + 1) * period
        plot_data = data[start:end]

        # 그래프 설정
        plt.figure(figsize=(12, 8))

        # 첫 번째 그래프: close_prices와 predicted_prices
        plt.subplot(2, 1, 1)  # 2개의 서브플롯 중 첫 번째
        x = range(len(plot_data))
        plt.plot(x, plot_data["predicted_prices"], label="Predicted Prices")
        plt.plot(x, plot_data["close_prices"], label="Close Prices")
        plt.xlabel("Index")
        plt.ylabel("Price")
        plt.title("Close Prices vs Predicted Prices")
        plt.legend()

        # 두 번째 그래프: macd_slope
        plt.subplot(2, 1, 2)  # 2개의 서브플롯 중 두 번째
        plt.plot(x, plot_data["macd_slope"], color="red")
        plt.xlabel("Index")
        plt.ylabel("MACD Slope")
        plt.title("MACD Slope")

        # 그래프 표시
        plt.tight_layout()
        plt.savefig(f'{stock_name}_graph{i}.png')
        plt.show()


    # 남은 부분을 따로 그래프로 표시
    if remainder > 0:
        start = num_periods * period
        plot_data = data[start:]

        # 그래프 설정
        plt.figure(figsize=(12, 8))

        # 첫 번째 그래프: close_prices와 predicted_prices
        plt.subplot(2, 1, 1)  # 2개의 서브플롯 중 첫 번째
        x = range(len(plot_data))
        plt.plot(x, plot_data["predicted_prices"], label="Predicted Prices")
        plt.plot(x, plot_data["close_prices"], label="Close Prices")
        plt.xlabel("Index")
        plt.ylabel("Price")
        plt.title("Close Prices vs Predicted Prices")
        plt.legend()

        # 두 번째 그래프: macd_slope
        plt.subplot(2, 1, 2)  # 2개의 서브플롯 중 두 번째
        plt.plot(x, plot_data["macd_slope"], color="red")
        plt.xlabel("Index")
        plt.ylabel("MACD Slope")
        plt.title("MACD Slope")

        # 그래프 표시
        plt.tight_layout()
        plt.savefig(f'{stock_name}_graph{num_periods}.png')
        plt.show()

def plot_predicted_returns(stock_name):
    close_prices = Stock_Info_Crawling.return_close(stock_name)
    macd_slope = calculate_macd_slope(stock_name)

    # MACD 슬로프를 입력 변수로, 15일 뒤의 주식 수익률을 타겟 변수로 사용하여 회귀 모델 학습
    X = macd_slope[1:-15].values.reshape(-1, 1)
    close_prices_back = close_prices[16:].reset_index(drop=True)
    close_prices_front = close_prices[1:-15].reset_index(drop=True)
    y = (close_prices_back - close_prices_front) / close_prices_front * 100

    # 선형 회귀 모델 생성 및 학습
    model = LinearRegression()
    model.fit(X, y)

    # 모든 날짜에 대한 주식 수익률 예측
    predicted_returns = model.predict(macd_slope[1:].values.reshape(-1, 1))
    actual_returns = (close_prices_back - close_prices_front) / close_prices_front * 100
    predicted_returns_for_actual_returns = predicted_returns[:-15]

    # 차이 계산
    difference = actual_returns - predicted_returns_for_actual_returns

    # 그래프 설정
    plt.figure(figsize=(12, 6))

    # difference 그래프
    x_diff = range(len(difference))
    plt.plot(x_diff, difference, color='blue', label='Difference')
    plt.xlabel('Index')
    plt.ylabel('Difference')
    plt.title('Difference between Actual Returns and Predicted Returns')
    plt.legend()

    # 그래프 저장
    plt.tight_layout()
    plt.savefig(f'{stock_name}_difference.png')
    plt.show()

    # actual_returns와 predicted_returns_for_actual_returns 그래프
    plt.figure(figsize=(12, 6))
    x_returns = range(len(actual_returns))
    plt.plot(x_returns, actual_returns, color='green', label='Actual Returns')
    plt.plot(x_returns, predicted_returns_for_actual_returns, color='orange', label='Predicted Returns')
    plt.xlabel('Index')
    plt.ylabel('Returns')
    plt.title('Actual Returns vs Predicted Returns')
    plt.legend()

    # 그래프 저장
    plt.tight_layout()
    plt.savefig(f'{stock_name}_actual_vs_predicted_returns.png')
    plt.show()

    # actual_returns와 predicted_returns_for_actual_returns가 동시에 상승하거나 하락한 비율 출력
    both_increase = ((actual_returns > 0) & (predicted_returns_for_actual_returns > 0)).sum() / len(actual_returns)
    both_decrease = ((actual_returns < 0) & (predicted_returns_for_actual_returns < 0)).sum() / len(actual_returns)
    print("Both Increase Ratio:", both_increase)
    print("Both Decrease Ratio:", both_decrease)

def main():
    stock_name = input("macd slope와 close를 선형회귀로 예측 후, 시각화할 주식의 이름을 입력하시오: ")
    plot_stock_price_with_predictions(stock_name)
    plot_all_stock_price_with_predictions(stock_name)
    predict_stock_price(stock_name)

if __name__=="__main__":
    main()