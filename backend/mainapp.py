from fastapi import FastAPI,File,UploadFile,Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from get_investment_data import get_bonds_data, get_stock_data, get_crypto_data, get_bank_names_for_RD, get_gold_data

app = FastAPI()

@app.get('/fetchdata')
async def fetch_data():
    try:
        crypto_data = await get_crypto_data()
        stock_data = await get_stock_data('https://m.moneycontrol.com/more_market.php')
        recurrent_deposit_data = await get_bank_names_for_RD()
        gold_data = await get_gold_data()
        bond_data = await get_bonds_data('https://www.indiabonds.com/search/?limit=100&switch_one=radio-grid')
        return JSONResponse(content={'stock_data': stock_data, 'crypto_data': crypto_data, 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data,'bond_data': bond_data, 'success': True}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':'failure while trying', 'success': False}, status_code=500)
    
#'stock': stock_data, 'crypto': crypto_data, 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data