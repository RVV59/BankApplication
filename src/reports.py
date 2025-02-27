import pandas as pd
from datetime import datetime, timedelta
import os
from mypy.strconv import indent
from logger import logger
import functools
from typing import Optional
from views import read_df_excel


# Пример данных
transactions = read_df_excel()
transactions["Категория"] = transactions["Категория"].str.strip()  # Удалить пробелы в начале и конце

# Функция для фильтрации транзакций по категории и дате
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:

    """
    Возвращает траты по заданной категории за последние три месяца.
    """
    # Определяем дату
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    # Вычисляем дату начала периода (три месяца назад)
    start_date = date - pd.DateOffset(months=3)

    # Преобразуем даты в столбце "Дата операции" с указанием формата
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        format="%d.%m.%Y %H:%M:%S"  # Указываем формат даты
    )

    # Фильтруем транзакции по категории и дате
    filtered_transactions = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= date)
    ]

    # Логируем результат
    logger.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}' за последние три месяца.")

    return filtered_transactions

# Декоратор для записи результата в файл
def report_to_file(filename: Optional[str] = None):
    """
    Декоратор для записи результата функции в файл.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Вызов функции и получение результата
            result = func(*args, **kwargs)

            # Определение имени файла
            if filename is None:
                default_filename = f"{func.__name__}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                file_path = default_filename
            else:
                file_path = filename

            # Создаем папку, если её нет
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # Преобразуем результат в JSON и записываем в файл
            result.to_json(file_path, orient="records", force_ascii=False, date_format="iso", indent=4)

            logger.info(f"Результат сохранен в файл: {file_path}")
            return result
        return wrapper
    return decorator

# Применяем декоратор к функции
@report_to_file('./data/report_category.json')  # Указываем путь к файлу
def spending_by_category_with_report(transactions: pd.DataFrame, category: str, date: Optional[str] = None)\
        -> pd.DataFrame:
    """
    Обертка для функции spending_by_category с декоратором report_to_file.
    """
    return spending_by_category(transactions, category, date)

res = spending_by_category_with_report(transactions, 'Супермаркеты', date="2021-12-31")
# print(res)