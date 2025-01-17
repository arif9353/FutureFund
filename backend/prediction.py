import joblib
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import re
from stock_clustering import stock_clustering
import json
from gold import get_gold_for_main
import copy


async def display_results(low_pred, mid_pred, high_pred):
    try:
        answer = []
        print("Low Risk:")
        print(f"s1: {low_pred[0]*100:.2f}%, s2: {low_pred[1]*100:.2f}%, s3: {low_pred[2]*100:.2f}%, s4: {low_pred[3]*100:.2f}%, s5: {low_pred[4]*100:.2f}%, s6: {low_pred[5]*100:.2f}%")
        low_percent = {"s1":f"{low_pred[0]*100}","s2":f"{low_pred[1]*100}","s3":f"{low_pred[2]*100}","s4":f"{low_pred[3]*100}","s5":f"{low_pred[4]*100}","s6":f"{low_pred[5]*100}"}
        answer.append(low_percent)
        print("Medium Risk:")
        print(f"s1: {mid_pred[0]*100:.2f}%, s2: {mid_pred[1]*100:.2f}%, s3: {mid_pred[2]*100:.2f}%, s4: {mid_pred[3]*100:.2f}%, s5: {mid_pred[4]*100:.2f}%, s6: {mid_pred[5]*100:.2f}%")
        mid_percent = {"s1":f"{mid_pred[0]*100}","s2":f"{mid_pred[1]*100}","s3":f"{mid_pred[2]*100}","s4":f"{mid_pred[3]*100}","s5":f"{mid_pred[4]*100}","s6":f"{mid_pred[5]*100}",}
        answer.append(mid_percent)
        print("High Risk:")
        print(f"s1: {high_pred[0]*100:.2f}%, s2: {high_pred[1]*100:.2f}%, s3: {high_pred[2]*100:.2f}%, s4: {high_pred[3]*100:.2f}%, s5: {high_pred[4]*100:.2f}%, s6: {high_pred[5]*100:.2f}%")
        high_percent = {"s1":f"{high_pred[0]*100}","s2":f"{high_pred[1]*100}","s3":f"{high_pred[2]*100}","s4":f"{high_pred[3]*100}","s5":f"{high_pred[4]*100}","s6":f"{high_pred[5]*100}",}
        answer.append(high_percent)
        return answer
    except Exception as e:
        print(f"error occurred in display_results function: {str(e)}")
        return {"response":f"error occurred in display_results function: {str(e)}"}

async def model_predict(employee_json, realtime_json):
    try:
        years_to_retire = employee_json["years_to_retire"]
        salary = employee_json["salary"]
        investment_amount = employee_json["investment_amount"]
        current_savings = employee_json["current_savings"]
        debt = employee_json["debt"]
        other_expenses = employee_json["other_expenses"]
        number_of_dependents = employee_json["number_of_dependents"]
        current_invested_amount = employee_json["current_invested_amount"]
        bank = employee_json["bank"]

        loaded_model = load_model('./arif/investment_recommendation.h5')
        preprocessor = joblib.load('./arif/preprocessor_pipeline.pkl')

        features = ['years_to_retire', 'salary', 'investment_amount', 'current_savings', 'debt',
                    'other_expenses', 'number_of_dependents', 'current_invested_amount']
        new_employee = pd.DataFrame([[years_to_retire, salary, investment_amount, current_savings, debt, other_expenses, number_of_dependents, current_invested_amount]], columns=features)
        
        # Preprocess the new data
        new_employee_processed = preprocessor.transform(new_employee)
        
        predicted_low, predicted_mid, predicted_high = loaded_model.predict(new_employee_processed)

        # Display the prediction results
        ans = await display_results(predicted_low[0], predicted_mid[0], predicted_high[0])

        low_percent = ans[0]
        mid_percent = ans[1]
        high_percent = ans[2]
        scaler = joblib.load('scaler.pkl')
        model_high = joblib.load('model_high.pkl')
        model_mid = joblib.load('model_mid.pkl')
        model_low = joblib.load('model_low.pkl')
        inp = np.array([[years_to_retire, investment_amount]])
        scaled_inp = scaler.transform(inp)

        goal_low = model_low.predict(scaled_inp)
        goal_low = np.expm1(goal_low)
        goal_low = float(goal_low[0])
        # low_json['goal_low'] = goal_low
        print(f"\nGoal low: {goal_low}")

        goal_mid = model_mid.predict(scaled_inp)
        goal_mid = np.expm1(goal_mid)
        goal_mid = float(goal_mid[0])
        # mid_json['goal_mid'] = goal_mid
        print(f"\nGoal mid: {goal_mid}\nType of: {type(goal_mid)}")

        goal_high = model_high.predict(scaled_inp)
        goal_high = np.expm1(goal_high)
        goal_high = float(goal_high[0])
        # high_json['goal_high'] = goal_high
        print(f"\nGoal high: {goal_high}")

        categorized_stocks = await stock_cluster_gen(float(investment_amount/2),realtime_json["stock"])
        low_json = await dealing_low(investment_amount, years_to_retire, bank, realtime_json, copy.deepcopy(categorized_stocks), goal_low, low_percent)
        mid_json = await dealing_mid(investment_amount, years_to_retire, bank, realtime_json, copy.deepcopy(categorized_stocks), goal_mid, mid_percent)
        high_json =  await dealing_high(investment_amount,years_to_retire,bank,realtime_json, copy.deepcopy(categorized_stocks), goal_high, high_percent)

        fin_resp = []
        fin_resp.append(low_json)
        fin_resp.append(mid_json)
        fin_resp.append(high_json)
        return fin_resp
    except Exception as e:
        print(f"error occurred in model_predict function: {str(e)}")
        return {"response": f"error occurred in model_predict function: {str(e)}"}
    

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
        if not categorized_stocks["High"] and not categorized_stocks["Medium"] and not categorized_stocks["Low"]:
            return None,None,None
        return categorized_stocks,max_price,quantity
    except Exception as e:
        print(f"error ocurred in stock_values_giver {str(e)}")

async def crypto_values_giver(crypto_data, investment_amount):
    try:
        affordable_cryptos = []
        for crypto in crypto_data:
            last_price = float(crypto['last_price'].replace(',', ''))
            if last_price <= investment_amount:
                affordable_cryptos.append(crypto)
        categorized_cryptos = {'High':[],'Medium':[],'Low':[]}
        for crypto in affordable_cryptos:
            change_percent = abs(float(crypto['changePercent']))
            if change_percent > 6:
                crypto["quantity"] = float(investment_amount/float(crypto['last_price'].replace(',', '')))
                categorized_cryptos['High'].append(crypto)
            elif 3<=change_percent<=6:
                crypto["quantity"] = float(investment_amount/float(crypto['last_price'].replace(',', '')))
                categorized_cryptos['Medium'].append(crypto)
            else:
                crypto["quantity"] = float(investment_amount/float(crypto['last_price'].replace(',', '')))
                categorized_cryptos['Low'].append(crypto)
            for category in categorized_cryptos:
                categorized_cryptos[category] = sorted(categorized_cryptos[category], key=lambda x: x['profit_percentage'], reverse=True)[:3]
        if not categorized_cryptos["High"] and categorized_cryptos["Medium"] and categorized_cryptos["Low"]:
            return None
        return categorized_cryptos
    except Exception as e:
        print(f"error occurred in crypto_values_giver function: {str(e)}")

async def calculate_rd_maturity(monthly_deposit, tenure_months, annual_interest_rate):
    try:
        total_principal = monthly_deposit * tenure_months
        quarterly_interest_rate = annual_interest_rate / 4 / 100
        quarters = tenure_months // 3
        maturity_amount = 0

        for i in range(1, tenure_months + 1):
            remaining_months = tenure_months - i + 1
            quarters_remaining = remaining_months // 3
            maturity_amount += monthly_deposit * (1 + quarterly_interest_rate) ** quarters_remaining

        profit = maturity_amount - total_principal
        answer=[]
        answer.append(maturity_amount)
        return maturity_amount, profit
    except Exception as e:
        print(f"error occurred in calculate_rd_maturity function: {str(e)}")

async def recurrent_deposit_give(investment_amount,years,bank,recurrent_deposit_main):
    try:
        if investment_amount>=100:
            tenure_months=None
            if years>10:
                tenure_months = 10*12
            else:
                tenure_months = years*12
            interest_rate = recurrent_deposit_main[bank]
            # Split the string to get the individual numbers
            rates = interest_rate.split(' - ')
            # Convert the split strings to float
            rate_min = float(rates[0])
            rate_max = float(rates[1])
            # Calculate the mean of the range
            annual_interest_rate = (rate_min + rate_max) / 2
            maturity_amount, profit = await calculate_rd_maturity(investment_amount, tenure_months, annual_interest_rate)

            answer = {
                "investment_amount":investment_amount,
                "maturity_amount": maturity_amount,
                "profit_amount": profit,
                "tenure_months":tenure_months,
                "interest_rate":annual_interest_rate
            }
            return answer
        else:
            return None
    except Exception as e:
        print(f"error while running recurrent_deposit_give function {str(e)}")

async def shortlist_properties(max_estimated_emi):
    try:
        with open('properties.json', 'r') as f:
            property_data = json.load(f)
        property_data = property_data["property"]
        shortlisted_properties = [property for property in property_data if property['estimated_emi'] <= max_estimated_emi]
        print("\n\nShortlisted_properties are:\n",shortlisted_properties)

        if not shortlisted_properties:
            return None,None
        max = 0
        for property in shortlisted_properties:
            if property['estimated_emi'] >= max:
                max = property['estimated_emi']
        return shortlisted_properties[:3],max
    except Exception as e:
        print(f"An error occurred in shortlist_properties fn {str(e)}")

async def shortlist_bonds(bond_data, max_price):
    try:
        shortlisted_bonds = []
        bond_price = None
        max = 0
        quantity = 0
        for bond in bond_data:
            if bond['frequency'] == 'QUARTERLY':
                bond_price = float(re.sub(r'[₹,\s]', '', bond['price']))/4
            elif bond['frequency'] == "SEMI ANNUALLY":
                bond_price = float(re.sub(r'[₹,\s]', '', bond['price']))/6
            elif bond['frequency'] == "ANNUALLY":
                bond_price = float(re.sub(r'[₹,\s]', '', bond['price']))/12
            elif bond['frequency'] == "MONTHLY":
                bond_price = float(re.sub(r'[₹,\s]', '', bond['price']))
            else:
                bond_price = 10000000000
            if bond_price <= max_price:
                if bond_price>=max:
                    max = bond_price
                    quantity = int(max_price/bond_price)
                shortlisted_bonds.append(bond)
        if not shortlisted_bonds:
            return None,None,None
        return shortlisted_bonds[:3],max,quantity
    except Exception as e:
        print(f"error occurred in shortlist_bonds fn {str(e)}")

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

async def dealing_low(investment_amount,years,bank,realtime_json,categorized_stocks,goal,low_percent):
    try:
        low_amounts = {
            's1': round(float(investment_amount * float(low_percent["s1"])) /100 ,2),
            's2': round(float(investment_amount * float(low_percent["s2"])) /100, 2),
            's3': round(float(investment_amount * float(low_percent["s3"])) /100, 2),
            's4': round(float(investment_amount * float(low_percent["s4"])) /100, 2),
            's5': round(float(investment_amount * float(low_percent["s5"])) /100, 2),
            's6': round(float(investment_amount * float(low_percent["s6"])) /100, 2)
        }

        # Adjust amounts to ensure they sum up to the original investment amount
        total_amount = sum(low_amounts.values())
        amount_difference = round(investment_amount - total_amount, 2)
        low_amounts["s3"] += amount_difference  # Adjust recurrent amount to make the sum exact

        print("befor changes:\n",low_amounts)

        stock_data, stock_maxprice, stock_quantity = await stock_values_giver(low_amounts["s1"], categorized_stocks)
        crypto_data = await crypto_values_giver(realtime_json["crypto"], low_amounts["s2"])
        property_data,property_maxemi = await shortlist_properties(low_amounts["s4"])
        bond_data,bond_maxprice,bond_quantity = await shortlist_bonds(realtime_json["bond"],low_amounts["s6"])
        gold_data,gold_quantity = await gold_give(realtime_json["gold"],years,low_amounts["s5"])
        

        if stock_data is None:
            low_amounts["s3"] = round((low_amounts["s3"]+low_amounts['s1']), 2)
            low_amounts["s1"] = 0
            print("Stock is not supported here so adding it's amount to RD")
        else:
            stock_difference_amount = round((low_amounts["s1"] - (stock_quantity*stock_maxprice)),2)
            low_amounts["s3"] = round((low_amounts["s3"]+stock_difference_amount),2)
            low_amounts["s1"] = low_amounts["s1"]-stock_difference_amount

        if crypto_data is None:
            low_amounts["s3"] = round((low_amounts["s3"]+low_amounts['s2']),2)
            low_amounts["s2"] = 0

        if property_data is None:
            low_amounts["s3"] = round((low_amounts["s3"]+low_amounts['s4']),2)
            low_amounts["s4"] = 0
            print("Property is not supported here so adding it's amount to RD")
        else:
            property_difference_amount = round((low_amounts["s4"] - (property_maxemi)),2)
            low_amounts["s3"] = round((low_amounts["s3"]+property_difference_amount),2)
            low_amounts["s4"] = low_amounts["s4"]-property_difference_amount

        if bond_data is None:
            low_amounts["s3"] = round((low_amounts["s3"]+low_amounts['s6']),2)
            low_amounts["s6"] = 0
            print("Bond is not supported here so adding it's amount to RD")
        else:
            bond_difference_amount = round((low_amounts["s6"] - (bond_quantity*bond_maxprice)),2)
            low_amounts["s3"] = round((low_amounts["s3"]+bond_difference_amount),2)
            low_amounts["s6"] = low_amounts["s6"]-bond_difference_amount

        if gold_data is None: 
            low_amounts["s3"] = round((low_amounts["s3"]+low_amounts['s5']),2)
            low_amounts["s5"] = 0
            print("Gold is not supported here so adding it's amount to RD")
        else:
            gold_difference_amount = round((low_amounts["s5"] - (gold_quantity*realtime_json["gold"])),2)
            low_amounts["s3"] = round((low_amounts["s3"]+gold_difference_amount),2)
            low_amounts["s5"] = low_amounts["s5"]-gold_difference_amount

        recurrent_data = await recurrent_deposit_give(low_amounts["s3"],years,bank,realtime_json["recurrent_deposit"])

        print("after changes:\n",low_amounts)

        stock_percent_div = round((float(low_amounts["s1"]/investment_amount)*100),2)
        crypto_percent_div = round((float(low_amounts["s2"]/investment_amount)*100),2)
        recurrent_percent_div = round((float(low_amounts["s3"]/investment_amount)*100),2)
        property_percent_div = round((float(low_amounts["s4"]/investment_amount)*100),2)
        gold_percent_div = round((float(low_amounts["s5"]/investment_amount)*100),2)
        bond_percent_div = round((float(low_amounts["s6"]/investment_amount)*100),2)

        # Adjust percentages to ensure they sum up to 100%
        total_percent = stock_percent_div + crypto_percent_div + recurrent_percent_div + property_percent_div + gold_percent_div + bond_percent_div
        percent_difference = round(100 - total_percent, 2)
        recurrent_percent_div += percent_difference  # Adjust recurrent percentage to make the sum exact
        recurrent_percent_div = round(recurrent_percent_div,2)

        low_json = {
            "stock": stock_data,
            "stock_amount": low_amounts["s1"],
            "stock_percent": stock_percent_div,
            "crypto": crypto_data,
            "crypto_amount": low_amounts["s2"],
            "crypto_percent": crypto_percent_div,
            "recurrent": recurrent_data,
            "recurrent_amount": low_amounts["s3"],
            "recurrent_percent": recurrent_percent_div,
            "property": property_data,
            "property_amount": low_amounts["s4"],
            "property_percent": property_percent_div,
            "gold": gold_data,
            "gold_amount": low_amounts["s5"],        
            "gold_percent": gold_percent_div,
            "bond": bond_data,
            "bond_amount": low_amounts["s6"],
            "bond_percent": bond_percent_div,
            "goal_savings": goal
        }

        # Recalculate total amounts to ensure they sum up to investment amount
        total_amount = sum([low_json[key + "_amount"] for key in ["stock", "crypto", "recurrent", "property", "gold", "bond"]])
        amount_difference = round(investment_amount - total_amount, 2)
        low_json["recurrent_amount"] += amount_difference  # Adjust recurrent amount to make the sum exact
        low_json["recurrent_amount"] = round(low_json["recurrent_amount"],2)
        
        return low_json
    except Exception as e:
        print(f"error occured while running dealing_low function {str(e)}")   
        return {"response":f"error occured while running dealing_low function {str(e)}"}


async def dealing_mid(investment_amount, years, bank, realtime_json, categorized_stocks, goal, mid_percent):
    try:
        mid_amounts = {
            's1': round(float(investment_amount * float(mid_percent["s1"])) / 100, 2),
            's2': round(float(investment_amount * float(mid_percent["s2"])) / 100, 2),
            's3': round(float(investment_amount * float(mid_percent["s3"])) / 100, 2),
            's4': round(float(investment_amount * float(mid_percent["s4"])) / 100, 2),
            's5': round(float(investment_amount * float(mid_percent["s5"])) / 100, 2),
            's6': round(float(investment_amount * float(mid_percent["s6"])) / 100, 2)
        }

        # Adjust amounts to ensure they sum up to the original investment amount
        total_amount = sum(mid_amounts.values())
        amount_difference = round(investment_amount - total_amount, 2)
        mid_amounts["s3"] += amount_difference  # Adjust recurrent amount to make the sum exact

        print("Before changes:\n", mid_amounts)
        
        stock_data, stock_maxprice, stock_quantity = await stock_values_giver(mid_amounts["s1"], categorized_stocks)
        property_data, property_maxemi = await shortlist_properties(mid_amounts["s4"])
        bond_data, bond_maxprice, bond_quantity = await shortlist_bonds(realtime_json["bond"], mid_amounts["s6"])
        gold_data, gold_quantity = await gold_give(realtime_json["gold"], years, mid_amounts["s5"])

        if stock_data is None:
            mid_amounts["s3"] += round(mid_amounts['s1'] / 2, 2)
            mid_amounts["s2"] += round(mid_amounts['s1'] / 2, 2)
            mid_amounts["s1"] = 0
            print("Stock is not supported here so adding its amount to RD")
        else:
            stock_difference_amount = round(mid_amounts["s1"] - (stock_quantity * stock_maxprice), 2)
            mid_amounts["s3"] += round(stock_difference_amount / 2, 2)
            mid_amounts["s2"] += round(stock_difference_amount / 2, 2)
            mid_amounts["s1"] -= stock_difference_amount

        if property_data is None:
            mid_amounts["s3"] += round(mid_amounts['s4'] / 2, 2)
            mid_amounts["s2"] += round(mid_amounts['s4'] / 2, 2)
            mid_amounts["s4"] = 0
            print("Property is not supported here so adding its amount to RD")
        else:
            property_difference_amount = round(mid_amounts["s4"] - property_maxemi, 2)
            mid_amounts["s3"] += round(property_difference_amount / 2, 2)
            mid_amounts["s2"] += round(property_difference_amount / 2, 2)
            mid_amounts["s4"] -= property_difference_amount

        if bond_data is None:
            mid_amounts["s3"] += round(mid_amounts['s6'] / 2, 2)
            mid_amounts["s2"] += round(mid_amounts['s6'] / 2, 2)
            mid_amounts["s6"] = 0
            print("Bond is not supported here so adding its amount to RD")
        else:
            bond_difference_amount = round(mid_amounts["s6"] - (bond_quantity * bond_maxprice), 2)
            mid_amounts["s3"] += round(bond_difference_amount / 2, 2)
            mid_amounts["s2"] += round(bond_difference_amount / 2, 2)
            mid_amounts["s6"] -= bond_difference_amount

        if gold_data is None:
            mid_amounts["s3"] += round(mid_amounts['s5'] / 2, 2)
            mid_amounts["s2"] += round(mid_amounts['s5'] / 2, 2)
            mid_amounts["s5"] = 0
            print("Gold is not supported here so adding its amount to RD")
        else:
            gold_difference_amount = round(mid_amounts["s5"] - (gold_quantity * realtime_json["gold"]), 2)
            mid_amounts["s3"] += round(gold_difference_amount / 2, 2)
            mid_amounts["s2"] += round(gold_difference_amount / 2, 2)
            mid_amounts["s5"] -= gold_difference_amount

        recurrent_data = await recurrent_deposit_give(mid_amounts["s3"], years, bank, realtime_json["recurrent_deposit"])
        crypto_data = await crypto_values_giver(realtime_json["crypto"], mid_amounts["s2"])

        print("After changes:\n", mid_amounts)

        stock_percent_div = round(mid_amounts["s1"] / investment_amount * 100, 2)
        crypto_percent_div = round(mid_amounts["s2"] / investment_amount * 100, 2)
        recurrent_percent_div = round(mid_amounts["s3"] / investment_amount * 100, 2)
        property_percent_div = round(mid_amounts["s4"] / investment_amount * 100, 2)
        gold_percent_div = round(mid_amounts["s5"] / investment_amount * 100, 2)
        bond_percent_div = round(mid_amounts["s6"] / investment_amount * 100, 2)

        # Adjust percentages to ensure they sum up to 100%
        total_percent = stock_percent_div + crypto_percent_div + recurrent_percent_div + property_percent_div + gold_percent_div + bond_percent_div
        percent_difference = round(100 - total_percent, 2)
        recurrent_percent_div += percent_difference  # Adjust recurrent percentage to make the sum exact
        recurrent_percent_div = round(recurrent_percent_div,2)



        mid_json = {
            "stock": stock_data,
            "stock_amount": mid_amounts["s1"],
            "stock_percent": stock_percent_div,
            "crypto": crypto_data,
            "crypto_amount": mid_amounts["s2"],
            "crypto_percent": crypto_percent_div,
            "recurrent": recurrent_data,
            "recurrent_amount": mid_amounts["s3"],
            "recurrent_percent": recurrent_percent_div,
            "property": property_data,
            "property_amount": mid_amounts["s4"],
            "property_percent": property_percent_div,
            "gold": gold_data,
            "gold_amount": mid_amounts["s5"],        
            "gold_percent": gold_percent_div,
            "bond": bond_data,
            "bond_amount": mid_amounts["s6"],
            "bond_percent": bond_percent_div,
            "goal_savings": goal
        }

        # Recalculate total amounts to ensure they sum up to investment amount
        total_amount = sum([mid_json[key + "_amount"] for key in ["stock", "crypto", "recurrent", "property", "gold", "bond"]])
        amount_difference = round(investment_amount - total_amount, 2)
        mid_json["recurrent_amount"] += amount_difference  # Adjust recurrent amount to make the sum exact
        mid_json["recurrent_amount"] = round(mid_json["recurrent_amount"],2)

        return mid_json
    except Exception as e:
        print(f"Error occurred while running dealing_mid function: {str(e)}")   
        return {"response": f"Error occurred while running dealing_mid function: {str(e)}"}



async def dealing_high(investment_amount,years,bank,realtime_json, categorized_stocks,goal,high_percent):
    try:
        high_amounts = {
            's1': round((float(investment_amount*(float(high_percent["s1"])))/100),2),
            's2': round((float(investment_amount*(float(high_percent["s2"])))/100),2),
            's3': round((float(investment_amount*(float(high_percent["s3"])))/100),2),
            's4': round((float(investment_amount*(float(high_percent["s4"])))/100),2),
            's5': round((float(investment_amount*(float(high_percent["s5"])))/100),2),
            's6': round((float(investment_amount*(float(high_percent["s6"])))/100),2)
        }

        # Adjust amounts to ensure they sum up to the original investment amount
        total_amount = sum(high_amounts.values())
        amount_difference = round(investment_amount - total_amount, 2)
        high_amounts["s3"] += amount_difference  # Adjust recurrent amount to make the sum exact

        print("before changes:\n",high_amounts)

        stock_data,stock_maxprice,stock_quantity = await stock_values_giver(high_amounts["s1"],categorized_stocks)
        recurrent_data = await recurrent_deposit_give(high_amounts["s3"],years,bank,realtime_json["recurrent_deposit"])
        property_data,property_maxemi = await shortlist_properties(high_amounts["s4"])
        bond_data,bond_maxprice,bond_quantity = await shortlist_bonds(realtime_json["bond"],high_amounts["s6"])

        gold_data,gold_quantity = await gold_give(realtime_json["gold"],years,high_amounts["s5"])
        

        if stock_data is None:
            high_amounts["s2"] = round((high_amounts["s2"]+high_amounts['s1']),2)
            high_amounts["s1"] = 0
            print("Stock is not supported here so adding it's amount to RD")
        else:
            stock_difference_amount = round((high_amounts["s1"] - (stock_quantity*stock_maxprice)),2)
            high_amounts["s2"] = round((high_amounts["s2"]+stock_difference_amount),2)
            high_amounts["s1"] = high_amounts["s1"]-stock_difference_amount
        
        if recurrent_data is None:
            high_amounts["s2"] = round((high_amounts["s2"]+high_amounts['s3']),2)
            high_amounts["s3"] = 0
        
        if property_data is None:
            high_amounts["s2"] = round((high_amounts["s2"]+high_amounts['s4']),2)
            high_amounts["s4"] = 0
            print("Property is not supported here so adding it's amount to RD")
        else:
            property_difference_amount = round((high_amounts["s4"] - (property_maxemi)),2)
            high_amounts["s2"] = round((high_amounts["s2"]+property_difference_amount),2)
            high_amounts["s4"] = high_amounts["s4"]-property_difference_amount
        
        if bond_data is None:
            high_amounts["s2"] = round((high_amounts["s2"]+high_amounts['s6']),2)
            high_amounts["s6"] = 0
            print("Bond is not supported here so adding it's amount to RD")
        else:
            bond_difference_amount = round((high_amounts["s6"] - (bond_quantity*bond_maxprice)),2)
            high_amounts["s2"] = round((high_amounts["s2"]+bond_difference_amount),2)
            high_amounts["s6"] = high_amounts["s6"]-bond_difference_amount
        
        if gold_data is None: 
            high_amounts["s2"] = round((high_amounts["s2"]+high_amounts['s5']),2)
            high_amounts["s5"] = 0
            print("Gold is not supported here so adding it's amount to RD")
        else:
            gold_difference_amount = round((high_amounts["s5"] - (gold_quantity*realtime_json["gold"])),2)
            high_amounts["s2"] = round((high_amounts["s2"]+gold_difference_amount),2)
            high_amounts["s5"] = high_amounts["s5"]-gold_difference_amount
        
        crypto_data = await crypto_values_giver(realtime_json["crypto"],high_amounts["s2"])
        
        print("after changes:\n",high_amounts)

        stock_percent_div = round((float(high_amounts["s1"]/investment_amount)*100),2)
        crypto_percent_div = round((float(high_amounts["s2"]/investment_amount)*100),2)
        recurrent_percent_div = round((float(high_amounts["s3"]/investment_amount)*100),2)
        property_percent_div = round((float(high_amounts["s4"]/investment_amount)*100),2)
        gold_percent_div = round((float(high_amounts["s5"]/investment_amount)*100),2)
        bond_percent_div = round((float(high_amounts["s6"]/investment_amount)*100),2)

        # Adjust percentages to ensure they sum up to 100%
        total_percent = stock_percent_div + crypto_percent_div + recurrent_percent_div + property_percent_div + gold_percent_div + bond_percent_div
        percent_difference = round(100 - total_percent, 2)
        recurrent_percent_div += percent_difference  # Adjust recurrent percentage to make the sum exact
        recurrent_percent_div = round(recurrent_percent_div,2)

        high_json = {
            "stock": stock_data,
            "stock_amount": high_amounts["s1"],
            "stock_percent": stock_percent_div,
            "crypto": crypto_data,
            "crypto_amount": high_amounts["s2"],
            "crypto_percent": crypto_percent_div,
            "recurrent": recurrent_data,
            "recurrent_amount": high_amounts["s3"],
            "recurrent_percent": recurrent_percent_div,
            "property": property_data,
            "property_amount": high_amounts["s4"],
            "property_percent": property_percent_div,
            "gold": gold_data,
            "gold_amount": high_amounts["s5"],        
            "gold_percent": gold_percent_div,
            "bond": bond_data,
            "bond_amount": high_amounts["s6"],
            "bond_percent": bond_percent_div,
            "goal_savings":goal
        }

        # Recalculate total amounts to ensure they sum up to investment amount
        total_amount = sum([high_json[key + "_amount"] for key in ["stock", "crypto", "recurrent", "property", "gold", "bond"]])
        amount_difference = round(investment_amount - total_amount, 2)
        high_json["recurrent_amount"] += amount_difference  # Adjust recurrent amount to make the sum exact
        high_json["recurrent_amount"] = round(high_json["recurrent_amount"],2)
        return high_json
    except Exception as e:
        print(f"error occured while running dealing_high function {str(e)}")   
        return {"response":f"error occured while running dealing_high function {str(e)}"}