import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()
current_dir = os.path.dirname(os.path.abspath(__file__))
user_settings_path = os.path.join(current_dir, '../user_settings.json')

with open(user_settings_path, 'r') as f:
    user_settings = json.load(f)

currencies = user_settings.get('user_currencies', [])
stocks = user_settings.get('user_stocks', [])

api_key = os.getenv('AV_SANDP500_API')


def get_currency_and_stock_data(api_key):
    '''Запрашивает по API данные курсов валют и акций и возвращает результат в json строке'''
    financial_data = {}

    currency_rates = []
    for currency in currencies:
        url = (f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency}'
               f'&to_currency=RUB&apikey={api_key}')

        try:
            response = requests.get(url)
            data = response.json()

            rate = float(data['Realtime Currency Exchange Rate']['5. Exchange Rate'])
            currency_rates.append({
                "currency": currency,
                "rate": round(rate, 2)
            })
        except KeyError:
            print(f"Ошибка при получении данных для валюты {currency}: {data}")

    stock_prices = []
    for ticker in stocks:
        url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={ticker}&apikey={api_key}'

        try:
            response = requests.get(url)
            data = response.json()

            price = float(data['Global Quote']['05. price'])
            stock_prices.append({
                "stock": ticker,
                "price": round(price, 2)
            })
        except KeyError:
            print(f"Ошибка при получении данных для акции {ticker}: {data}")

    financial_data.update({"currency_rates": currency_rates})
    financial_data.update({"stock_prices": stock_prices})

    json_data = json.dumps(financial_data, indent=4)

    return json_data


json_str = get_currency_and_stock_data(api_key)
print(json_str)
