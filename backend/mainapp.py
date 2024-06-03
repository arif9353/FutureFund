from fastapi import FastAPI,File,UploadFile,Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from get_investment_data import get_bonds_data, get_stock_data, get_crypto_data, get_bank_names_for_RD, get_gold_data, get_stock_data_main
from property import property_json
from prediction import model_predict
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

Json_Main = None
#Stock_Main = None

@app.get('/fetchdata')
async def fetch_data():
    try:
        global Json_Main
        print("fetching data")
        location="Delhi"
        average_cpi = 0.046433252043303265
        years = 10
        crypto_data = await get_crypto_data()
        stock_data = await get_stock_data('https://m.moneycontrol.com/more_market.php')
        recurrent_deposit_data = await get_bank_names_for_RD()
        gold_data = await get_gold_data()
        bond_data = await get_bonds_data('https://www.indiabonds.com/search/?limit=100&switch_one=radio-grid')
        property_data = await property_json(location, average_cpi, years)
        stock_main_data = await get_stock_data_main('https://m.moneycontrol.com/more_market.php')
        Json_Main = {
            "stock": stock_main_data,
            "crypto":crypto_data[1],
            "recurrent_deposit": recurrent_deposit_data,
            "gold":gold_data,
            "bond":bond_data[1],
            "property": property_data
        }
        return JSONResponse(content={'stock_data': stock_data, 'crypto_data': crypto_data[0], 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data,'bond_data': bond_data[0], 'property_data':property_data,'success': True}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':'failure while trying', 'success': False}, status_code=500)
    
#'stock_data': stock_data, 'crypto_data': crypto_data, 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data,'bond_data': bond_data,          

@app.get('/model')
async def main_model():
    try:
        global Json_Main
        json_data = {'location': 'Mumbai', 'years_to_retire': 30, 'salary': 175000, 'investment_amount': 100000, 'current_savings': 100000, 'debt': 30000, 'other_expenses': 30000, 'number_of_dependents': 3, 'current_invested_amount': 0, 'bank': 'sbi_bank'} 
        print(Json_Main)
        ans = model_predict(json_data,Json_Main)
        return JSONResponse(content={'low_json':ans},status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':f'failure while trying {str(e)}', 'success': False}, status_code=500)