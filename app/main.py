from fastapi import FastAPI, HTTPException, Request, WebSocket, WebSocketDisconnect, APIRouter
from fastapi.responses import JSONResponse, HTMLResponse
import requests
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from polygon import RESTClient
from typing import List, Optional
import discord
import pytz
import streamBot
from streamBot import retrieve_messages
from openAI import summarize_text

#1198802839217131580
#MjExMjcxMDg2MDQwNDE2MjU2.Gfjysr.QszGgFIoBxbU7cLWvcEcN29ZGIXDdpPYCtFWKE
#1193011030100557844
#MjExMjcxMDg2MDQwNDE2MjU2.GTaVqT.wmnEajKiytq0bvKvHsxm8hQShGHlaSP4JW7Ieg
app = FastAPI()
router = APIRouter()

app.include_router(router)
discord_api_key = 'MTIxNDEwNjA0NjQ2MTkwNjk2NA.GeChRC.69zbzxWARdhoantscV_LzSYMJeeM5eJuN_w8PA'
discord_auth_key = 'MjExMjcxMDg2MDQwNDE2MjU2.GTaVqT.wmnEajKiytq0bvKvHsxm8hQShGHlaSP4JW7Ieg'
channel_id = '1198802201355759737'
polygon_api_key = 'XLHdBEwveKc6WmYDA7orsTl6soIG_cPb'
openai_api_key = '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'
client = RESTClient(polygon_api_key)

eastern = pytz.timezone('US/Eastern')
now_utc = datetime.now(pytz.utc)
now_eastern = now_utc.astimezone(eastern)

today = now_eastern.date()

if now_eastern.weekday() == 0 and now_eastern.hour < 9:
    today -= timedelta(days=3)
elif now_eastern.weekday() == 6:  # Sunday
    today -= timedelta(days=2)
elif now_eastern.weekday() == 5:  # Saturday
    today -= timedelta(days=1)

today = today.isoformat()

origins =[
    "https://marketbump-frontend.vercel.app",
    "https://marketbump.io",
    "http://localhost:5173",
    "http://localhost:8000",
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
    url = f"https://api.polygon.io/v1/open-close/{ticker}/{today}?adjusted=true&apiKey={polygon_api_key}"
    day_data = requests.get(url).json()
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
    
     # Summarize each news article
    for article in news_data:
        article['description'] = summarize_text(article['description'])
    
    return {
        "ticker": ticker,
        "news_data": news_data,
    }

@app.get("/api/discord", response_class=JSONResponse)
def receive_message():
    messageData = retrieve_messages(channel_id, discord_auth_key)
    message = messageData[0]
    author = messageData[1]
    return {"message": message, 
            "author": author
            }



