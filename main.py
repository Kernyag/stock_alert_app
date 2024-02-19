import requests
import os
from dotenv import load_dotenv
import json
from datetime import date, timedelta
from twilio.rest import Client

STOCK = "AAPL"
COMPANY_NAME = "Apple"

load_dotenv()
STOCK_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")

stock_parameters ={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_KEY
}
stock_api_endpoint ="https://www.alphavantage.co/query"

# Get the stock data
"""response = requests.get(stock_api_endpoint, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]"""
# Saving a file for debugging
"""with open("daily_AAPL_debug.json", mode="w") as file:
    json.dump(stock_data, file, indent=4)"""
# For debugging
with open("daily_AAPL_debug.json", mode="r") as file:
    stock_data = json.load(file)

stock_data = [value for (key, value) in stock_data.items()]

# Get the closing values
yesterday_close_value = float(stock_data[0]["4. close"])
before_yesterday_close_value = float(stock_data[1]["4. close"])

# Calculate diff
close_value_diff_usd = yesterday_close_value - before_yesterday_close_value
diff_in_percentage = round((close_value_diff_usd / before_yesterday_close_value) * 100, 2)

change_sign = ""
if diff_in_percentage > 0:
    change_sign = "🔺"
else:
    change_sign = "🔻"

# Check news if stock is changed by 5% if yes send the TOP 3 article
news_api_parameters = {
    "q": COMPANY_NAME,
    "searchIn": "title",
    "language": "en",
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY
}

news_api_endpoint = "https://newsapi.org/v2/everything"

if abs(diff_in_percentage) > 5:
    response = requests.get(news_api_endpoint, params=news_api_parameters)
    response.raise_for_status()
    news_data = response.json()["articles"]

    for i in range(3):
        article_title = news_data[i]["title"]
        article_description = news_data[i]["description"]
        article_link = news_data[i]["url"]
        articel_to_send = (f"{STOCK}: {change_sign}{diff_in_percentage}%\n"
            f"Headline: {article_title}\n"
            f"Brief: {article_description}\n"
            f"url: {article_link}"
            )
        
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
                    body=articel_to_send,
                    from_='+17622215342',
                    to='+36209439294'
                )
        print(message.status)
else:
    print("No big price movement")

