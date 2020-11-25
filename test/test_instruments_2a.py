import pytest
import numpy as np
from datetime import date

from src.instruments import Bond

# Run with 'pytest test/test_Bond.py'

@pytest.fixture
def bond():
    settle = date(2020, 11, 24)
    maturity = date(2029, 12, 17)
    issuance_cost = 0.01
    coupon = 0.02
    symbol = "LDA255"
    return Bond(settle, maturity, issuance_cost, coupon, symbol)

def test_get_secondary_cashflow_month(bond):
    actual = bond._get_secondary_cashflow_month()
    expected = 6
    assert actual == expected

@pytest.mark.parametrize("year, month, day, expected", [
    (2020, 2, 29, 28),
    (2016, 2, 29, 29),
])
def test_get_adjusted_dom(bond, year, month, day, expected):
    actual = bond._get_adjusted_dom(year, month, day)
    assert actual == expected
