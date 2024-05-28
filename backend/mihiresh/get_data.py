import requests
from bs4 import BeautifulSoup
import json
import re
import time
import requests
import logging
from bs4 import BeautifulSoup



async def get_top_cryptos(url1):
    # Send a GET request to the website
    response = requests.get(url1)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the table containing the cryptocurrency data
        table = soup.find('table', {'class': 'tableWrapper_web_tbl_indices__qR1nw'})

        if table:
            # Extract rows from the table
            rows = table.find_all('tr')[1:]  # Exclude header row
            data = []
            for row in rows:
                columns = row.find_all('td')
                name = columns[0].get_text(strip=True)
                price = columns[1].get_text(strip=True).replace(',', '')
                change = columns[2].get_text(strip=True)
                chg_percent = columns[3].get_text(strip=True)
                high_24h = columns[4].get_text(strip=True).replace(',', '')
                low_24h = columns[5].get_text(strip=True).replace(',', '')
                high_52_week = columns[6].get_text(strip=True).replace(',', '')
                low_52_week = columns[7].get_text(strip=True).replace(',', '')
                perf_3m = columns[8].get_text(strip=True)
                technical_review = columns[9].get_text(strip=True)

                data.append({
                    'Name': name,
                    'Price': f'Rs. {price}',
                    'Change': change,
                    'Change Percent': chg_percent,
                    '24H High': f'Rs. {high_24h}',
                    '24H Low': f'Rs. {low_24h}',
                    '52 Week High': f'Rs. {high_52_week}',
                    '52 Week Low': f'Rs. {low_52_week}',
                    '3M Performance': perf_3m,
                    'Technical Review': technical_review
                })

            return data
        else:
            return json.dumps({'error': 'No table found on the page.'})
    else:
        return json.dumps({'error': 'Failed to retrieve the webpage.'})


# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def get_stock_advice(base_url):
    try:
        # Initialize data list
        data = []
        
        # Initial parameters for the AJAX request
        params = {
            'sec': 'stk_adv',
            'ajax': 1,
            'start': 1,
            'limit': 60
        }

        while True:
            response = requests.get(base_url, params=params)
            if response.status_code != 200:
                logging.error(f"Failed to retrieve data from AJAX request: {response.status_code}")
                break
            
            soup = BeautifulSoup(response.content, 'html.parser')
            additional_data = await parse_stock_advice(soup)
            print("additional data", additional_data)
            if not additional_data:
                break
            
            data.extend(additional_data)
            
            # Update the 'start' parameter to get the next set of data
            params['start'] += params['limit']
            
            time.sleep(2)  # Delay between requests to mimic user behavior

        return data

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        return {'error': f'An error occurred: {e}'}

async def parse_stock_advice(soup):
    data = []
    news_list = soup.find('ul', {'class': 'news_list'})
    lmno = 0
    if news_list:
        articles = news_list.find_all('li')
        for article in articles:
            lmno=lmno+1
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
                logging.error(f"Error processing article: {e}")
        print("this is lmnopq",lmno)
    else:
        logging.warning('No news list found in the soup')

    return data