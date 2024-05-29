import requests
from bs4 import BeautifulSoup
import json
import re, os
import time
import requests
import logging
from bs4 import BeautifulSoup

ALPHA_VANTAGE_API = os.getenv("ALPHA_VANTAGE_API")

async def fetch_usd_to_inr_rate():
    url =f"https://v6.exchangerate-api.com/v6/f9b6ab6c50a2837e18b4ff2d/latest/USD"
    response = requests.get(url)
    data = response.json()
    
    if data['result'] == 'success':
        usd_to_inr_rate = data['conversion_rates']['INR']
        return usd_to_inr_rate
    else:
        print(f"Error fetching data: {data['error-type']}")
        return None


async def get_gold_data():
    # Replace with your actual Alpha Vantage API key
    symbol = 'GLD'  # GLD is an ETF that tracks the price of gold
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=1min&apikey={ALPHA_VANTAGE_API}'

    response = requests.get(url)
    data = response.json()

    if "Time Series (1min)" in data:
        latest_time = list(data['Time Series (1min)'].keys())[0]
        latest_data = data['Time Series (1min)'][latest_time]
        latest_price = float(latest_data['4. close'])
        usd_to_inr = await fetch_usd_to_inr_rate()
        latest_price_inr = usd_to_inr * latest_price
        return latest_price_inr
    else:
        print(f"Error fetching data: {data}")
        return None


async def get_crypto_data(url1):
    # Send a GET request to the website
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url1, headers=headers)
    print(response)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the cryptocurrency data
        table = soup.find('table', {'class': 'tableWrapper_web_tbl_indices__qR1nw'})

        if table:
            # Extract rows from the table
            count = 0
            rows = table.find_all('tr')[1:]  # Exclude header row
            data = []
            for row in rows:

                columns = row.find_all('td')
                name = columns[0].get_text(strip=True)
                price = columns[1].get_text(strip=True).replace(',', '')
                """
                change = columns[2].get_text(strip=True)
                chg_percent = columns[3].get_text(strip=True)
                high_24h = columns[4].get_text(strip=True).replace(',', '')
                low_24h = columns[5].get_text(strip=True).replace(',', '')
                high_52_week = columns[6].get_text(strip=True).replace(',', '')
                low_52_week = columns[7].get_text(strip=True).replace(',', '')
                perf_3m = columns[8].get_text(strip=True)
                """
                technical_review = columns[9].get_text(strip=True)
                if technical_review == "Very Bullish":
                    count = count + 1
                    data.append({
                        'Name': name,
                        'Price': f'Rs. {price}',
                        #'Change': change,
                        #'Change Percent': chg_percent,
                        #'24H High': f'Rs. {high_24h}',
                        #'24H Low': f'Rs. {low_24h}',
                        #'52 Week High': f'Rs. {high_52_week}',
                        #'52 Week Low': f'Rs. {low_52_week}',
                        #'3M Performance': perf_3m,
                        'Technical Review': technical_review
                    })

            print(count)
            return data
        else:
            return json.dumps({'error': 'No table found on the page.'})
    else:
        return json.dumps({'error': 'Failed to retrieve the webpage.'})



async def get_stock_data(base_url):
    try:
        # Initialize data list
        data = []
        
        # Initial parameters for the AJAX request
        params = {
            'sec': 'stk_adv',
            'ajax': 1,
            'start': 1,
            'limit': 25
        }

        while True:
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                print(f"Failed to retrieve data from AJAX request: {response.status_code}")
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            additional_data = await parse_stock_advice(soup)
            if not additional_data:
                break
            
            data.extend(additional_data)
            
            # Update the 'start' parameter to get the next set of data
            params['start'] += params['limit']
            
            time.sleep(2)  # Delay between requests to mimic user behavior

        return data

    except Exception as e:
        print(f"An error occurred: {e}")
        return {'error': f'An error occurred: {e}'}

async def parse_stock_advice(soup):
    data = []
    news_list = soup.find('ul', {'class': 'news_list'})
    if news_list:
        articles = news_list.find_all('li')
        for article in articles:
            try:
                stock_info = article.find('div', {'class': 'rb_gd14'})
                if stock_info:
                    stock_name_link = stock_info.find('a')
                    stock_name = stock_name_link.get_text(strip=True) if stock_name_link else 'N/A'
                    stock_price_element = stock_info.find_all('strong')[1] if len(stock_info.find_all('strong')) > 1 else None
                    stock_price = stock_price_element.get_text(strip=True).replace(',', '') if stock_price_element else '0.0'
                    try:
                        stock_price_float = float(stock_price)
                    except ValueError:
                        stock_price_float = 0.0
                    article_link = article.find('div', {'class': 'MT5'}).find('a')
                    recommendation = article_link.get_text(strip=True)
                    recommendation_parts = recommendation.split(':')
                    if len(recommendation_parts) > 1:
                        recommendation_trimmed = recommendation_parts[0].split(';')[0].strip()
                        source = recommendation_parts[-1].strip()
                    else:
                        recommendation_trimmed = recommendation
                        source = ''
                    match = re.search(r'target of Rs (\d+[:,]?\d+)', recommendation)
                    if match:
                        target_value = match.group(1).replace(',', '')
                        try:
                            target_value_float = float(target_value)
                        except ValueError:
                            target_value_float = 0.0
                    else:
                        target_value = ''
                        target_value_float = 0.0
                    revenue = target_value_float - stock_price_float
                    if stock_price_float != 0:
                        profit_percent = (revenue / stock_price_float) * 100
                    else:
                        profit_percent = 0.0
                    data.append({
                        'Stock Name': stock_name,
                        'Price': stock_price,
                        'Recommendation': recommendation_trimmed,
                        'Target Price': target_value,
                        'Source': source,
                        'Revenue': revenue,
                        'Profit Percent': profit_percent
                    })      
            except Exception as e:
                print(f"Error processing article: {e}")
    else:
        print('No news list found in the soup')

    return data

async def get_bank_names_for_RD():
    try:
        bank_interest_data = {
            "SBI Bank": "6.5 - 7",
            "ICICI Bank": "4.75 - 7.20",
            "HDFC Bank": "4.50 - 7.25",
            "Kotak Mahindra Bank": "6.00 - 7.40",
            "Axis Bank": "5.75 - 7.20",
            "Bank of Baroda": "5.75 - 7.25",
            "Punjab National Bank": "6.00 - 7.25",
            "IDBI Bank": "6.25 - 7.00",
            "Canara Bank": "6.15 - 7.25",
            "Union Bank of India": "5.75 - 6.50",
            "Yes Bank": "6.10 - 7.75",
            "Bandhan Bank": "4.50 - 7.85",
            "Bank of Maharashtra": "5.50 - 6.25",
            "IndusInd Bank": "7.00 - 7.75",
            "Jammu and Kashmir Bank": "5.75 - 7.10",
            "Karnataka Bank": "5.80 - 7.40",
            "Saraswat Bank": "7.00 - 7.50",
            "Federal Bank": "5.75 - 7.50",
            "DBS Bank": "6.00 - 7.50",
            "RBL Bank": "5.00 - 8.00",
            "Indian Bank": "4.50 - 7.25",
            "Indian Overseas Bank": "5.75 - 7.30",
            "TMB Bank": "6.75 - 7.75"
        }
        return bank_interest_data
    except Exception as e:
        print(str(e))