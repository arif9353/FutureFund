from fastapi import FastAPI,File,UploadFile,Form, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from get_data import get_stock_advice, get_top_cryptos

app = FastAPI()

@app.get('/fetchdata')
async def fetch_data():
    try:
        # crypto_data = await get_top_cryptos('https://www.moneycontrol.com/crypto-market/market-movers/top-cryptos/inr')
        stock_data = await get_stock_advice('https://m.moneycontrol.com/markets/stock-advice/')
        return JSONResponse(content={'stock': stock_data, 'success': True}, status_code=200)
    except Exception as e:
        return JSONResponse(content={'message':'failure while trying', 'success': False}, status_code=500)
    

    # 'crypto': crypto_data, 