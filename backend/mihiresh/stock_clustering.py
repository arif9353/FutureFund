from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import yfinance as yf
from yahooquery import search
import time
import asyncio

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


if __name__ == "__main__":

    all_recommended_stocks = [
        {
        "name": "HCL Tech",
        "price": "1324.10",
        "recommendation": "Buy HCL Technologies",
        "target_price": "1880",
        "source": "Motilal Oswal",
        "revenue": 555.9000000000001,
        "profit_percent": 41.983233894720954
        },
        {
        "name": "HCL Tech",
        "price": "1324.10",
        "recommendation": "Buy HCL Technologies",
        "target_price": "1880",
        "source": "Motilal Oswal",
        "revenue": 555.9000000000001,
        "profit_percent": 41.983233894720954
        },
        {
        "name": "HDFC Life",
        "price": "549.85",
        "recommendation": "Buy HDFC Life Insurance Company",
        "target_price": "750",
        "source": "Sharekhan",
        "revenue": 200.14999999999998,
        "profit_percent": 36.400836591797756
        },
        {
        "name": "Guj State Petro",
        "price": "290.00",
        "recommendation": "Buy Gujarat State Petronet",
        "target_price": "392",
        "source": "Prabhudas Lilladher",
        "revenue": 102,
        "profit_percent": 35.172413793103445
        },
        {
        "name": "Metro Brands",
        "price": "1135.55",
        "recommendation": "Buy Metro Brands",
        "target_price": "1530",
        "source": "Motilal Oswal",
        "revenue": 394.45000000000005,
        "profit_percent": 34.73647131346044
        },
        {
        "name": "Infosys",
        "price": "1406.90",
        "recommendation": "Buy Infosys",
        "target_price": "1870",
        "source": "YES Securities",
        "revenue": 463.0999999999999,
        "profit_percent": 32.91634089132134
        },
        {
        "name": "HDFC Life",
        "price": "549.85",
        "recommendation": "Buy HDFC Life Insurance",
        "target_price": "725",
        "source": "Emkay Global Financial",
        "revenue": 175.14999999999998,
        "profit_percent": 31.85414203873783
        },
        {
        "name": "Infosys",
        "price": "1406.90",
        "recommendation": "Buy Infosys",
        "target_price": "1850",
        "source": "Sharekhan",
        "revenue": 443.0999999999999,
        "profit_percent": 31.494775748098647
        },
        {
        "name": "Infosys",
        "price": "1406.90",
        "recommendation": "Buy Infosys",
        "target_price": "1850",
        "source": "Sharekhan",
        "revenue": 443.0999999999999,
        "profit_percent": 31.494775748098647
        },
        {
        "name": "Infosys",
        "price": "1406.90",
        "recommendation": "Buy Infosys",
        "target_price": "1850",
        "source": "Emkay Global Financial",
        "revenue": 443.0999999999999,
        "profit_percent": 31.494775748098647
        },
        {
        "name": "HDFC Bank",
        "price": "1531.55",
        "recommendation": "Buy HDFC Bank",
        "target_price": "2010",
        "source": "Religare Retail Research",
        "revenue": 478.45000000000005,
        "profit_percent": 31.23959387548562
        },
        {
        "name": "HDFC Bank",
        "price": "1531.55",
        "recommendation": "Buy HDFC Bank",
        "target_price": "2000",
        "source": "Prabhudas Lilladher",
        "revenue": 468.45000000000005,
        "profit_percent": 30.58666057262251
        },
        {
        "name": "HDFC Bank",
        "price": "1531.55",
        "recommendation": "Buy HDFC Bank",
        "target_price": "2000",
        "source": "Prabhudas Lilladher",
        "revenue": 468.45000000000005,
        "profit_percent": 30.58666057262251
        },
        {
        "name": "IndusInd Bank",
        "price": "1461.85",
        "recommendation": "Buy IndusInd Bank",
        "target_price": "1900",
        "source": "Motilal Oswal",
        "revenue": 438.1500000000001,
        "profit_percent": 29.972295379142878
        },
        {
        "name": "Shyam Metalics",
        "price": "609.75",
        "recommendation": "Buy Shyam Metalics and Energy",
        "target_price": "780",
        "source": "ICICI Securities",
        "revenue": 170.25,
        "profit_percent": 27.92127921279213
        },
        {
        "name": "HDFC Bank",
        "price": "1531.55",
        "recommendation": "Buy HDFC Bank",
        "target_price": "1950",
        "source": "Motilal Oswal",
        "revenue": 418.45000000000005,
        "profit_percent": 27.32199405830695
        },
        {
        "name": "HDFC Life",
        "price": "549.85",
        "recommendation": "Neutral HDFC Life Insurance",
        "target_price": "700",
        "source": "Motilal Oswal",
        "revenue": 150.14999999999998,
        "profit_percent": 27.307447485677905
        },
        {
        "name": "Titan Company",
        "price": "3241.90",
        "recommendation": "Buy Titan Company Ltd",
        "target_price": "4112",
        "source": "Sharekhan",
        "revenue": 870.0999999999999,
        "profit_percent": 26.839199235016498
        },
        {
        "name": "Cello World",
        "price": "845.00",
        "recommendation": "Buy Cello World",
        "target_price": "1060",
        "source": "ICICI Securities",
        "revenue": 215,
        "profit_percent": 25.443786982248522
        },
        {
        "name": "Infosys",
        "price": "1406.90",
        "recommendation": "Buy Infosys",
        "target_price": "1750",
        "source": "Emkay Global Financial",
        "revenue": 343.0999999999999,
        "profit_percent": 24.386950031985208
        },
        {
        "name": "Infosys",
        "price": "1406.90",
        "recommendation": "Buy Infosys",
        "target_price": "1750",
        "source": "Motilal Oswal",
        "revenue": 343.0999999999999,
        "profit_percent": 24.386950031985208
        },
        {
        "name": "HDFC Bank",
        "price": "1531.55",
        "recommendation": "Buy HDFC Bank",
        "target_price": "1900",
        "source": "Sharekhan",
        "revenue": 368.45000000000005,
        "profit_percent": 24.057327543991384
        },
        {
        "name": "HDFC Life",
        "price": "549.85",
        "recommendation": "Neutral HDFC Life Insurance",
        "target_price": "670",
        "source": "Motilal Oswal",
        "revenue": 120.14999999999998,
        "profit_percent": 21.851414022005997
        },
        {
        "name": "Infosys",
        "price": "1406.90",
        "recommendation": "Buy Infosys",
        "target_price": "1700",
        "source": "Sharekhan",
        "revenue": 293.0999999999999,
        "profit_percent": 20.83303717392849
        },
        {
        "name": "Wipro",
        "price": "440.65",
        "recommendation": "Neutral Wipro",
        "target_price": "520",
        "source": "Motilal Oswal",
        "revenue": 79.35000000000002,
        "profit_percent": 18.00748893679792
        }
    ]

    answer = asyncio.run(stock_clustering(all_recommended_stocks))
    if answer is not None:
        json_str = answer.to_json()
        print(json_str)
    else:
        print("No result from stock_clustering.")



