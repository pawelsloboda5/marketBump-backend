import requests
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
def test_get_stock_news():
    response = client.get("/api/news/AMD")
    assert response.status_code == 200
    assert "ticker" in response.json()
    assert response.json()["ticker"] == "AMD"
    print(response.json())
