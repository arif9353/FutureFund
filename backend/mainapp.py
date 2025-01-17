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

@app.get('/fetchdata')
async def fetch_data():
    try:
        print("fetching data")
        #location="Delhi"
        #average_cpi = 0.046433252043303265
        #years = 10
        crypto_data = await get_crypto_data()
        stock_data = await get_stock_data('https://m.moneycontrol.com/more_market.php')
        recurrent_deposit_data = await get_bank_names_for_RD()
        #gold_data = await get_gold_data()
        gold_data = 18010.96
        bond_data = await get_bonds_data('https://www.indiabonds.com/search/?limit=100&switch_one=radio-grid')
        #property_data = await property_json(location, average_cpi, years)
        stock_main_data = await get_stock_data_main('https://m.moneycontrol.com/more_market.php')
        json_main = {
            "stock": stock_main_data,
            "crypto":crypto_data[1],
            "recurrent_deposit": recurrent_deposit_data,
            "gold":gold_data,
            "bond":bond_data[1],
        }
        return JSONResponse(content={'stock_data': stock_data, 'crypto_data': crypto_data[0], 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data,'bond_data': bond_data[0], 'details':json_main,'success': True}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':'failure while trying', 'success': False}, status_code=500)
    
#'stock_data': stock_data, 'crypto_data': crypto_data, 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data,'bond_data': bond_data,          

@app.post('/model')
async def main_model(request:Request):
    try:
        data = await request.json()
        json_data = {'location': data["location"], 'years_to_retire': data["years_to_retire"], 'salary': data["salary"], 'investment_amount': data["investment_amount"], 'current_savings': data["current_savings"], 'debt': data["debt"], 'other_expenses': data["other_expenses"], 'number_of_dependents': data["number_of_dependents"], 'current_invested_amount': data["current_invested_amount"], 'bank': data["bank"]} 
        ans = await model_predict(json_data,data["details"])
        return JSONResponse(content={'low_json':ans[0],'mid_json':ans[1],'high_json':ans[2]},status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':f'failure while trying {str(e)}', 'success': False}, status_code=500)