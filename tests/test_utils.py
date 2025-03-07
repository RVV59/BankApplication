from unittest.mock import patch, mock_open, Mock
import json
from src.utils import get_currency_and_stock_data


@patch('os.getenv')
# Mock для открытия файла user_settings.json
@patch('builtins.open', new_callable=mock_open, read_data=json.dumps({
    'user_currencies': ['USD', 'EUR'],
    'user_stocks': ['AAPL', 'AMZN', 'GOOGL', 'MSFT', 'TSLA']  # Все акции
}))
# Mock для requests.get
@patch('requests.get')
def test_get_currency_and_stock_data(mock_requests_get, mock_file, mock_getenv):
    mock_getenv.return_value = 'test_api_key'

    mock_response_currency = Mock()
    mock_response_currency.json.return_value = {
        'Realtime Currency Exchange Rate': {
            '5. Exchange Rate': '75.50'
        }
    }

    mock_response_stock = Mock()
    mock_response_stock.json.return_value = {
        'Global Quote': {
            '05. price': '150.00'
        }
    }

    mock_requests_get.side_effect = [
        mock_response_currency,  # Ответ для USD
        mock_response_currency,  # Ответ для EUR
        mock_response_stock,     # Ответ для AAPL
        mock_response_stock,     # Ответ для AMZN
        mock_response_stock,     # Ответ для GOOGL
        mock_response_stock,     # Ответ для MSFT
        mock_response_stock      # Ответ для TSLA
    ]

    result = get_currency_and_stock_data('test_api_key')

    expected_result = json.dumps({
        "currency_rates": [
            {"currency": "USD", "rate": 75.5},
            {"currency": "EUR", "rate": 75.5}
        ],
        "stock_prices": [
            {"stock": "AAPL", "price": 150.0},
            {"stock": "AMZN", "price": 150.0},
            {"stock": "GOOGL", "price": 150.0},
            {"stock": "MSFT", "price": 150.0},
            {"stock": "TSLA", "price": 150.0}
        ]
    }, indent=4)

    assert result == expected_result, "Результат не соответствует ожидаемому"
