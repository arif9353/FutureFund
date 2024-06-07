import joblib
from tensorflow.keras.models import load_model
import pandas as pd
import numpy as np
import copy
from dealing_allocation import dealing_low,dealing_high,dealing_mid
from stock import stock_cluster_gen
import json


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

        loaded_model = load_model('./investment_recommendation_mih.h5')
        preprocessor = joblib.load('./preprocessor_pipeline.pkl')

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

        categorized_stocks = await stock_cluster_gen(float(investment_amount/2),realtime_json["stock_data"])
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