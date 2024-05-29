import requests
from bs4 import BeautifulSoup
import json
import re, os
import time
import requests
import logging
from bs4 import BeautifulSoup
from datetime import datetime

ALPHA_VANTAGE_API = os.getenv("ALPHA_VANTAGE_API")


###THIS IS FOR GOLD

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


### THIS IS FOR CRYPTOCURRENCY

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


##THIS IS FOR STOCK


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
        sorted_data = sorted(data, key=lambda x: x['Profit Percent'], reverse=True)
        return sorted_data[:25]

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

### THIS IS FOR RECURRING DEPOSITS

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


###THIS IS FOR BONDS

async def estimate_face_value(bond_data):
    try:
        # Extract relevant details from the bond data
        coupon_rate = float(bond_data['coupon'].replace('%', '').strip()) / 100
        yield_rate = float(bond_data['yield'].replace('%', '').strip()) / 100
        maturity_date = datetime.strptime(bond_data['maturity'], '%b %Y')
        if maturity_date.year == 9999:
            print(f"Skipping bond {bond_data['name']} with maturity date of Dec 9999.")
            return None
        current_date = datetime.now()  # Use the current date
        price = float(bond_data['price'].replace('₹', '').replace(',', '').strip())
        frequency = bond_data['frequency']
        
        # Calculate the maturity period in years, including months
        maturity_period_years = (maturity_date - current_date).days / 365.25
        
        # Determine the number of payments per year based on the frequency
        if frequency == 'MONTHLY':
            payments_per_year = 12
        elif frequency == 'QUARTERLY':
            payments_per_year = 4
        elif frequency == 'SEMI ANNUAL':
            payments_per_year = 2
        elif frequency == 'CUMULATIVE AT MATURITY':
            payments_per_year = 1  # For cumulative bonds, we treat as a single payment at the end
        else:  # Assume ANNUALLY
            payments_per_year = 1
        
        # Calculate the total number of payments
        total_payments = payments_per_year * maturity_period_years
        
        # Calculate the yield per period
        yield_per_period = yield_rate / payments_per_year
        
        # Approximate the coupon payment per period
        coupon_payment_per_period = (coupon_rate / payments_per_year) * price
        
        # Calculate the face value
        face_value = coupon_payment_per_period * (1 - (1 + yield_per_period) ** -total_payments) / yield_per_period
        face_value += price / ((1 + yield_per_period) ** total_payments)
        
        return round(face_value, 2)
    except Exception as e:
        print(f"Error estimating face value for bond {bond_data['name']}: {e}")
        return None

async def calculate_bond_profit(bond_data, face_value):
    try:
        # Extract relevant details from the bond data
        name = bond_data['name']
        coupon_rate = float(bond_data['coupon'].replace('%', '').strip()) / 100
        maturity_date = datetime.strptime(bond_data['maturity'], '%b %Y')
        current_date = datetime.now()  # Use the current date
        price = float(bond_data['price'].replace('₹', '').replace(',', '').strip())
        frequency = bond_data['frequency']
        
        # Calculate the maturity period in years, including months
        maturity_period_years = (maturity_date - current_date).days / 365.25
        
        # Calculate the annual coupon payment
        annual_coupon_payment = coupon_rate * face_value
        
        # Determine the number of payments per year based on the frequency
        if frequency == 'MONTHLY':
            payments_per_year = 12
        elif frequency == 'QUARTERLY':
            payments_per_year = 4
        elif frequency == 'SEMI ANNUAL':
            payments_per_year = 2
        elif frequency == 'CUMULATIVE AT MATURITY':
            payments_per_year = 1  # For cumulative bonds, we treat as a single payment at the end
        else:  # Assume ANNUALLY
            payments_per_year = 1
        
        # Calculate the total number of payments
        total_payments = payments_per_year * maturity_period_years
        
        # Calculate the total coupon payments
        if frequency == 'CUMULATIVE AT MATURITY':
            total_coupon_payments = annual_coupon_payment * maturity_period_years  # Simplified for cumulative bonds
        else:
            monthly_coupon_payment = annual_coupon_payment / 12
            total_coupon_payments = monthly_coupon_payment * total_payments
        
        # Calculate the profit
        profit = total_coupon_payments - (price - face_value)
        
        return {
            "name": name,
            "coupon_rate": f"{coupon_rate * 100:.4f}%",
            "maturity": bond_data['maturity'],
            "yield": bond_data['yield'],
            "price": f"₹ {price:,.2f}",
            "frequency": frequency,
            "profit": f"₹ {profit:,.2f}"
        }
    except Exception as e:
        print(f"Error calculating profit for bond {bond_data['name']}: {e}")
        return None

async def get_bond_details(url1):
    try:
        response = requests.get(url1)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            bond_rows = soup.find_all('tr', class_='clickable-row')
            bonds = []
            
            for bond_row in bond_rows:
                bond_name = bond_row.find('p', class_='company-title-f-cata').text.strip()
                bond_coupon = bond_row.find_all('td', class_='table-data')[1].find('p').text.strip()
                bond_maturity = bond_row.find_all('td', class_='table-data')[2].find('p').text.strip()
                bond_frequency = bond_row.find_all('td', class_='table-data')[4].find('p').text.strip()
                bond_yield = bond_row.find_all('td', class_='table-data')[5].find('p').text.strip()
                bond_price_str = bond_row.find_all('td', class_='table-data')[6].find('p').text.strip()
                bond_price = float(bond_price_str.replace('₹', '').replace(',', '').strip())
                
                try:
                    float(bond_coupon.replace('%', '').strip())
                    maturity_date = datetime.strptime(bond_maturity, '%b %Y')
                    
                    if maturity_date.year == 9999:
                        print(f"Skipping bond {bond_name} with maturity date of Dec 9999.")
                        continue
                except ValueError:
                    print(f"Skipping bond {bond_name} due to invalid data.")
                    continue
                
                bond_details = {
                    'name': bond_name,
                    'coupon': bond_coupon,
                    'maturity': bond_maturity,
                    'yield': bond_yield,
                    'price': bond_price_str,
                    'frequency': bond_frequency
                }
                
                bonds.append(bond_details)
            
            bonds.sort(key=lambda x: (float(x['price'].replace('₹', '').replace(',', '').strip()), 
                                      -float(x['yield'].replace('%', '').strip())))
            
            return bonds
        else:
            return None
    except Exception as e:
        print(f"Error fetching bond details: {e}")
        return None

async def get_bonds_data(url):
    all_bond_details = await get_bond_details(url)
    if not all_bond_details:
        return json.dumps({"bonds": [], "success": False})
    
    final_answer = []
    for bond in all_bond_details:
        estimated_face_value = await estimate_face_value(bond)
        if estimated_face_value is None:
            continue
        bond_profit = await calculate_bond_profit(bond, estimated_face_value)
        if bond_profit is None:
            continue
        bond['estimated_face_value'] = estimated_face_value
        bond['bond_profit'] = bond_profit['profit']
        final_answer.append(bond)
    
    final_answer.sort(key=lambda x: float(x['bond_profit'].replace('₹', '').replace(',', '').strip()), reverse=True)
    return final_answer[:25]
