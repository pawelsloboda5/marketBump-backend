from fastapi import FastAPI
from fastapi.responses import JSONResponse, HTMLResponse
import requests
from fastapi.middleware.cors import CORSMiddleware




app = FastAPI()
polygon_api_key = 'XLHdBEwveKc6WmYDA7orsTl6soIG_cPb'

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://marketbump-frontend.vercel.app/"],  # Adjust the origin as per your React app's URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html>
        <head>
            <title>News API Home</title>
        </head>
        <body>
            <h1>Welcome to the News API</h1>
            <button id="loadNewsBtn">Load AMD News</button>
            <div id="newsContainer"></div>
            <script>
                document.getElementById('loadNewsBtn').addEventListener('click', function() {
                    fetch('https://api.polygon.io/v2/reference/news?ticker=AMD&apiKey=XLHdBEwveKc6WmYDA7orsTl6soIG_cPb')
                        .then(response => response.text())
                        .then(html => {
                            document.getElementById('newsContainer').innerHTML = html;
                        })
                        .catch(err => console.error(err));
                });
            </script>
        </body>
    </html>
    """


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
    url = f"https://api.polygon.io/v1/open-close/{ticker}/2024-02-16?adjusted=true&apiKey={polygon_api_key}"
    response = requests.get(url)
    if response.status_code == 200:  # Success
        stock_data_open = response.json()
        return stock_data_open['open']
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
