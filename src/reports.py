import functools
import os
from datetime import datetime
from typing import Optional

import pandas as pd

from logger import logger
from src.views import read_df_excel

transactions = read_df_excel()
transactions["Категория"] = transactions["Категория"].str.strip()


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние три месяца.
    """
    if date is None:
        date = pd.Timestamp.now()
    else:
        date = pd.Timestamp(date)

    start_date = date - pd.DateOffset(months=3)

    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        format="%d.%m.%Y %H:%M:%S"
    )

    filtered_transactions = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
    ]

    logger.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}' за последние три месяца.")

    return filtered_transactions


def report_to_file(filename: Optional[str] = None):
    """
    Декоратор для записи результата функции в файл.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if filename is None:
                default_filename = f"{func.__name__}_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                file_path = default_filename
            else:
                file_path = filename
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                result.to_json(file_path, orient="records", force_ascii=False, date_format="iso", indent=4)

            logger.info(f"Результат сохранен в файл: {file_path}")
            return result

        return wrapper

    return decorator


@report_to_file('./data/report_category.json')
def spending_by_category_with_report(transactions: pd.DataFrame, category: str, date: Optional[str] = None) \
        -> pd.DataFrame:
    """
    Обертка для функции spending_by_category с декоратором report_to_file.
    """
    return spending_by_category(transactions, category, date)


res = spending_by_category_with_report(transactions, 'Супермаркеты', date="2021-12-31")
