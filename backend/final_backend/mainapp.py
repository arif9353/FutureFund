from fastapi import FastAPI, Request
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

@app.get('/fetchdata')
async def fetch_data():
    try:
        print("fetching data")
        #location="Delhi"
        #average_cpi = 0.046433252043303265
        #years = 10
        crypto_data = await get_crypto_data()
        stock_data, stock_main_data = await get_stock_data('https://m.moneycontrol.com/more_market.php')
        recurrent_deposit_data = await get_bank_names_for_RD()
        gold_data = await fetch_real_time_gold_price_alpha_vantage()
        #gold_data = 18010.96
        bond_data = await get_bonds_data('https://www.indiabonds.com/search/?limit=100&switch_one=radio-grid')
        #property_data = await property_json(location, average_cpi, years)
        with open('properties.json', 'r') as f:
            property_data = json.load(f)
        json_main = {
            "stock": stock_main_data,
            "crypto":crypto_data[1],
            "recurrent_deposit": recurrent_deposit_data,
            "gold":gold_data,
            "bond":bond_data[1],
        }
        return JSONResponse(content={'stock_data': stock_data, 'crypto_data': crypto_data[0], 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data,'bond_data': bond_data[0], 'details':json_main,'property_data':property_data["property"][:25], 'success': True}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':'failure while trying', 'success': False}, status_code=500)
    
#'stock_data': stock_data, 'crypto_data': crypto_data, 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data,'bond_data': bond_data,          

@app.post('/model')
async def main_model(request:Request):
    try:
        data = await request.json()
        json_data = {'years_to_retire': data["years_to_retire"], 'salary': data["salary"], 'investment_amount': data["investment_amount"], 'current_savings': data["current_savings"], 'debt': data["debt"], 'other_expenses': data["other_expenses"], 'number_of_dependents': data["number_of_dependents"], 'current_invested_amount': data["current_invested_amount"], 'bank': data["bank"]} 
        ans = await model_predict(json_data,data["details"])
        return JSONResponse(content={'low_json':ans[0],'mid_json':ans[1],'high_json':ans[2]},status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':f'failure while trying {str(e)}', 'success': False}, status_code=500)