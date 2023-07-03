import pandas as pd
import matplotlib.pyplot as plt
import Stock_Info_Crawling


def show_macdNclose(close, macd):
    # Date 컬럼을 datetime 형식으로 변환
    close['Date'] = pd.to_datetime(close['Date'])
    macd['Date'] = pd.to_datetime(macd['Date'])

    # 두 데이터 프레임을 Date 컬럼을 기준으로 병합
    merged_data = pd.merge(close, macd, on='Date')

    # 그래프 그리기
    plt.figure(figsize=(12, 6))

    # Price 그래프
    plt.subplot(2, 1, 1)
    plt.plot(merged_data['Date'], merged_data['Close'], color='blue', label='Price')
    plt.title('Stock Price')
    plt.ylabel('Price')
    plt.legend()

    # MACD 그래프
    plt.subplot(2, 1, 2)
    plt.plot(merged_data['Date'], merged_data['macd'], color='red', label='MACD')
    plt.plot(merged_data['Date'], merged_data['signal'], color='green', label='Signal')
    plt.bar(merged_data['Date'], merged_data['histogram'], color='gray', label='Histogram')
    plt.title('MACD')
    plt.ylabel('MACD')
    plt.xlabel('Date')
    plt.legend()

    plt.tight_layout()
    plt.show()

    return


def show_macdNclose_period(close, macd, period):
    # Date 컬럼을 datetime 형식으로 변환
    close['Date'] = pd.to_datetime(close['Date'])
    macd['Date'] = pd.to_datetime(macd['Date'])

    # 두 데이터 프레임을 Date 컬럼을 기준으로 병합
    merged_data = pd.merge(close, macd, on='Date')

    # 데이터 분할 및 그래프 그리기
    num_splits = len(merged_data) // period
    remainder = len(merged_data) % period

    for i in range(num_splits):
        start_idx = i * period
        end_idx = (i + 1) * period
        plot_data = merged_data.iloc[start_idx:end_idx]

        # 그래프 그리기
        plt.figure(figsize=(12, 6))

        # Price 그래프
        plt.subplot(2, 1, 1)
        plt.plot(plot_data['Date'], plot_data['Close'], color='blue', label='Price')
        plt.title('Stock Price')
        plt.ylabel('Price')
        plt.legend()

        # MACD 그래프
        plt.subplot(2, 1, 2)
        plt.plot(plot_data['Date'], plot_data['macd'], color='red', label='MACD')
        plt.plot(plot_data['Date'], plot_data['signal'], color='green', label='Signal')
        plt.bar(plot_data['Date'], plot_data['histogram'], color='gray', label='Histogram')
        plt.title('MACD')
        plt.ylabel('MACD')
        plt.xlabel('Date')
        plt.legend()

        plt.tight_layout()
        plt.show()

    if remainder > 0:
        plot_data = merged_data.iloc[-remainder:]

        # 그래프 그리기
        plt.figure(figsize=(12, 6))

        # Price 그래프
        plt.subplot(2, 1, 1)
        plt.plot(plot_data['Date'], plot_data['Close'], color='blue', label='Price')
        plt.title('Stock Price')
        plt.ylabel('Price')
        plt.legend()

        # MACD 그래프
        plt.subplot(2, 1, 2)
        plt.plot(plot_data['Date'], plot_data['macd'], color='red', label='MACD')
        plt.plot(plot_data['Date'], plot_data['signal'], color='green', label='Signal')
        plt.bar(plot_data['Date'], plot_data['histogram'], color='gray', label='Histogram')
        plt.title('MACD')
        plt.ylabel('MACD')
        plt.xlabel('Date')
        plt.legend()

        plt.tight_layout()
        plt.show()

    return


def find_macd_sign_change_dates(macd):
    change_dates = []

    for i in range(len(macd) - 1):
        if (macd['macd'].iloc[i] >= 0 and macd['macd'].iloc[i + 1] < 0) or (
                macd['macd'].iloc[i] < 0 and macd['macd'].iloc[i + 1] >= 0):
            change_dates.append(macd['Date'].iloc[i])

    return change_dates


def show_macdNclose_with_markers(stock_name, close, macd, period):
    close['Date'] = pd.to_datetime(close['Date'])
    macd['Date'] = pd.to_datetime(macd['Date'])

    merged_data = pd.merge(close, macd, on='Date')

    change_dates = find_macd_sign_change_dates(macd)
    i = 0
    for date in change_dates:
        selected_data = merged_data[(merged_data['Date'] >= date - pd.DateOffset(days=period)) & (
                    merged_data['Date'] <= date + pd.DateOffset(days=period))]

        plt.figure(figsize=(12, 6))

        plt.subplot(2, 1, 1)
        plt.plot(selected_data['Date'], selected_data['Close'], color='blue', label='Price')
        plt.scatter(date, selected_data.loc[selected_data['Date'] == date, 'Close'], color='green', marker='o', s=100,
                    label='Change Date')
        plt.title('Stock Price')
        plt.ylabel('Price')
        plt.legend()

        plt.subplot(2, 1, 2)
        plt.plot(selected_data['Date'], selected_data['macd'], color='red', label='MACD')
        plt.plot(selected_data['Date'], selected_data['signal'], color='green', label='Signal')
        plt.bar(selected_data['Date'], selected_data['histogram'], color='gray', label='Histogram')
        plt.scatter(date, selected_data.loc[selected_data['Date'] == date, 'macd'], color='green', marker='o', s=100,
                    label='Change Date')

        plt.title('MACD')
        plt.ylabel('MACD')
        plt.xlabel('Date')
        plt.legend()

        plt.tight_layout()
        plt.savefig(f"{stock_name}_macd_sig_{i:03d}.png")
        i += 1
        plt.show()

    return


def main():
    stock_name = input("종가와 macd 그래프를 생성할 주식의 이름을 입력하세요: ")
    Stock_Info_Crawling.save_stock_data_to_csv(stock_name)

    close = pd.read_csv(f'{stock_name}_day.csv')
    macd = pd.read_csv(f'{stock_name}_macd.csv')

    show_macdNclose(close, macd)
    show_macdNclose_with_markers(stock_name, close, macd, 15)

    return


if __name__ == "__main__":
    main()