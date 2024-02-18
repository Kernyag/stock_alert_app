import requests
import os
from dotenv import load_dotenv
import json
from datetime import date, timedelta

STOCK = "AAPL"
COMPANY_NAME = "Apple Inc"

load_dotenv()
STOCK_KEY = os.getenv("STOCK_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

stock_parameters ={
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_KEY
}
stock_api_endpoint ="https://www.alphavantage.co/query"
today = date.today()

# Check if it is Sunday of Monday
if today.weekday() == 0:
    yesterday = today - timedelta(days=3)
    before_yesterday = yesterday - timedelta(days=1)
elif today.weekday() == 6:
    yesterday = today - timedelta(days=2)
    before_yesterday = yesterday - timedelta(days=1)
else:
    yesterday = today - timedelta(days=1)
    before_yesterday = yesterday - timedelta(days=1)

yesterday = str(yesterday)
before_yesterday = str(before_yesterday)

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
"""response = requests.get(stock_api_endpoint, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()"""

with open("dummy_data.json", mode="r") as file:
    stock_data = json.load(file)

# Get the closing values
yesterday_close_value = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])
before_yesterday_close_value = float(stock_data["Time Series (Daily)"][before_yesterday]["4. close"])

# Calculate diff
close_value_diff_usd = yesterday_close_value - before_yesterday_close_value
diff_in_percentage = round((close_value_diff_usd / before_yesterday_close_value) * 100, 2)
print(diff_in_percentage)
if abs(diff_in_percentage) > 5:
    print("Get news")

# Saving a file for debugging
"""with open("daily_AAPL.json", mode="w") as file:
    json.dump(stock_data, file, indent=4)"""

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

news_api_parameters = {
    "q": "Apple",
    "from": "2024-02-15",
    "language": "en",
    "sortBy": "popularity",
    "apiKey": NEWS_API_KEY
}

news_api_endpoint = "https://newsapi.org/v2/everything"
response = requests.get(news_api_endpoint, params=news_api_parameters)
response.raise_for_status()
news_data = response.json()

message = []
for i in range(3):
    article_title = news_data["articles"][i]["title"]
    article_description = news_data["articles"][i]["description"]
    article_link = news_data["articles"][i]["url"]
    message.append(f"{article_title}\n"
        f"{article_description}\n"
        f"{article_link}"
        )



## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

