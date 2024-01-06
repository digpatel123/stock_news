import requests
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.
import os
from twilio.rest import Client

# Stock Parameters
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
# Alpha Vantage
ALPHA_API_KEY = os.getenv("ALPHA_API_KEY")
ALPHA_ENDPOINT = "https://www.alphavantage.co/query"
# News API
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
# twilio account
twilio_account_sid = os.getenv("TWILIO_ACCOUNT_SID")
twilio_auth_token = os.getenv("TWILIO_AUTH_TOKEN")

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": ALPHA_API_KEY
}

response = requests.get(ALPHA_ENDPOINT, params=stock_params)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]

# Get yesterday's closing stock price
yesterday_data = data_list[0]
yesterday_closing_price = yesterday_data["4. close"]

# Get the day before yesterday's closing stock price
day_before_yesterday_data = data_list[1]
day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]

# Find the  difference
difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
up_down = None
if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# Work out the percentage difference in price between closing price yesterday and closing price the day
# after yesterday.
difference_percentage = (difference / float(yesterday_closing_price)) * 100
print(difference_percentage)

#If difference percentage is greater than 5 then print("Get News").
if abs(difference_percentage) > 5:
    print("Get News")

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 
news_params = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME
}

response = requests.get(NEWS_ENDPOINT, params=news_params)
data = response.json()["articles"][:3]


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 

# Format of the message
formatted_articles = [f"{STOCK}: {up_down}{difference_percentage}%\nHeadline: {article['title']}\nBrief: {article['description']}" for article in data]

for article in data:
    client = Client(twilio_account_sid, twilio_auth_token)
    message = client.messages.create(
        body= formatted_articles,
        from_='+1 555 555-5555',
        to='+1 555 555-5555')


