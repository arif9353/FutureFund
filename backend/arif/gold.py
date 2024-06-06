import yfinance as yf
import pandas as pd
import os, requests
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from dotenv import load_dotenv

load_dotenv()

ALPHA_VANTAGE_API = os.getenv("ALPHA_VANTAGE_API")
EXCHANGE_RATE_API = os.getenv("EXCHANGE_RATE_API")

# Fetch historical gold prices (using GLD ETF as a proxy)
gold_data = yf.download('GLD', start='2010-01-01', end='2024-05-24', interval='1mo')

# Handle missing values
gold_data = gold_data.dropna()

# Create relevant features
gold_data['MA_2'] = gold_data['Close'].rolling(window=2).mean()
gold_data['MA_5'] = gold_data['Close'].rolling(window=5).mean()
gold_data['Volatility'] = gold_data['Close'].rolling(window=2).std()
gold_data['Return'] = gold_data['Close'].pct_change()

# Drop rows with NaN values created by rolling window calculations
gold_data = gold_data.dropna()
print(gold_data.head())

# Define features and target
features = ['MA_2', 'MA_5', 'Volatility', 'Return']
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
print(f"Mean Squared Error: {mse}")

def fetch_usd_to_inr_rate():
    url =f"https://v6.exchangerate-api.com/v6/{EXCHANGE_RATE_API}/latest/USD"
    print(url)
    response = requests.get(url)
    data = response.json()
    
    if data['result'] == 'success':
        usd_to_inr_rate = data['conversion_rates']['INR']
        print(usd_to_inr_rate)
        return usd_to_inr_rate
    else:
        print(f"Error fetching data: {data['error-type']}")
        return None


def fetch_real_time_gold_price_alpha_vantage():
    # Replace with your actual Alpha Vantage API key
    symbol = 'GLD'  # GLD is an ETF that tracks the price of gold
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHA_VANTAGE_API}'

    response = requests.get(url)
    data = response.json()

    if "Time Series (1min)" in data:
        latest_time = list(data['Time Series (1min)'].keys())[0]
        latest_data = data['Time Series (1min)'][latest_time]
        latest_price = float(latest_data['4. close'])
        print("\nThe leatest price is: ", latest_price)
        print("\n")
        return latest_price
    else:
        print(f"Error fetching data: {data}")
        return None

def predict_next_n_days(n_days):
    # Fetch real-time gold data
    gold_price = fetch_real_time_gold_price_alpha_vantage()
    if gold_price is None:
        return None

    # Copy the last row of the gold_data DataFrame to use for prediction
    last_row = gold_data.iloc[-1].copy()
    
    predictions = []
    usd_to_inr = fetch_usd_to_inr_rate()

    for _ in range(n_days):
        ma_2 = last_row['MA_2']
        ma_5 = last_row['MA_5']
        volatility = last_row['Volatility']
        return_pct = last_row['Return']
        
        # Prepare the input data for prediction
        input_data = pd.DataFrame([[ma_2, ma_5, volatility, return_pct]], columns=features)
        input_data_scaled = scaler.transform(input_data)

        # Predict future gold price (next closing price)
        future_price = model.predict(input_data_scaled)[0]
        future_price_inr = future_price * usd_to_inr
        predictions.append(future_price_inr)

        # Update the last_row with the new prediction
        # Use concat to append the new predicted price
        extended_close = pd.concat([gold_data['Close'], pd.Series([future_price])])
        
        last_row['Close'] = future_price
        last_row['MA_2'] = extended_close.rolling(window=2).mean().iloc[-1]
        last_row['MA_5'] = extended_close.rolling(window=5).mean().iloc[-1]
        last_row['Volatility'] = extended_close.rolling(window=2).std().iloc[-1]
        last_row['Return'] = future_price / gold_data['Close'].iloc[-1] - 1

    return predictions

# Example usage
future_gold_prices = predict_next_n_days(10)
if future_gold_prices:
    print(f"Predicted future gold prices for the next 10 months: {future_gold_prices}")
