import joblib
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import re
import json
import copy
from stock_gen import stock_cluster_gen, stock_values_giver
from gold import get_gold_for_main
from prediction import crypto_values_giver, calculate_rd_maturity, recurrent_deposit_give, shortlist_properties, shortlist_bonds, gold_give

async def dealing_low(investment_amount,years,bank,realtime_json,categorized_stocks, goal):
    try:
        global low_percent
        low_amounts = {
            's1': float(investment_amount*(float(low_percent["s1"])))/100,
            's2': float(investment_amount*(float(low_percent["s2"])))/100,
            's3': float(investment_amount*(float(low_percent["s3"])))/100,
            's4': float(investment_amount*(float(low_percent["s4"])))/100,
            's5': float(investment_amount*(float(low_percent["s5"])))/100,
            's6':float(investment_amount*(float(low_percent["s6"])))/100
        }
        print("befor changes:\n",low_amounts)
        stock_data,stock_maxprice,stock_quantity = await stock_values_giver(low_amounts["s1"],categorized_stocks)
        crypto_data = await crypto_values_giver(realtime_json["crypto"],low_amounts["s2"])
        property_data,property_maxemi = await shortlist_properties(realtime_json["property"],low_amounts["s4"])
        bond_data,bond_maxprice,bond_quantity = await shortlist_bonds(realtime_json["bond"],low_amounts["s6"])
        gold_data,gold_quantity = await gold_give(realtime_json["gold"],years,low_amounts["s5"])
        

        if stock_data is None:
            low_amounts["s3"]=low_amounts["s3"]+low_amounts['s1']
            low_amounts["s1"] = 0
            print("Stock is not supported here so adding it's amount to RD")
        else:
            stock_difference_amount = low_amounts["s1"] - (stock_quantity*stock_maxprice)
            low_amounts["s3"]=low_amounts["s3"]+stock_difference_amount
            low_amounts["s1"]=low_amounts["s1"]-stock_difference_amount

        if crypto_data is None:
            low_amounts["s3"]=low_amounts["s3"]+low_amounts['s2']
            low_amounts["s2"] = 0

        if property_data is None:
            low_amounts["s3"]=low_amounts["s3"]+low_amounts['s4']
            low_amounts["s4"] = 0
            print("Property is not supported here so adding it's amount to RD")
        else:
            property_difference_amount = low_amounts["s4"] - (property_maxemi)
            low_amounts["s3"]=low_amounts["s3"]+property_difference_amount
            low_amounts["s4"]=low_amounts["s4"]-property_difference_amount

        if bond_data is None:
            low_amounts["s3"]=low_amounts["s3"]+low_amounts['s6']
            low_amounts["s6"] = 0
            print("Bond is not supported here so adding it's amount to RD")
        else:
            bond_difference_amount = low_amounts["s6"] - (bond_quantity*bond_maxprice)
            low_amounts["s3"] = low_amounts["s3"]+bond_difference_amount
            low_amounts["s6"] = low_amounts["s6"]-bond_difference_amount

        if gold_data is None: 
            low_amounts["s3"]=low_amounts["s3"]+low_amounts['s5']
            low_amounts["s5"] = 0
            print("Gold is not supported here so adding it's amount to RD")
        else:
            gold_difference_amount = low_amounts["s5"] - (gold_quantity*realtime_json["gold"])
            low_amounts["s3"] = low_amounts["s3"]+gold_difference_amount
            low_amounts["s5"] = low_amounts["s5"]-gold_difference_amount

        recurrent_data = await recurrent_deposit_give(low_amounts["s3"],years,bank,realtime_json["recurrent_deposit"])

        print("after changes:\n",low_amounts)

        stock_percent_div = float(low_amounts["s1"]/investment_amount)*100
        crypto_percent_div = float(low_amounts["s2"]/investment_amount)*100
        recurrent_percent_div = float(low_amounts["s3"]/investment_amount)*100
        property_percent_div = float(low_amounts["s4"]/investment_amount)*100
        gold_percent_div = float(low_amounts["s5"]/investment_amount)*100
        bond_percent_div = float(low_amounts["s6"]/investment_amount)*100

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
            "goal": goal
        }

        return low_json
    except Exception as e:
        print(f"error occured while running dealing_low function {str(e)}")   
        return {"response":f"error occured while running dealing_low function {str(e)}"}

async def dealing_mid(investment_amount,years,bank,realtime_json,categorized_stocks, goal):
    try:
        global mid_percent
        mid_amounts = {
            's1': float(investment_amount*(float(mid_percent["s1"])))/100,
            's2': float(investment_amount*(float(mid_percent["s2"])))/100,
            's3': float(investment_amount*(float(mid_percent["s3"])))/100,
            's4': float(investment_amount*(float(mid_percent["s4"])))/100,
            's5': float(investment_amount*(float(mid_percent["s5"])))/100,
            's6':float(investment_amount*(float(mid_percent["s6"])))/100
        }
        print("befor changes:\n",mid_amounts)
        stock_data,stock_maxprice,stock_quantity = await stock_values_giver(mid_amounts["s1"],categorized_stocks)
        property_data,property_maxemi = await shortlist_properties(realtime_json["property"],mid_amounts["s4"])
        bond_data,bond_maxprice,bond_quantity = await shortlist_bonds(realtime_json["bond"],mid_amounts["s6"])
        gold_data,gold_quantity = await gold_give(realtime_json["gold"],years,mid_amounts["s5"])
        

        if stock_data is None:
            mid_amounts["s3"]=mid_amounts["s3"]+(mid_amounts['s1']/2)
            mid_amounts["s2"]=mid_amounts["s2"]+(mid_amounts['s1']/2)
            mid_amounts["s1"] = 0
            print("Stock is not supported here so adding it's amount to RD")
        else:
            stock_difference_amount = mid_amounts["s1"] - (stock_quantity*stock_maxprice)
            mid_amounts["s3"]=mid_amounts["s3"]+(stock_difference_amount/2)
            mid_amounts["s2"]=mid_amounts["s2"]+(stock_difference_amount/2)
            mid_amounts["s1"]=mid_amounts["s1"]-stock_difference_amount

        if property_data is None:
            mid_amounts["s3"]=mid_amounts["s3"]+(mid_amounts['s4']/2)
            mid_amounts["s2"]=mid_amounts["s2"]+(mid_amounts['s4']/2)
            mid_amounts["s4"] = 0
            print("Property is not supported here so adding it's amount to RD")
        else:
            property_difference_amount = mid_amounts["s4"] - (property_maxemi)
            mid_amounts["s3"]=mid_amounts["s3"]+(property_difference_amount/2)
            mid_amounts["s2"]=mid_amounts["s2"]+(property_difference_amount/2)
            mid_amounts["s4"]=mid_amounts["s4"]-property_difference_amount

        if bond_data is None:
            mid_amounts["s3"]=mid_amounts["s3"]+(mid_amounts['s6']/2)
            mid_amounts["s2"]=mid_amounts["s2"]+(mid_amounts['s6']/2)
            mid_amounts["s6"] = 0
            print("Bond is not supported here so adding it's amount to RD")
        else:
            bond_difference_amount = mid_amounts["s6"] - (bond_quantity*bond_maxprice)
            mid_amounts["s3"] = mid_amounts["s3"]+(bond_difference_amount/2)
            mid_amounts["s2"] = mid_amounts["s2"]+(bond_difference_amount/2)
            mid_amounts["s6"] = mid_amounts["s6"]-bond_difference_amount

        if gold_data is None: 
            mid_amounts["s3"]=mid_amounts["s3"]+(mid_amounts['s5']/2)
            mid_amounts["s2"]=mid_amounts["s2"]+(mid_amounts['s5']/2)
            mid_amounts["s5"] = 0
            print("Gold is not supported here so adding it's amount to RD")
        else:
            gold_difference_amount = mid_amounts["s5"] - (gold_quantity*realtime_json["gold"])
            mid_amounts["s3"] = mid_amounts["s3"]+(gold_difference_amount/2)
            mid_amounts["s2"] = mid_amounts["s2"]+(gold_difference_amount/2)
            mid_amounts["s5"] = mid_amounts["s5"]-gold_difference_amount

        recurrent_data = await recurrent_deposit_give(mid_amounts["s3"],years,bank,realtime_json["recurrent_deposit"])
        crypto_data = await crypto_values_giver(realtime_json["crypto"],mid_amounts["s2"])


        print("after changes:\n",mid_amounts)

        stock_percent_div = float(mid_amounts["s1"]/investment_amount)*100
        crypto_percent_div = float(mid_amounts["s2"]/investment_amount)*100
        recurrent_percent_div = float(mid_amounts["s3"]/investment_amount)*100
        property_percent_div = float(mid_amounts["s4"]/investment_amount)*100
        gold_percent_div = float(mid_amounts["s5"]/investment_amount)*100
        bond_percent_div = float(mid_amounts["s6"]/investment_amount)*100

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
            "goal": goal
        }

        return mid_json
    except Exception as e:
        print(f"error occured while running dealing_low function {str(e)}")   
        return {"response":f"error occured while running dealing_low function {str(e)}"}

async def dealing_high(investment_amount,years,bank,realtime_json, categorized_stocks, goal):
    try:
        global high_percent

        high_amounts = {
            's1': float(investment_amount*(float(high_percent["s1"])))/100,
            's2': float(investment_amount*(float(high_percent["s2"])))/100,
            's3': float(investment_amount*(float(high_percent["s3"])))/100,
            's4': float(investment_amount*(float(high_percent["s4"])))/100,
            's5': float(investment_amount*(float(high_percent["s5"])))/100,
            's6':float(investment_amount*(float(high_percent["s6"])))/100
        }

        print("before changes:\n",high_amounts)
        print("investment for stocks in high\n",high_amounts["s1"])
        stock_data,stock_maxprice,stock_quantity = await stock_values_giver(high_amounts["s1"],categorized_stocks)
        recurrent_data = await recurrent_deposit_give(high_amounts["s3"],years,bank,realtime_json["recurrent_deposit"])
        property_data,property_maxemi = await shortlist_properties(realtime_json["property"],high_amounts["s4"])
        bond_data,bond_maxprice,bond_quantity = await shortlist_bonds(realtime_json["bond"],high_amounts["s6"])
        print("gold data in high")
        print(realtime_json["gold"])
        print(years)
        print(high_amounts["s5"])
        gold_data,gold_quantity = await gold_give(realtime_json["gold"],years,high_amounts["s5"])
        

        if stock_data is None:
            high_amounts["s2"]=high_amounts["s2"]+high_amounts['s1']
            high_amounts["s1"] = 0
            print("Stock is not supported here so adding it's amount to RD")
        else:
            stock_difference_amount = high_amounts["s1"] - (stock_quantity*stock_maxprice)
            high_amounts["s2"]=high_amounts["s2"]+stock_difference_amount
            high_amounts["s1"]=high_amounts["s1"]-stock_difference_amount
        
        if recurrent_data is None:
            high_amounts["s2"]=high_amounts["s2"]+high_amounts['s3']
            high_amounts["s3"] = 0
        
        if property_data is None:
            high_amounts["s2"]=high_amounts["s2"]+high_amounts['s4']
            high_amounts["s4"] = 0
            print("Property is not supported here so adding it's amount to RD")
        else:
            property_difference_amount = high_amounts["s4"] - (property_maxemi)
            high_amounts["s2"]=high_amounts["s2"]+property_difference_amount
            high_amounts["s4"]=high_amounts["s4"]-property_difference_amount
        
        if bond_data is None:
            high_amounts["s2"]=high_amounts["s2"]+high_amounts['s6']
            high_amounts["s6"] = 0
            print("Bond is not supported here so adding it's amount to RD")
        else:
            bond_difference_amount = high_amounts["s6"] - (bond_quantity*bond_maxprice)
            high_amounts["s2"] = high_amounts["s2"]+bond_difference_amount
            high_amounts["s6"] = high_amounts["s6"]-bond_difference_amount
        
        if gold_data is None: 
            high_amounts["s2"]=high_amounts["s2"]+high_amounts['s5']
            high_amounts["s5"] = 0
            print("Gold is not supported here so adding it's amount to RD")
        else:
            gold_difference_amount = high_amounts["s5"] - (gold_quantity*realtime_json["gold"])
            high_amounts["s2"] = high_amounts["s2"]+gold_difference_amount
            high_amounts["s5"] = high_amounts["s5"]-gold_difference_amount
        
        crypto_data = await crypto_values_giver(realtime_json["crypto"],high_amounts["s2"])
        
        print("after changes:\n",high_amounts)

        stock_percent_div = float(high_amounts["s1"]/investment_amount)*100
        crypto_percent_div = float(high_amounts["s2"]/investment_amount)*100
        recurrent_percent_div = float(high_amounts["s3"]/investment_amount)*100
        property_percent_div = float(high_amounts["s4"]/investment_amount)*100
        gold_percent_div = float(high_amounts["s5"]/investment_amount)*100
        bond_percent_div = float(high_amounts["s6"]/investment_amount)*100

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
            "goal": goal
        }
        
        return high_json
    except Exception as e:
        print(f"error occured while running dealing_high function {str(e)}")   
        return {"response":f"error occured while running dealing_high function {str(e)}"}
   