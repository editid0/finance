from dotenv import load_dotenv
import os, requests

# Load environment variables from .env file
load_dotenv()

POLYGON_KEY = os.getenv("POLYGON_KEY")
if not POLYGON_KEY:
    raise ValueError("POLYGON_KEY is not set in the environment variables.")

headers = {"Authorization": f"Bearer {POLYGON_KEY}"}

params = {"ticker": "AAPL", "limit": 1}

response = requests.get(
    "https://api.polygon.io/v3/reference/dividends", headers=headers, params=params
)

data = response.json()
print(data)
