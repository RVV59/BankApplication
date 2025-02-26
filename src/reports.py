import pandas as pd
from datetime import datetime, timedelta
from typing import Optional
from logger import logger


def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> str:
    """
    Возвращает траты по заданной категории за последние три месяца в формате JSON.

    :param transactions: Датафрейм с транзакциями.
    :param category: Название категории.
    :param date: Опциональная дата (строка в формате 'YYYY-MM-DD'). Если не передана, используется текущая дата.
    :return: JSON-строка с тратами по категории за последние три месяца.
    """
    # Определяем дату
    if date is None:
        date = datetime.now()
    else:
        date = datetime.strptime(date, "%Y-%m-%d")

    # Вычисляем дату начала периода (три месяца назад)
    start_date = date - timedelta(days=90)

    # Фильтруем транзакции по категории и дате
    filtered_transactions = transactions[
        (transactions["Категория"] == category) &
        (pd.to_datetime(transactions["Дата операции"]) >= start_date) &
        (pd.to_datetime(transactions["Дата операции"]) <= date)
    ]

    # Логируем результат
    logger.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}' за последние три месяца.")

    # Преобразуем результат в JSON
    return filtered_transactions.to_json(orient="records", force_ascii=False, date_format="iso")