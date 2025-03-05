from src.reports import spending_by_category_with_report
from src.services import find_transactions_by_phone
from src.utils import get_currency_and_stock_data
from src.views import get_financial_data

if __name__ == "__mane__":
    print(get_financial_data("2021-12-31", "M"))
    json_str = get_currency_and_stock_data(api_key)
    print(json_str)
    res = find_transactions_by_phone(transactions)
    print(res)
    res = spending_by_category_with_report(transactions, 'Супермаркеты', date="2021-12-31")
