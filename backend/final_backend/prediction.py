import joblib
from tensorflow.keras.models import load_model
from tensorflow.keras.losses import CategoricalCrossentropy

import pandas as pd
import numpy as np
import copy
from dealing_allocation import dealing_low,dealing_high,dealing_mid
from stock import stock_cluster_gen
import json


async def omit_assets(allocations, omit):
    # Asset indices corresponding to s1, s2, ..., s6
    asset_indices = {'s1': 0, 's2': 1, 's3': 2, 's4': 3, 's5': 4, 's6': 5}

    # Set the values of omitted assets to 0
    for asset in omit:
        allocations[0][asset_indices[asset]] = 0

    # Calculate the sum of remaining assets
    remaining_sum = allocations.sum(axis=1, keepdims=True)

    # Redistribute the values of omitted assets proportionally to the remaining assets
    allocations = allocations / remaining_sum

    # Convert the final allocation to a percentage scale (0-100%)
    allocations_percentage = allocations 
    
    return allocations_percentage

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
        print(employee_json)
        years_to_retire = employee_json["years_to_retire"]
        print(type(years_to_retire))
        salary = employee_json["salary"]
        print(type(salary))
        investment_amount = employee_json["investment_amount"]
        print(type(investment_amount))
        current_savings = employee_json["current_savings"]
        print(type(current_savings))
        debt = employee_json["debt"]
        print(type(debt))
        other_expenses = employee_json["other_expenses"]
        print(type(other_expenses))
        number_of_dependents = employee_json["number_of_dependents"]
        print(type(number_of_dependents))
        current_invested_amount = employee_json["current_invested_amount"]
        print(type(current_invested_amount))
        bank = employee_json["bank"]
        print(type(bank))
        stock_allocation_bool = employee_json["stock_allocation_bool"]
        print(type(stock_allocation_bool))
        crypto_allocation_bool = employee_json["crypto_allocation_bool"]
        print(type(crypto_allocation_bool))
        bond_allocation_bool = employee_json["bond_allocation_bool"]
        print(type(stock_allocation_bool))
        recurrent_deposit_allocation_bool = employee_json["recurrent_deposit_allocation_bool"]
        print(type(recurrent_deposit_allocation_bool))
        property_allocation_bool = employee_json["property_allocation_bool"]
        print(type(property_allocation_bool))
        gold_allocation_bool = employee_json["gold_allocation_bool"]
        print(type(gold_allocation_bool))
        print("This iss gold allocation",gold_allocation_bool)

        
        # Load the model with custom objects
        loaded_model = load_model('finals_allocation.h5')

        preprocessor = joblib.load('finals_preprocessor.pkl')

        features = ['years_to_retire', 'salary', 'investment_amount', 'current_savings', 'debt',
                    'other_expenses', 'number_of_dependents', 'current_invested_amount','s1','s2','s3','s4','s5','s6']
        new_employee = pd.DataFrame([[years_to_retire, salary, investment_amount, current_savings, debt, other_expenses, number_of_dependents, current_invested_amount,stock_allocation_bool,
                                      crypto_allocation_bool,recurrent_deposit_allocation_bool,property_allocation_bool,gold_allocation_bool,bond_allocation_bool]], columns=features)
        
        # Preprocess the new data
        new_employee_processed = preprocessor.transform(new_employee)
        
        predicted_low, predicted_mid, predicted_high = loaded_model.predict(new_employee_processed)
        print("\n\nthis is predicted_low\n\n",type(predicted_low))
        # Display the prediction results
        boolean_list = []
        if stock_allocation_bool == 0:
            boolean_list.append('s1')
        if crypto_allocation_bool == 0:
            boolean_list.append('s2')        
        if recurrent_deposit_allocation_bool == 0:
            boolean_list.append('s3')        
        if property_allocation_bool == 0:
            boolean_list.append('s4')
        if gold_allocation_bool == 0:
            boolean_list.append('s5')
        if bond_allocation_bool == 0:
            boolean_list.append('s6')
        
        low_per = await omit_assets(np.array(predicted_low),boolean_list)
        mid_per = await omit_assets(np.array(predicted_mid),boolean_list)
        high_per = await omit_assets(np.array(predicted_high),boolean_list)
        ans = await display_results(np.array(low_per[0]), np.array(mid_per[0]), np.array(high_per[0]))
        
        low_percent = ans[0]
        mid_percent = ans[1]
        high_percent = ans[2]

        print("\n\nThis is:\n",high_percent)

        scaler = joblib.load('scaler_for_goal.pkl')
        model_high = joblib.load('new_model_high.pkl')
        model_mid = joblib.load('new_model_mid.pkl')
        model_low = joblib.load('new_model_low.pkl')


        categorized_stocks = await stock_cluster_gen(float(investment_amount/2),realtime_json["stock_data"])
        low_json = await dealing_low(investment_amount, years_to_retire, bank, realtime_json, copy.deepcopy(categorized_stocks), low_percent)
        mid_json = await dealing_mid(investment_amount, years_to_retire, bank, realtime_json, copy.deepcopy(categorized_stocks), mid_percent)
        high_json =  await dealing_high(investment_amount,years_to_retire,bank,realtime_json, copy.deepcopy(categorized_stocks), high_percent)
        
        profit_low = low_json["overall_profit"]
        print("\nProfit for low:\n",profit_low)
        input_fun_low = [years_to_retire, investment_amount, debt, profit_low, current_savings]
        scaled_inp_low = scaler.fit_transform([input_fun_low])

        goal_low = model_low.predict(scaled_inp_low)
        goal_low = np.expm1(goal_low)
        goal_low = float(goal_low[0])
        # low_json['goal_low'] = goal_low
        print(f"\nGoal low: {goal_low}")

        profit_mid = mid_json["overall_profit"]
        print("\nProfit for mid:\n",profit_mid)
        input_fun_mid = [years_to_retire, investment_amount, debt, profit_mid, current_savings]
        scaled_inp_mid = scaler.fit_transform([input_fun_mid])

        goal_mid = model_mid.predict(scaled_inp_mid)
        goal_mid = np.expm1(goal_mid)
        goal_mid = float(goal_mid[0])
        # mid_json['goal_mid'] = goal_mid
        print(f"\nGoal mid: {goal_mid}\nType of: {type(goal_mid)}")

        profit_high = high_json["overall_profit"]
        print("\nProfit for high:\n",profit_high)
        input_fun_high = [years_to_retire, investment_amount, debt, profit_high, current_savings]
        scaled_inp_high = scaler.fit_transform([input_fun_high])

        goal_high = model_high.predict(scaled_inp_high)
        goal_high = np.expm1(goal_high)
        goal_high = float(goal_high[0])
        # high_json['goal_high'] = goal_high
        print(f"\nGoal high: {goal_high}")

        low_json["goal_savings"] = goal_low
        mid_json["goal_savings"] = goal_mid
        high_json["goal_savings"] = goal_high
        fin_resp = []
        fin_resp.append(low_json)
        fin_resp.append(mid_json)
        fin_resp.append(high_json)
        return fin_resp
    except Exception as e:
        print(f"error occurred in model_predict function: {str(e)}")
        return {"response": f"error occurred in model_predict function: {str(e)}"}