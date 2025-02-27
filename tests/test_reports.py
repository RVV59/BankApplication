import os
import pandas as pd
from datetime import datetime, timedelta
from logger import logger
import functools

# Чтение данных из Excel
def read_df_excel():
    '''Читаем Excel-файл'''
    operations_path = os.path.join(os.path.dirname(__file__), "../data/operations1.xlsx")
    operations_xls = pd.read_excel(operations_path)
    return operations_xls

# Функция для фильтрации транзакций по категории и дате
def spending_by_category(transactions, category, date=None):
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

    # Преобразуем даты в столбце "Дата операции" с указанием формата
    transactions["Дата операции"] = pd.to_datetime(
        transactions["Дата операции"],
        format="%d.%m.%Y %H:%M:%S"  # Указываем формат даты
    )

    # Очищаем категории от лишних пробелов
    transactions["Категория"] = transactions["Категория"].str.strip()

    # Фильтруем транзакции по категории и дате
    filtered_transactions = transactions[
        (transactions["Категория"] == category) &
        (transactions["Дата операции"] >= start_date) &
        (transactions["Дата операции"] <= date)
    ]

    # Логируем результат
    logger.info(f"Найдено {len(filtered_transactions)} транзакций по категории '{category}' за последние три месяца.")

    # Преобразуем результат в JSON
    return filtered_transactions.to_json(orient="records", force_ascii=False, date_format="iso")

# Декоратор для записи результата в файл
def report_to_file(filename=None):
    """
    Декоратор для записи результата функции в файл.

    :param filename: Имя файла. Если не указано, используется имя по умолчанию.
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

            # Запись результата в файл
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(result)

            logger.info(f"Результат сохранен в файл: {file_path}")
            return result
        return wrapper
    return decorator

# Применяем декоратор к функции
@report_to_file('./src/data/report_category.json')  # Указываем путь к файлу
def spending_by_category_with_report(transactions, category, date=None):
    """
    Обертка для функции spending_by_category с декоратором report_to_file.
    """
    return spending_by_category(transactions, category, date)

# Пример вызова функции с декоратором
transactions = read_df_excel()
res = spending_by_category_with_report(transactions, 'Супермаркет')
print(res)