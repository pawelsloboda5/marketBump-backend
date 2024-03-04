from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import requests
from fastapi.middleware.cors import CORSMiddleware
import schedule
import datetime
from polygon import RESTClient

polygon_api_key = 'XLHdBEwveKc6WmYDA7orsTl6soIG_cPb'
client = RESTClient(polygon_api_key)
app = FastAPI()

#Variables needed to be fetched from polygon.io
#Stock data:
#ticker, day open, day close, day high, day low, volume, scrape realtime quote
#News data:
#ticker, title, url, summary, author, keywords

#Get todays date but go back to friday if it is the weekend
today = datetime.date.today()
if today.strftime("%w") == "0":
    today = today - datetime.timedelta(days=2)
elif today.strftime("%w") == "6":
    today = today - datetime.timedelta(days=1)
today = today.isoformat()

news = client.list_ticker_news('AAPL', today)
day_open = client.get_daily_open_close_agg('AAPL', today)
open = day_open.open
print(day_open.open)
print(news)

