class TestFinancialData(unittest.TestCase):

    def setUp(self):
        self.api_key = 'TEST_API_KEY'

    @patch('requests.get')
    def test_successful_response(self, mock_get):
        # Подготавливаем моки для успешных запросов
        stock_mock_response = {'Global Quote': {'05. price': '150.00'}}
        currency_mock_response = {'Realtime Currency Exchange Rate': {'5. Exchange Rate': '70.00'}}

        # Настройка моков для запросов акций и валют
        mock_get.side_effect = [
            MagicMock(return_value={'json': lambda: stock_mock_response}),  # Ответ для акций
            MagicMock(return_value={'json': lambda: currency_mock_response})  # Ответ для валют
        ]

        # Выполняем функцию
        actual_result = get_financial_data(self.api_key)

        # Ожидаемый результат
        expected_result = json.dumps({
            "currency_rates": [
                {
                    "currency": "USD",
                    "rate": 70.00
                }
            ],
            "stock_prices": [
                {
                    "stock": "AAPL",
                    "price": 150.00
                }
            ]
        }, indent=4)

        # Сравниваем полученные данные с ожидаемыми
        self.assertEqual(actual_result, expected_result)

    @patch('requests.get')
    def test_error_handling(self, mock_get):
        # Подготовка мока для ошибки
        error_mock_response = {'Error Message': 'Invalid API key'}

        # Настройка мока для возврата ошибки
        mock_get.return_value = MagicMock(return_value={'json': lambda: error_mock_response})

        # Выполнение функции должно вызвать ошибку
        with self.assertRaises(Exception) as context:
            get_financial_data(self.api_key)

        # Проверка сообщения об ошибке
        self.assertTrue('Invalid API key' in str(context.exception))

if __name__ == '__main__':
    unittest.main()