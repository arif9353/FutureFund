import re
from stock_clustering import stock_clustering
import json
import requests
from bs4 import BeautifulSoup
import json
import re
import time

#FETCHING DATA

async def get_stock_data(base_url):
    try:
        # Initialize data list
        data = []
        
        # Initial parameters for the AJAX request
        params = {
            'sec': 'stk_adv',
            'ajax': 1,
            'start': 1,
            'limit': 50
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
        sorted_data = sorted(data, key=lambda x: x['profit_percent'], reverse=True)
        return sorted_data[:25], sorted_data

    except Exception as e:
        print(f"An error occurred: {e}")
        return {'An error occurred while trying to get the stock data: {e}'}

async def parse_stock_advice(soup):
    try:
        data = []
        news_list = soup.find('ul', {'class': 'news_list'})
        if news_list:
            articles = news_list.find_all('li')
            for article in articles:
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
                    if profit_percent >0.0:
                        data.append({
                            'name': stock_name,
                            'price': stock_price,
                            'recommendation': recommendation_trimmed,
                            'target_price': target_value,
                            'source': source,
                            'revenue': revenue,
                            'profit_percent': profit_percent
                        })      
        else:
            print('No news list found in the soup')

        return data
    except Exception as e:
        print(f"Error occurred while trying to parse stock data: {str(e)}")
        return f"Error occurred while trying to parse stock data: {str(e)}"

# CLUSTERING OF STOCKS

async def stock_cluster_gen(investment_amount, stock_data):
    try:
        affordable_stocks = []
        for stock in stock_data:
            if investment_amount >= float(stock['price'].replace(',', '')):
                affordable_stocks.append(stock)

        clusters_df,all_recommend_stocks = await stock_clustering(affordable_stocks)
        cluster_json = clusters_df.to_json()
        cluster_dict = json.loads(cluster_json)


        for stock in all_recommend_stocks:
            stock_name = stock['name']
            if stock_name in cluster_dict:
                stock['category'] = cluster_dict[stock_name]
        if not all_recommend_stocks:
            return None
        return all_recommend_stocks
    except Exception as e:
        print(f"error ocurred in stock_cluster_gen fn {str(e)}")


#GIVING STOCKS AS PER AFFORDABILITY

async def stock_values_giver(investment_amount, stock_data):
    try:
        affordable_stocks = []
        for stock in stock_data:
            if stock:
                if investment_amount >= float(stock['price'].replace(',', '')):
                    affordable_stocks.append(stock)
        categorized_stocks = {'High':[],'Medium':[],'Low':[]}
        
        count_high= 0
        count_low= 0
        count_mid= 0 
        max_price = 0
        quantity = 0
        max_profit = 0
        max_profit_quantity = 0

        for stock in affordable_stocks:
            if stock:
                stock_category = stock.get('category')
                stock_price = float(stock['price'].replace(',', ''))
                profit = stock['revenue']
                if stock_category == "high":
                    if count_high < 3:
                        curr_quantity = int(investment_amount / stock_price)
                        stock["quantity"] = curr_quantity
                        if stock_price > max_price:
                            max_price = stock_price
                            quantity = curr_quantity
                        categorized_stocks['High'].append(stock)
                        if (profit*curr_quantity)>=max_profit:
                            max_profit = profit
                            max_profit_quantity = curr_quantity
                        count_high += 1
                elif stock_category == "mid":               
                    if count_mid < 3:
                        curr_quantity = int(investment_amount / stock_price)
                        stock["quantity"] = curr_quantity 
                        profit = stock['revenue']
                        if stock_price > max_price:
                            max_price = stock_price
                            quantity = curr_quantity
                        categorized_stocks['Medium'].append(stock)
                        if (profit*curr_quantity)>=max_profit:
                            max_profit = profit
                            max_profit_quantity = curr_quantity
                        count_mid += 1

                elif stock_category == "low":
                    if count_low < 3:
                        curr_quantity = int(investment_amount / stock_price)
                        stock["quantity"] = curr_quantity
                        profit = stock['revenue']
                        if stock_price > max_price:
                            max_price = stock_price
                            quantity = curr_quantity
                        categorized_stocks['Low'].append(stock)
                        if (profit*curr_quantity)>=max_profit:
                            max_profit = profit
                            max_profit_quantity = curr_quantity
                        count_low += 1
        if not categorized_stocks["High"] and not categorized_stocks["Medium"] and not categorized_stocks["Low"]:
            return None,None,None, None, None
        return categorized_stocks,max_price,quantity,max_profit,max_profit_quantity
    except Exception as e:
        print(f"error ocurred in stock_values_giver {str(e)}")
