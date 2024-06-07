from fastapi import FastAPI, Form, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from stock import get_stock_data
from crypto import get_crypto_data
from recurrent_deposit import get_bank_names_for_RD
from bonds import get_bonds_data
from property import property_json
from gold import fetch_real_time_gold_price_alpha_vantage
from prediction import model_predict
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

Json_Main = None

@app.get('/fetchdata')
async def fetch_data():
    try:
        global Json_Main
        print("fetching data")
        #location="Delhi"
        #average_cpi = 0.046433252043303265
        #years = 10
        crypto_data = await get_crypto_data()
        stock_data, stock_main_data = await get_stock_data('https://m.moneycontrol.com/more_market.php')
        recurrent_deposit_data = await get_bank_names_for_RD()
        #gold_data = await get_gold_data()
        gold_data = 18010.96
        bond_data = await get_bonds_data('https://www.indiabonds.com/search/?limit=100&switch_one=radio-grid')
        #property_data = await property_json(location, average_cpi, years)
        with open('properties.json', 'r') as f:
            property_data = json.load(f)
        Json_Main = {
            "stock": stock_main_data,
            "crypto":crypto_data[1],
            "recurrent_deposit": recurrent_deposit_data,
            "gold":gold_data,
            "bond":bond_data[1],
        }
        return JSONResponse(content={'stock_data': stock_data, 'crypto_data': crypto_data[0], 'recurrent_deposit': recurrent_deposit_data,  'gold_data': gold_data,'bond_data': bond_data[0], 'property_data':property_data["property"][:25], 'details':Json_Main,'success': True}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':'failure while trying', 'success': False}, status_code=500)
    
#'stock_data': stock_data, 'crypto_data': crypto_data, 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data,'bond_data': bond_data,          

@app.post('/model')
async def main_model(details:str=Form(...),years_to_retire: str = Form(...),salary: str=Form(...),investment_amount: str=Form(...),current_savings: str=Form(...),debt: str=Form(...),other_expenses: str=Form(...),number_of_dependents: str=Form(...),current_invested_amount: str=Form(...),bank: str=Form(...)):
    try:
        global Json_Main
        json_data = {'years_to_retire': int(years_to_retire), 'salary': float(salary), 'investment_amount': float(investment_amount), 'current_savings': float(current_savings), 'debt': float(debt), 'other_expenses': float(other_expenses), 'number_of_dependents': int(number_of_dependents), 'current_invested_amount': float(current_invested_amount), 'bank': bank} 
        ans = await model_predict(json_data,details)
        return JSONResponse(content={'low_json':ans[0],'mid_json':ans[1],'high_json':ans[2]},status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':f'failure while trying {str(e)}', 'success': False}, status_code=500)