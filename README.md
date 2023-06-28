# stock_investing_algorithm
제2회 KRX 주식 투자 알고리즘 경진대회

## 디렉토리설명
### 주식데이터크롤링
주식 데이터를 크롤링하는 코드 위주
#### Listed_Stock_Data_Crawling.py
stock_code_crawling 함수 = krx에서 현재 상장되있는 모든 주식의 회사명, 종목코드, 상장일 데이터를 크롤링해서 csv파일로 저장한다
#### Stock_Info_Crawling.py
특정 주식의 상장일부터의 날짜, 시가, 고가, 저가, 종가, 거래량, 전날대비 변화율 크롤링 후 csv파일로 저장한다

### 주식데이터전처리
크롤링된 데이터를 바탕으로 새로운 지표를 생성하는 코드
#### macd.py
특정 주식에 사용자가 원하는 기간을 가진 이동평균선을 기준으로 macd, signal, histogram을 생성한다
default 기간 = short_period=12, long_period=26, signal_period=9
