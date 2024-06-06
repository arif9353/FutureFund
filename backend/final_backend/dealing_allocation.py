from stock import stock_values_giver
from gold import gold_give
from crypto import crypto_values_giver 
from recurrent_deposit import calculate_rd_maturity, recurrent_deposit_give
from bonds import shortlist_bonds
from property import shortlist_properties

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

        stock_data, stock_maxprice, stock_quantity, stock_max_profit, stock_profit_quantity = await stock_values_giver(low_amounts["s1"], categorized_stocks)
        crypto_data, crypto_max_profit, crypto_max_quantity = await crypto_values_giver(realtime_json["crypto"], low_amounts["s2"])
        property_data,property_maxemi, property_max_profit = await shortlist_properties(low_amounts["s4"])
        bond_data, bond_maxprice, bond_quantity = await shortlist_bonds(realtime_json["bond"],low_amounts["s6"])
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

        overall_profit = 0
        if stock_data is not None:
            overall_profit+=(stock_profit_quantity*stock_max_profit) 
            print("overall profit is for stock data:\n",overall_profit)
        if crypto_data is not None:
            overall_profit+= (crypto_max_quantity*crypto_max_profit) 
            print("overall profit is for crypto data:\n",overall_profit) 
        if recurrent_data is not None:
            overall_profit+= (recurrent_data["profit_amount"]/recurrent_data["tenure_months"]) 
            print("overall profit is for recurrent data:\n",overall_profit) 
        if property_data is not None:
            overall_profit+= property_max_profit/240 
            print("overall profit is for property data:\n",overall_profit) 
        if bond_data is not None:
            overall_profit+= (float(bond_data[0]["bond_profit"].replace('₹', '').replace(',', '').strip())*bond_data[0]["quantity"]) 
            print("overall profit is for bond data:\n",overall_profit) 
        if gold_data is not None:
            overall_profit+=gold_data/(years*12) 
            print("overall profit is for gold data:\n",overall_profit)

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
            "gold_profit": gold_data,
            "gold_amount": low_amounts["s5"],        
            "gold_percent": gold_percent_div,
            "bond": bond_data,
            "bond_amount": low_amounts["s6"],
            "bond_percent": bond_percent_div,
            "goal_savings": goal,
            "overall_profit": overall_profit
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
        
        stock_data, stock_maxprice, stock_quantity, stock_max_profit, stock_profit_quantity = await stock_values_giver(mid_amounts["s1"], categorized_stocks)
        property_data, property_maxemi, property_max_profit = await shortlist_properties(mid_amounts["s4"])
        bond_data, bond_maxprice, bond_quantity = await shortlist_bonds(realtime_json["bond"], mid_amounts["s6"])
        gold_data, gold_quantity = await gold_give(realtime_json["gold"], years, mid_amounts["s5"])
        print("\n\nproperty_max_emi is:\n\n",property_maxemi)
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
        crypto_data,crypto_max_profit,crypto_max_quantity = await crypto_values_giver(realtime_json["crypto"], mid_amounts["s2"])

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

        overall_profit = 0
        if stock_data is not None:
            overall_profit+=(stock_profit_quantity*stock_max_profit) 
            print("overall profit is for stock data:\n",overall_profit)
        if crypto_data is not None:
            overall_profit+= (crypto_max_quantity*crypto_max_profit) 
            print("overall profit is for crypto data:\n",overall_profit) 
        if recurrent_data is not None:
            overall_profit+= (recurrent_data["profit_amount"]/recurrent_data["tenure_months"]) 
            print("overall profit is for recurrent data:\n",overall_profit) 
        if property_data is not None:
            overall_profit+= property_max_profit/240 
            print("overall profit is for property data:\n",overall_profit) 
        if bond_data is not None:
            overall_profit+= (float(bond_data[0]["bond_profit"].replace('₹', '').replace(',', '').strip())*bond_data[0]["quantity"]) 
            print("overall profit is for bond data:\n",overall_profit) 
        if gold_data is not None:
            overall_profit+=gold_data/(years*12) 
            print("overall profit is for gold data:\n",overall_profit)

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
            "gold_profit": gold_data,
            "gold_amount": mid_amounts["s5"],        
            "gold_percent": gold_percent_div,
            "bond": bond_data,
            "bond_amount": mid_amounts["s6"],
            "bond_percent": bond_percent_div,
            "goal_savings": goal,
            "overall_profit": overall_profit
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

        stock_data,stock_maxprice,stock_quantity, stock_max_profit, stock_profit_quantity = await stock_values_giver(high_amounts["s1"],categorized_stocks)
        recurrent_data = await recurrent_deposit_give(high_amounts["s3"],years,bank,realtime_json["recurrent_deposit"])
        property_data,property_maxemi, property_max_profit = await shortlist_properties(high_amounts["s4"])
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
        
        crypto_data, crypto_max_profit, crypto_max_quantity = await crypto_values_giver(realtime_json["crypto"],high_amounts["s2"])
        
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

        overall_profit = 0
        if stock_data is not None:
            overall_profit+=(stock_profit_quantity*stock_max_profit) 
            print("overall profit is for stock data:\n",overall_profit)
        if crypto_data is not None:
            overall_profit+= (crypto_max_quantity*crypto_max_profit) 
            print("overall profit is for crypto data:\n",overall_profit) 
        if recurrent_data is not None:
            overall_profit+= (recurrent_data["profit_amount"]/recurrent_data["tenure_months"]) 
            print("overall profit is for recurrent data:\n",overall_profit) 
        if property_data is not None:
            overall_profit+= property_max_profit/240 
            print("overall profit is for property data:\n",overall_profit) 
        if bond_data is not None:
            overall_profit+= (float(bond_data[0]["bond_profit"].replace('₹', '').replace(',', '').strip())*bond_data[0]["quantity"]) 
            print("overall profit is for bond data:\n",overall_profit) 
        if gold_data is not None:
            overall_profit+=gold_data/(years*12) 
            print("overall profit is for gold data:\n",overall_profit)

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
            "gold_profit": gold_data,
            "gold_amount": high_amounts["s5"],        
            "gold_percent": gold_percent_div,
            "bond": bond_data,
            "bond_amount": high_amounts["s6"],
            "bond_percent": bond_percent_div,
            "goal_savings":goal,
            "overall_profit": overall_profit
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
   