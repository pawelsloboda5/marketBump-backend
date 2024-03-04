from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import requests
from fastapi.middleware.cors import CORSMiddleware
import datetime
from polygon import RESTClient
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

polygon_api_key = 'XLHdBEwveKc6WmYDA7orsTl6soIG_cPb'
client = RESTClient(polygon_api_key)
app = FastAPI()

#Get todays date but go back to friday if it is the weekend
today = datetime.date.today()
if today.strftime("%w") == "0":
    today = today - datetime.timedelta(days=2)
elif today.strftime("%w") == "6":
    today = today - datetime.timedelta(days=1)
today = today.isoformat()

origins =[
    "https://marketbump-frontend.vercel.app",
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Adjust the origin as per your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Variables needed to be fetched from polygon.io
#Stock data:
#ticker, day open, day close, day high, day low, volume, scrape realtime quote
#News data:
#ticker, title, url, summary, author, keywords

def fetch_day_data(ticker: str, client):
    day_data_url = f"https://api.polygon.io/v1/open-close/{ticker}/{today}?adjusted=true&apiKey={polygon_api_key}"
    day_data = requests.get(day_data_url).json()
    
    if day_data:
        return day_data
    

def fetch_news_data(ticker: str, client):
    news_data_url = f"https://api.polygon.io/v2/reference/news?limit=9&order=descending&sort=published_utc&ticker={ticker}&published_utc.gte={today}&apiKey={polygon_api_key}"
    news_data = requests.get(news_data_url).json()

    if news_data:
        return news_data
  

@app.get("/api/stockData/{ticker}", response_class=JSONResponse)
def get_stock_day_data(ticker: str = "AMD"):
    day_data = fetch_day_data(ticker, client)

    if not day_data:
        return JSONResponse(content={"error": "Data could not be fetched"}, status_code=400)

    return {
        "ticker": ticker,
        "day_data": day_data,
    }

@app.get("/api/newsData/{ticker}", response_class=JSONResponse)
def get_stock_news(ticker: str = "AMD"):
    news_data = fetch_news_data(ticker, client)

    if not news_data:
        return JSONResponse(content={"error": "Data could not be fetched"}, status_code=400)
    # Ensure news_data is an array and extract it if it's nested within another object
    news_data = news_data.get('results', []) if isinstance(news_data, dict) else news_data

    return {
        "ticker": ticker,
        "news_data": news_data,
    }