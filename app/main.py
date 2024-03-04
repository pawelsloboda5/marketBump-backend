from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import requests
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from polygon import RESTClient
from typing import List, Optional
import pytz
import uvicorn
from streamBot import client, get_most_recent_message
import asyncio

app = FastAPI()

discord_api_key = 'MTIxNDEwNjA0NjQ2MTkwNjk2NA.GeChRC.69zbzxWARdhoantscV_LzSYMJeeM5eJuN_w8PA'
polygon_api_key = 'XLHdBEwveKc6WmYDA7orsTl6soIG_cPb'
client = RESTClient(polygon_api_key)


# Define the Eastern Timezone
eastern = pytz.timezone('US/Eastern')

# Get the current time in UTC and convert it to Eastern Time
now_utc = datetime.now(pytz.utc)
now_eastern = now_utc.astimezone(eastern)

# Initialize today as the current date
today = now_eastern.date()

# Check if it's Monday before 9:30 AM
if now_eastern.weekday() == 0 and now_eastern.hour < 9:
    # Adjust to the previous Friday
    today -= timedelta(days=3)
# Check if it's Saturday or Sunday
elif now_eastern.weekday() == 6:  # Sunday
    today -= timedelta(days=2)
elif now_eastern.weekday() == 5:  # Saturday
    today -= timedelta(days=1)

# Convert to ISO format
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
    day_data = client.get_daily_open_close_agg(ticker, today)
    if day_data:
        return day_data
    

def fetch_news_data(ticker: str, client):
    news_data_url = f"https://api.polygon.io/v2/reference/news?limit=3&order=descending&sort=published_utc&ticker={ticker}&published_utc.gte={today}&apiKey={polygon_api_key}"
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



     



