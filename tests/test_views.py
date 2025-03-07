import pytest
import pandas as pd
import json
from src.views import get_financial_data, read_df_excel  # Замените `your_module` на имя вашего модуля


@pytest.fixture(scope="module")
def test_data():
    df = read_df_excel()
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")
    df["Сумма операции"] = df["Сумма операции"].astype(str).str.replace(",", ".").astype(float)
    return df


# Тест для месячного периода
def test_get_financial_data_monthly(test_data):
    result = get_financial_data("2021-12-31", "M")
    result_dict = json.loads(result)

    # Проверяем, что результат содержит ожидаемые ключи
    assert "expenses" in result_dict
    assert "income" in result_dict
    assert "currency_rates" in result_dict
    assert "stock_prices" in result_dict

    # Проверяем, что сумма расходов и доходов не отрицательная
    assert result_dict["expenses"]["total_amount"] >= 0
    assert result_dict["income"]["total_amount"] >= 0

    # Проверяем, что категории расходов и доходов не пустые
    assert len(result_dict["expenses"]["main"]) > 0
    assert len(result_dict["income"]["categories"]) > 0


# Тест для недельного периода
def test_get_financial_data_weekly(test_data):
    result = get_financial_data("2021-12-31", "W")
    result_dict = json.loads(result)

    # Проверяем, что результат содержит ожидаемые ключи
    assert "expenses" in result_dict
    assert "income" in result_dict

    # Проверяем, что сумма расходов и доходов не отрицательная
    assert result_dict["expenses"]["total_amount"] >= 0
    assert result_dict["income"]["total_amount"] >= 0


# Тест для годового периода
def test_get_financial_data_yearly(test_data):
    result = get_financial_data("2021-12-31", "Y")
    result_dict = json.loads(result)

    # Проверяем, что результат содержит ожидаемые ключи
    assert "expenses" in result_dict
    assert "income" in result_dict

    # Проверяем, что сумма расходов и доходов не отрицательная
    assert result_dict["expenses"]["total_amount"] >= 0
    assert result_dict["income"]["total_amount"] >= 0


# Тест для всего периода
def test_get_financial_data_all(test_data):
    result = get_financial_data("2021-12-31", "ALL")
    result_dict = json.loads(result)

    # Проверяем, что результат содержит ожидаемые ключи
    assert "expenses" in result_dict
    assert "income" in result_dict

    # Проверяем, что сумма расходов и доходов не отрицательная
    assert result_dict["expenses"]["total_amount"] >= 0
    assert result_dict["income"]["total_amount"] >= 0


# Тест для некорректного периода
def test_get_financial_data_invalid_period(test_data):
    with pytest.raises(ValueError, match="Неверный параметр диапазона"):
        get_financial_data("2021-12-31", "INVALID")
