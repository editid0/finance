from dotenv import load_dotenv
import os, requests, csv

# Load environment variables from .env file
load_dotenv()

POLYGON_KEY = os.getenv("POLYGON_KEY")
if not POLYGON_KEY:
    raise ValueError("POLYGON_KEY is not set in the environment variables.")

headers = {"Authorization": f"Bearer {POLYGON_KEY}"}

data = []
with open("dump.csv", mode="r") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

# Remove non-USD rows
data = [row for row in data if row["Currency (Price / share)"] == "USD"]

stock_amounts = {}

for row in data:
    action = row["Action"]  # Market buy, Market sell
    time = row["Time"]  # 2025-06-03 15:39:38.225
    ticker = row["Ticker"]  # AAPL
    shares = float(row["No. of shares"])  # 0.2000000000
    price = float(row["Price / share"])  # 202.5300000000
    if stock_amounts.get(ticker) is None:
        stock_amounts[ticker] = {}
    if action == "Market buy":
        stock_amounts[ticker]["shares"] = (
            stock_amounts[ticker].get("shares", 0) + shares
        )
        stock_amounts[ticker]["total_cost"] = stock_amounts[ticker].get(
            "total_cost", 0
        ) + (shares * price)
    elif action == "Market sell":
        stock_amounts[ticker]["shares"] = (
            stock_amounts[ticker].get("shares", 0) - shares
        )
        stock_amounts[ticker]["total_cost"] = stock_amounts[ticker].get(
            "total_cost", 0
        ) - (shares * price)
# Remove tickers with no shares left
stock_amounts = {
    ticker: info for ticker, info in stock_amounts.items() if info["shares"] > 0
}

# Round down total cost, and shares to maximum of 8 decimal places
for ticker, info in stock_amounts.items():
    info["total_cost"] = round(info["total_cost"], 8)
    info["shares"] = round(info["shares"], 8)

print("Stock amounts:")
for ticker, info in stock_amounts.items():
    print(
        f"Ticker: {ticker}, Shares: {info['shares']}, Total Cost: {info['total_cost']}"
    )


# params = {"ticker": "AAPL", "limit": 1}

# response = requests.get(
#     "https://api.polygon.io/v3/reference/dividends", headers=headers, params=params
# )

# data = response.json()
# print(data)
