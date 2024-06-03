from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import yfinance as yf
from yahooquery import search
import time

final_tickers = {}
ticker_dict = {}
tickers = []

async def stock_clustering(all_recommended_stocks):
    try:
        global final_tickers
        global ticker_dict
        global tickers
        all_recommended_stocks = filter_unique_stocks(all_recommended_stocks)
        metrics_df = await get_metrics_df(all_recommended_stocks)
        kmeans = KMeans(n_clusters=3)
        metrics_df['Risk_Level'] = kmeans.fit_predict(metrics_df[['Volatility', 'Avg_Return']])
        risk_mapping = {0: 'low', 1: 'mid', 2: 'high'}
        metrics_df['Risk_Level'] = metrics_df['Risk_Level'].map(risk_mapping)
        metrics_df.rename(index=final_tickers, inplace=True)
        output = metrics_df['Risk_Level']
        return output
    except Exception as e:
        print(f"Error: {e}")

def filter_unique_stocks(all_recommended_stocks):
    unique_stocks = {stock['name']: stock for stock in all_recommended_stocks}
    return list(unique_stocks.values())

async def get_metrics_df(all_recommended_stocks):
    try:
        global final_tickers
        global ticker_dict
        global tickers
        metrics_df = await calculate_metrics(all_recommended_stocks)
        return metrics_df
    except Exception as e:
        print(f"Error: {e}")

async def calculate_metrics(all_recommended_stocks):
    try:
        global final_tickers
        global ticker_dict
        global tickers
        ticker_dict = await ticker_value(all_recommended_stocks)
        stock_data = await fetch_stock_data(ticker_dict)
        metrics = {}
        for stock, data in stock_data.items():
            data['Return'] = data['Close'].pct_change()
            volatility = data['Return'].std() * np.sqrt(252 / len(data))
            avg_return = data['Return'].mean() * 252 / len(data)
            metrics[stock] = {'Volatility': volatility, 'Avg_Return': avg_return}
        metrics_df = pd.DataFrame(metrics).T
        return metrics_df
    except Exception as e:
        print(f"Error: {e}")

async def ticker_value(all_recommended_stocks):
    try:
        global final_tickers
        global ticker_dict
        global tickers
        for stock in all_recommended_stocks:
            ticker = get_ticker_symbol_yahoo(stock['name'])
            if ticker:
                ticker_dict[ticker] = stock['name']
                tickers.append(ticker)
            time.sleep(1) 
        tickers = list(filter(None, tickers))
        return ticker_dict
    except Exception as e:
        print(f"Error: {e}")

def get_ticker_symbol_yahoo(company_name, retries=5, delay=1):
    try:
        global final_tickers
        global ticker_dict
        global tickers
        for attempt in range(retries):
            try:
                response = search(company_name)
                if 'quotes' in response and response['quotes']:
                    symbol = response['quotes'][0]['symbol']
                    print(f"Found symbol for {company_name}: {symbol}")
                    return symbol
                else:
                    print(f"No results found for {company_name}. Response: {response}")
            except Exception as e:
                print(f"Exception fetching data for {company_name}: {e}")
            time.sleep(delay)
        print(f"Failed to get ticker for {company_name} after {retries} attempts")
        return None
    except Exception as e:
        print(f"Error: {e}")

async def fetch_stock_data(stocks, period='5y'):
    try:
        global final_tickers
        global ticker_dict
        global tickers
        stock_data = {}
        for stock in stocks.keys():
            try:
                print(f"Fetching data for {stock}...")
                ticker = yf.Ticker(stock)
                stock_history = ticker.history(period=period)
                if not stock_history.empty:
                    stock_data[stock] = stock_history
                    final_tickers[stock] = stocks[stock]
                    print(f"Data for {stock}: {stock_history.head()}")
                else:
                    print(f"{stock}: No data found, symbol may be delisted or incorrectly formatted")
            except Exception as e:
                print(f"{stock}: Error fetching data - {e}")
        return stock_data
    except Exception as e:
        print(f"Error: {e}")

