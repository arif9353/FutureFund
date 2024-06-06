import yfinance as yf
import pandas as pd
import os, requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error

async def fetch_usd_to_inr_rate():
    try:
        url =f"https://v6.exchangerate-api.com/v6/f9b6ab6c50a2837e18b4ff2d/latest/USD"
        response = requests.get(url)
        data = response.json()
        
        if data['result'] == 'success':
            usd_to_inr_rate = data['conversion_rates']['INR']
            return usd_to_inr_rate
        else:
            print(f"Error fetching data: {data['error-type']}")
            return None
    except Exception as e:
        print(f"Error fetching currency exchange data (usd-to-inr): {str(e)}")
        return f"Error Occurred: {str(e)}"

async def fetch_real_time_gold_price_alpha_vantage():
    try:
        # Replace with your actual Alpha Vantage API key
        symbol = 'GLD'  # GLD is an ETF that tracks the price of gold
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey=QYHRK01Q1ORWYPSJ'

        response = requests.get(url)
        data = response.json()

        if "Time Series (1min)" in data:
            latest_time = list(data['Time Series (1min)'].keys())[0]
            latest_data = data['Time Series (1min)'][latest_time]
            latest_price = float(latest_data['4. close'])
            usd_to_inr = await fetch_usd_to_inr_rate()
            latest_price = latest_price*usd_to_inr
            """
        latest_price=215.3
        latest_price = latest_price*83.4319
        print("\nThe leatest price is: ", latest_price)
        return latest_price
    """
            return latest_price
        else:
            print(f"Error fetching data: {data}")
            return None
    except Exception as e:
        print(f"error occurred in fetch_real_time_gold_price_alpha_vantage function in gold.py {str(e)}")

async def predict_next_n_days(n_days):
    try:
        gold_data = yf.download('GLD', start='2010-01-01', end='2024-05-24')

        # Handle missing values
        gold_data = gold_data.dropna()

        # Create relevant features
        gold_data['MA_10'] = gold_data['Close'].rolling(window=10).mean()
        gold_data['MA_50'] = gold_data['Close'].rolling(window=50).mean()
        gold_data['Volatility'] = gold_data['Close'].rolling(window=10).std()
        gold_data['Return'] = gold_data['Close'].pct_change()

        # Drop rows with NaN values created by rolling window calculations
        gold_data = gold_data.dropna()

        # Define features and target
        features = ['MA_10', 'MA_50', 'Volatility', 'Return']
        X = gold_data[features]
        y = gold_data['Close']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Train a regression model
        model = RandomForestRegressor(n_estimators=100, random_state=42)
        model.fit(X_train_scaled, y_train)

        # Evaluate the model
        y_pred = model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)

        # Fetch real-time gold data
        gold_price = await fetch_real_time_gold_price_alpha_vantage()
        #gold_price = 18010.96
        if gold_price is None:
            return None
        # Copy the last row of the gold_data DataFrame to use for prediction
        last_row = gold_data.iloc[-1].copy()
        predictions = []
        usd_to_inr = await fetch_usd_to_inr_rate()
        for _ in range(n_days):
            ma_10 = last_row['MA_10']
            ma_50 = last_row['MA_50']
            volatility = last_row['Volatility']
            return_pct = last_row['Return']
            
            # Prepare the input data for prediction
            input_data = pd.DataFrame([[ma_10, ma_50, volatility, return_pct]], columns=features)
            input_data_scaled = scaler.transform(input_data)

            # Predict future gold price (next closing price)
            future_price = model.predict(input_data_scaled)[0]
            future_price_inr = future_price * usd_to_inr
            predictions.append(future_price_inr)

            # Update the last_row with the new prediction
            # Use concat to append the new predicted price
            extended_close = pd.concat([gold_data['Close'], pd.Series([future_price])])
            
            last_row['Close'] = future_price
            last_row['MA_10'] = extended_close.rolling(window=10).mean().iloc[-1]
            last_row['MA_50'] = extended_close.rolling(window=50).mean().iloc[-1]
            last_row['Volatility'] = extended_close.rolling(window=10).std().iloc[-1]
            last_row['Return'] = future_price / gold_data['Close'].iloc[-1] - 1

        return predictions
    except Exception as e:
        print(f"error occurred in predict_next_n_days function in gold.py {str(e)}")

# Example usage

async def get_gold_for_main():
    try:
        future_gold_prices = await predict_next_n_days(30)
        print("future gold price: ",future_gold_prices[-1])
        return future_gold_prices[-1]
    except Exception as e:
        print(f"error occurred in get_gold_for_main function in gold.py {str(e)}")


#PREDICTING FUTURE GOLD PRICE AND PROFITS AS PER THE INVESTMENT AMOUNT

async def gold_give(gold_price,years,investment_price):
    try:
        if investment_price>=gold_price:
            quantity = int(investment_price/gold_price)
            future_gold_price = await get_gold_for_main()
            profit_pm = future_gold_price - gold_price
            profit = profit_pm * years * 12
            return profit,quantity
        else:
            return None,None
    except Exception as e:
        print(f"error occurred in gold_give fn {str(e)}")




'''
if __name__ == "__main__":
    answer = asyncio.run(get_gold_for_main())
    print(answer)
'''

"""
                if count_high < 3:
                    if stock_price > max_price:
                        max_price = stock_price
                        quantity = int(investment_amount / stock_price)
                    categorized_stocks['High'].append(stock)
                    count_high += 1

                if stock_price > max_price:
                        max_price = stock_price
                        quantity = int(investment_amount / stock_price)
                    categorized_stocks['Medium'].append(stock)
                    count_mid += 1

                if count_low < 3:
                    if stock_price > max_price:
                        max_price = stock_price
                        quantity = int(investment_amount / stock_price)
                    categorized_stocks['Low'].append(stock)
                    count_low += 1
"""