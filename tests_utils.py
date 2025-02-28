import unittest
from unittest.mock import patch, mock_open
import json
from src.utils import get_currency_and_stock_data  # Замените на имя вашего модуля

# Мок для чтения файла user_settings.json
user_settings_mock = {
    'user_currencies': ['USD', 'EUR'],
    'user_stocks': ['AAPL', 'AMZN', 'TSLA']  # Обновленный список акций
}

# Мок для ответа API курсов валют
currency_response_mock = {
    "Realtime Currency Exchange Rate": {
        "5. Exchange Rate": "75.50"
    }
}

# Мок для ответа API курсов акций
stock_response_mock = {
    "Global Quote": {
        "05. price": "150.00"
    }
}


@patch('requests.get')
@patch('os.getenv')
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps(user_settings_mock))
def test_get_currency_and_stock_data(mock_file, mock_getenv, mock_get):
    # Настройка моков
    mock_getenv.return_value = 'test_api_key'

    # Используем бесконечный генератор для side_effect
    from itertools import cycle
    mock_get.return_value.json.side_effect = cycle([
        currency_response_mock,  # Ответ для USD
        currency_response_mock,  # Ответ для EUR
        stock_response_mock,  # Ответ для AAPL
        stock_response_mock,  # Ответ для AMZN
        stock_response_mock  # Ответ для TSLA
    ])

    # Вызов тестируемой функции
    result = get_currency_and_stock_data('test_api_key')

    # Преобразуем результат в словарь для удобства проверки
    result_dict = json.loads(result)

    # Проверка структуры результата
    assert "currency_rates" in result_dict, "Отсутствует ключ 'currency_rates'"
    assert "stock_prices" in result_dict, "Отсутствует ключ 'stock_prices'"

    # Проверка количества валют и акций
    assert len(result_dict["currency_rates"]) == 2, "Ожидалось 2 валюты"
    assert len(result_dict["stock_prices"]) == 3, "Ожидалось 3 акции"  # Обновлено ожидание

    # Проверка структуры данных для валют
    for currency in result_dict["currency_rates"]:
        assert "currency" in currency, "Отсутствует ключ 'currency'"
        assert "rate" in currency, "Отсутствует ключ 'rate'"

    # Проверка структуры данных для акций
    for stock in result_dict["stock_prices"]:
        assert "stock" in stock, "Отсутствует ключ 'stock'"
        assert "price" in stock, "Отсутствует ключ 'price'"


# Запуск теста
if __name__ == "__main__":
    test_get_currency_and_stock_data()
    print("Тест пройден успешно!")