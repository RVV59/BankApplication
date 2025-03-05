import pytest
from src.services import investment_bank

def test_investment_bank():
    # Тестовые данные
    transactions = [
        {"Дата операции": "2023-10-01", "Сумма операции": 1712},
        {"Дата операции": "2023-10-05", "Сумма операции": 845},
        {"Дата операции": "2023-10-10", "Сумма операции": 123},
        {"Дата операции": "2023-11-15", "Сумма операции": 456},
    ]

    # Тест 1: Проверка округления с пределом 50
    assert investment_bank("2023-10", transactions, limit=50) == 70.0

    # Тест 2: Проверка округления с пределом 100
    assert investment_bank("2023-10", transactions, limit=100) == 220.0

    # Тест 3: Проверка некорректного предела округления
    with pytest.raises(ValueError):
        investment_bank("2023-10", transactions, limit=25)

    # Тест 4: Проверка пустого списка транзакций
    assert investment_bank("2023-10", [], limit=50) == 0.0

    # Тест 5: Проверка транзакций за другой месяц
    assert investment_bank("2023-11", transactions, limit=50) == 44.0