import pytest
from src.views import read_df_excel
from src.reports import spending_by_category, report_to_file

@pytest.fixture(scope='module')
def transactions():
    df = read_df_excel()
    df['Категория'] = df['Категория'].str.strip()
    return df

@pytest.mark.parametrize('category, expected_length', [
    ('Супермаркеты', 131),
    ('Транспорт', 5),
])
def test_spending_by_category(transactions, category, expected_length):
    result = spending_by_category(transactions, category, date="2021-12-31")
    assert len(result) == expected_length
