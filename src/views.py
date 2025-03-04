import os
from typing import Any
import pandas as pd
from datetime import datetime, timedelta
import json
from logger import logger


operations_path = os.path.join(os.path.dirname(__file__), "../data/operations.xls")

def read_df_excel():
    '''Читаем Excel-файл'''
    with open(operations_path, 'r', encoding='utf-8'):
        operations_xls = pd.read_excel(operations_path)
    return operations_xls

# Вызываем функцию и выводим результат
df = read_df_excel()

# Преобразуем столбец "Дата операции" в формат datetime
df["Дата операции"] = pd.to_datetime(df["Дата операции"], format="%d.%m.%Y %H:%M:%S")

# Преобразуем столбец "Сумма операции" в числовой формат
df["Сумма операции"] = df["Сумма операции"].astype(str).str.replace(",", ".").astype(float)
# df["Сумма операции"] = df["Сумма операции"].astype(str).str.replace(",", ".")
df_sorted = df.sort_values(by="Сумма операции", ascending=False)


def get_date_range(date_str, period="M"):
    '''Функция для получения диапазона дат'''
    date = datetime.strptime(date_str, "%Y-%m-%d")
    if period == "W":
        start_date = date - timedelta(days=date.weekday())
        end_date = date
    elif period == "M":
        start_date = date.replace(day=1)
        end_date = date
    elif period == "Y":
        start_date = date.replace(month=1, day=1)
        end_date = date
    elif period == "ALL":
        start_date = datetime.min
        end_date = date
    else:
        raise ValueError("Неверный параметр диапазона")
    return start_date, end_date


def get_financial_data(date_str, period="M"):
    start_date, end_date = get_date_range(date_str, period)

    # Фильтруем данные по диапазону дат
    filtered_df = df[(df["Дата операции"] >= start_date) & (df["Дата операции"] <= end_date)]

    # Расходы (отрицательные суммы)
    expenses_df = filtered_df[filtered_df["Сумма операции"] < 0]
    expenses_total = int(expenses_df["Сумма операции"].sum() * -1) # Сумма расходов (положительное число)
    expenses_by_category = expenses_df.groupby("Категория")["Сумма операции"].sum().abs().to_dict()
    sorted_expenses_by_category = sorted(expenses_by_category.items(), key=lambda x: abs(x[1]), reverse=True)

    # Определяем 7 самых затратных категорий
    main_expenses = sorted_expenses_by_category[:7]

    # Остальные категории
    other_categories = sorted_expenses_by_category[7:]
    others_total = sum([x[1] for x in other_categories])

    # Собираем данные о главных расходах
    main_expenses_list = []
    for cat, amt in main_expenses:
        main_expenses_list.append({"category": cat, "amount": int(amt)})

    # Собираем данные о прочих расходах
    others_expenses = {"category": "Others", "amount": int(others_total)}

    # Поступления (положительные суммы)
    incomes_df = filtered_df[filtered_df["Сумма операции"] > 0]
    incomes_total = incomes_df["Сумма операции"].sum()
    incomes_by_category = incomes_df.groupby("Категория")["Сумма операции"].sum().to_dict()
    sorted_incomes_by_category = sorted(incomes_by_category.items(), key=lambda x: abs(x[1]), reverse=True)

    # Собираем данные о доходах
    income_categories = []
    for cat, amt in sorted_incomes_by_category:
        income_categories.append({"category": cat, "amount": amt})

    result = {
        "expenses": {
            "total_amount": expenses_total,
            "main": main_expenses_list,
            "others": others_expenses
        },
        "income": {
            "total_amount": incomes_total,
            "categories": income_categories
        },
        "currency_rates": {},  # Здесь можно добавить данные о курсах валют
        "stock_prices": {}  # Здесь можно добавить данные о ценах акций
    }

    return json.dumps(result, indent=4, ensure_ascii=False)

logger.info("Начало тестирования финансовой отчетности...")
print(get_financial_data("2021-12-31", "M"))
logger.info("Тестирование финансовой отчетности завершено.")