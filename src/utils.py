import requests
import json


def get_financial_data(api_key):
    # Валюты для запроса (например, USD и EUR)
    currencies = ['USD', 'EUR']

    # Акции
    stocks = ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']

    financial_data = {}

    # Запрашиваем курсы валют
    currency_rates = []
    for currency in currencies:
        url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={currency}&to_currency=RUB&apikey={api_key}'

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

    # Запрашиваем курсы акций
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

    # Формирование финального JSON ответа
    financial_data.update({"currency_rates": currency_rates})
    financial_data.update({"stock_prices": stock_prices})

    json_data = json.dumps(financial_data, indent=4)

    return json_data


# Пример использования функции
if __name__ == "__main__":
    api_key = 'WJGZKPTYANGO2YD7'  # Замените на ваш реальный API ключ
    json_str = get_financial_data(api_key)
    print(json_str)