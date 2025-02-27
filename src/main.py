from pathlib import Path
# import loguru

# # Определение пути до папки logs в корне проекта
# project_root = Path(__file__).parent.resolve()  # Получаем путь до корня проекта
# log_dir = project_root / 'logs'  # Присоединяем папку logs
# log_file = log_dir / 'app.log'   # Указываем имя файла журнала
#
# # Создание папки logs, если она еще не существует
# log_dir.mkdir(parents=True, exist_ok=True)
#
# # Настройка логгера
# logger.add(str(log_file), rotation="500 MB")  # Логирование в файл
#
# def main():
#     logger.info("Application started")
#
# # ТАК ВЫЗЫВАЕТСЯ ЛОГЕР В ЛЮБОМ МОДУЛЕ
# # from loguru import logger
# #
# # def some_function():
# #     logger.info("This is an info message from the module.")
#




if __name__ == "__main__":
    main()

transacions = pd.read_excel()