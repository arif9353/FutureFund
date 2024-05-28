import requests
from bs4 import BeautifulSoup
import re
import json


def get_stock_advice(url):
    # Send a GET request to the website
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the section containing the news articles
        middle_section = soup.find('div', {'class': 'middle_section'})

        # Prepare data for JSON
        data = []

        if middle_section:
            # Extract individual news items from 'news_list'
            news_list = middle_section.find('ul', {'class': 'news_list'})
            if news_list:
                articles = news_list.find_all('li')
                for article in articles:
                    stock_info = article.find('div', {'class': 'rb_gd14'})
                    stock_name_link = stock_info.find('a')
                    stock_name = stock_name_link.get_text(strip=True)
                    stock_price = stock_info.find_all('strong')[1].get_text(strip=True).replace(',', '')

                    try:
                        stock_price_float = float(stock_price)
                    except ValueError:
                        stock_price_float = 0.0

                    article_link = article.find('div', {'class': 'MT5'}).find('a')
                    recommendation = article_link.get_text(strip=True)

                    # Trim recommendation up to the first colon and parse details
                    recommendation_parts = recommendation.split(':')
                    if len(recommendation_parts) > 1:
                        recommendation_trimmed = recommendation_parts[0].split(';')[0].strip()
                        source = recommendation_parts[-1].strip()
                    else:
                        recommendation_trimmed = recommendation
                        source = ''

                    # Extract target price
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

                    # Calculate revenue
                    revenue = target_value_float - stock_price_float

                    # Calculate profit percent
                    if stock_price_float != 0:
                        profit_percent = (revenue / stock_price_float) * 100
                    else:
                        profit_percent = 0.0

                    data.append({
                        'Stock Name': stock_name,
                        'Price': f'Rs {stock_price}',
                        'Recommendation': recommendation_trimmed,
                        'Target Price': target_value,
                        'Source': source,
                        'Revenue': f'Rs {revenue:.2f}',
                        'Profit Percent': f'{profit_percent:.2f}%'
                    })
            else:
                return json.dumps({'error': 'No news list found on the page.'})
        else:
            return json.dumps({'error': 'No middle section found on the page.'})
    else:
        return json.dumps({'error': 'Failed to retrieve the webpage.'})

    # Sort data by profit percent in descending order and select top 3
    top_3_stocks = sorted(data, key=lambda x: float(x['Profit Percent'].replace('%', '')), reverse=True)[:3]

    return json.dumps(top_3_stocks, indent=4)


# URL of the website
url = 'https://m.moneycontrol.com/markets/stock-advice/'
top_3_stocks_json = get_stock_advice(url)
print(top_3_stocks_json)
