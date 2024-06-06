import joblib
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import re
from stock_clustering import stock_clustering
import json

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

async def stock_values_giver(investment_amount, stock_data):
    try:
        affordable_stocks = []
        for stock in stock_data:
            if stock:
                if investment_amount >= float(stock['price'].replace(',', '')):
                    affordable_stocks.append(stock)
        print(f"\n\nStock Data from Stock values giver: \n{stock_data}")
        categorized_stocks = {'High':[],'Medium':[],'Low':[]}
        
        count_high= 0
        count_low= 0
        count_mid= 0 
        max_price = 0
        quantity = 0

        for stock in affordable_stocks:
            if stock:
                stock_category = stock.get('category')
                stock_price = float(stock['price'].replace(',', ''))

                if stock_category == "high":
                    if count_high < 3:
                        curr_quantity = int(investment_amount / stock_price)
                        stock["quantity"] = curr_quantity
                        if stock_price > max_price:
                            max_price = stock_price
                            quantity = curr_quantity
                        categorized_stocks['High'].append(stock)
                        count_high += 1
                elif stock_category == "mid":               
                    if count_mid < 3:
                        curr_quantity = int(investment_amount / stock_price)
                        stock["quantity"] = curr_quantity 
                        if stock_price > max_price:
                            max_price = stock_price
                            quantity = curr_quantity
                        categorized_stocks['Medium'].append(stock)
                        count_mid += 1

                elif stock_category == "low":
                    if count_low < 3:
                        curr_quantity = int(investment_amount / stock_price)
                        stock["quantity"] = curr_quantity
                        if stock_price > max_price:
                            max_price = stock_price
                            quantity = curr_quantity
                        categorized_stocks['Low'].append(stock)
                    count_low += 1
        print("\nThis is categorized stocks in stock_values_giver:\n",categorized_stocks)
        if not categorized_stocks["High"] and not categorized_stocks["Medium"] and not categorized_stocks["Low"]:
            return None,None,None
        return categorized_stocks,max_price,quantity
    except Exception as e:
        print(f"error ocurred in stock_values_giver {str(e)}")
