# logger.py
from loguru import logger

# Настройка логгера
logger.add(
    "logs/logfile.log",  # Путь к файлу логов
    rotation="10 MB",    # Ротация логов каждые 10 МБ
    retention="30 days", # Хранение логов 30 дней
    level="INFO",        # Уровень логирования
    format="{time} {level} {message}",  # Формат логов
    encoding="utf-8",    # Кодировка файла
)