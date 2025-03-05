import json
import re
from datetime import datetime
from typing import Any, Dict, List

from logger import logger


def investment_bank(month: str, transactions: List[Dict[str, Any]], limit: int) -> float:
    """
    Рассчитывает сумму, которую можно отложить в «Инвесткопилку» за указанный месяц.
    """
    if limit not in {10, 50, 100}:
        logger.error(f"Недопустимый предел округления: {limit}. Допустимые значения: 10, 50, 100.")
        raise ValueError("Предел округления должен быть 10, 50 или 100.")

    total_savings = 0.0

    for transaction in transactions:
        try:
            operation_date = datetime.strptime(transaction["Дата операции"], "%Y-%m-%d")
            transaction_month = operation_date.strftime("%Y-%m")

            if transaction_month == month:
                amount = transaction["Сумма операции"]

                rounded_amount = ((amount + limit - 1) // limit) * limit
                savings = rounded_amount - amount

                total_savings += savings

                logger.info(
                    f"Транзакция на {amount} руб. округлена до {rounded_amount} руб. "
                    f"Отложено в копилку: {savings} руб."
                )
        except KeyError as e:
            logger.error(f"Отсутствует обязательное поле в транзакции: {e}")
        except Exception as e:
            logger.error(f"Ошибка при обработке транзакции: {e}")

    logger.info(f"Итого отложено в «Инвесткопилку» за {month}: {total_savings} руб.")
    return total_savings


transactions = [
    {"Дата операции": "2023-10-01", "Сумма операции": 1712},
    {"Дата операции": "2023-10-05", "Сумма операции": 845},
    {"Дата операции": "2023-10-10", "Сумма операции": 123},
    {"Дата операции": "2023-11-15", "Сумма операции": 456},  # Эта транзакция не будет учтена
]

savings = investment_bank("2023-10", transactions, limit=50)
print(f"Сумма в копилке: {savings} руб.")

transactions = [
    {"Дата операции": "2023-10-01", "Сумма операции": 100, "Описание": "Я МТС +7 921 11-22-33"},
    {"Дата операции": "2023-10-02", "Сумма операции": 200, "Описание": "Тинькофф Мобайл +7 995 555-55-55"},
    {"Дата операции": "2023-10-03", "Сумма операции": 300, "Описание": "МТС Mobile +7 981 333-44-55"},
    {"Дата операции": "2023-10-04", "Сумма операции": 400, "Описание": "Оплата за интернет"},
]


def find_transactions_by_phone(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ищет транзакции, содержащие в описании мобильные номера.
    """
    phone_regex = re.compile(
        r"\+7\s?\d{3}\s?\d{3}[- ]?\d{2}[- ]?\d{2}"
    )

    result = []

    for transaction in transactions:
        try:
            description = transaction.get("Описание", "")
            if phone_regex.search(description):
                result.append(transaction)
                logger.info(f"Найдена транзакция с номером телефона: {description}")
        except Exception as e:
            logger.error(f"Ошибка при обработке транзакции: {e}")

    return json.dumps(result, ensure_ascii=False, indent=4)


res = find_transactions_by_phone(transactions)
print(res)
