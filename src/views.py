import os
import pandas as pd


operations_path = os.path.join(os.path.dirname(__file__), "../data/operations.xls")

def read_df_excel():
    '''Читаем Excel-файл'''
    with open(abs_path, 'r', encoding='utf-8'):
        operations_xls = pd.read_excel(abs_path)
    return operations_xls

# Вызываем функцию и выводим результат
# first_five_rows = read_df_excel()
# print(first_five_rows)
