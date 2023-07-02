from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import Stock_Info_Crawling
import matplotlib.pyplot as plt
import pandas as pd

def ACF_PACF_test_show(stock_name):
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)

    price_data = pd.Series(df['Close'])

    plot_acf(price_data)
    plot_pacf(price_data)
    plt.show()

    dff1 = price_data.diff().dropna()
    plot_acf(dff1)
    plot_pacf(dff1)
    plt.show()

def ACF_PACF_test_save(stock_name):
    df = Stock_Info_Crawling.save_stock_data_to_csv(stock_name)

    price_data = pd.Series(df['Close'])

    plot_acf(price_data)
    plt.savefig(f"{stock_name}_ACF.png")
    plt.close()

    plot_pacf(price_data)
    plt.savefig(f"{stock_name}_PACF.png")
    plt.close()

    dff1 = price_data.diff().dropna()

    plot_acf(dff1)
    plt.savefig(f"{stock_name}_Diff_ACF.png")
    plt.close()

    plot_pacf(dff1)
    plt.savefig(f"{stock_name}_Diff_PACF.png")
    plt.close()


def main():
    stock_name = input("ACF, PACF 검정을 진행할 주식의 이름을 입력해주세요: ")
    ACF_PACF_test_show(stock_name)

if __name__ == "__main__":
    main()