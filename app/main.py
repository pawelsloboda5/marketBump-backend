from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import requests
from fastapi.middleware.cors import CORSMiddleware
import schedule
import datetime




app = FastAPI()
polygon_api_key = 'XLHdBEwveKc6WmYDA7orsTl6soIG_cPb'
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


def fetch_news_data(ticker: str = "AMD"):
    url = f"https://api.polygon.io/v2/reference/news?ticker={ticker}&apiKey={polygon_api_key}"
    response = requests.get(url)
    if response.status_code == 200:  # Success
        news_data = response.json()
        # Assuming you want to return the articles directly
        return news_data.get('results', [])  # Safely get 'results' or return empty list
    else:
        return []  # Return an empty list in case of an error
    
def fetch_stock_data(ticker: str = "AMD"):
    today = datetime.date.today().isoformat()  # Get today's date in YYYY-MM-DD format
    url = f"https://api.polygon.io/v1/open-close/{ticker}/{today}?adjusted=true&apiKey={polygon_api_key}"
    response = requests.get(url)
    if response.status_code == 200:  # Success
        stock_data = response.json()
        return {
            'open': stock_data.get('open'),
            'close': stock_data.get('close'),
            'volume': stock_data.get('volume'),
            'market_cap': stock_data.get('marketcap')
        }
    else:
        return []  # Return an empty list in case of an error
def fetch_stock_data_close(ticker: str = "AMD"):
    url = f"https://api.polygon.io/v1/open-close/{ticker}/2024-02-16?adjusted=true&apiKey={polygon_api_key}"
    response = requests.get(url)
    if response.status_code == 200:  # Success
        stock_data_close = response.json()
        return stock_data_close['close']
    else:
        return []  # Return an empty list in case of an error

def get_news(ticker: str = "AMD"):
    return fetch_news_data(ticker)

@app.get("/api/news/{ticker}", response_class=JSONResponse)
def get_stock_news(ticker: str = "AMD"):
    news_data = fetch_news_data(ticker)  # Call get_news function to fetch the data
    stock_data_open = fetch_stock_data(ticker)
    stock_data_close = fetch_stock_data_close(ticker)

    # Construct a JSON response structure
    response_content = {
        "ticker": ticker,
        "stock_data_open": stock_data_open,
        "stock_data_close": stock_data_close,  # Ensure this is structured correctly for JSON
        "news": news_data  # List of article dictionaries
    }

    return response_content
