from fastapi import FastAPI,File,UploadFile,Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from get_investment_data import get_stock_data, get_crypto_data, get_bank_names_for_RD, get_gold_data

app = FastAPI()

@app.get('/fetchdata')
async def fetch_data():
    try:
        crypto_data = await get_crypto_data('https://www.moneycontrol.com/crypto-market/market-movers/top-cryptos/inr')
        stock_data = await get_stock_data('https://m.moneycontrol.com/more_market.php')
        recurrent_deposit_data = await get_bank_names_for_RD()
        gold_data = await get_gold_data()
        return JSONResponse(content={'stock': stock_data, 'crypto': crypto_data, 'recurrent_deposit': recurrent_deposit_data, 'gold_data': gold_data, 'success': True}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':'failure while trying', 'success': False}, status_code=500)
    
