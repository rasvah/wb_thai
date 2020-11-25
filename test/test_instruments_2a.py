from datetime import date
import numpy as np
from numpy.testing import assert_array_equal

from src.instruments import Bond


def test_get_coupons_LB246A():
    settle = date(2020, 11, 26)
    maturity = date(2024, 6, 17)
    issuance_cost = 0.0
    coupon = 0.0075
    symbol = "LB246A"
    bond = Bond(settle, maturity, issuance_cost, coupon, symbol)
    actual_amounts, actual_dates = bond.get_coupons()
    expected_dates = [date(2020, 12, 17), \
        date(2021, 6, 17), date(2021, 12, 17),
        date(2022, 6, 17), date(2022, 12, 17),
        date(2023, 6, 17), date(2023, 12, 17),
        date(2024, 6, 17)]
    expected_amounts = [0.00375, 0.00375, 0.00375, 0.00375, 0.00375, \
        0.00375, 0.00375, 0.00375]
    assert actual_amounts == expected_amounts
    assert actual_dates == expected_dates


def test_get_CFs_period_LB246A():
    settle = date(2020, 11, 26)
    maturity = date(2024, 6, 17)
    issuance_cost = 0.0
    coupon = 0.0075
    symbol = "LB246A"
    bond = Bond(settle, maturity, issuance_cost, coupon, symbol)
    begin_date = date(2021, 1, 1)
    end_date = date(2023, 12, 31)
    actual = bond.get_CFs_period(begin_date, end_date)
    expected = 3 * 0.0075
    assert actual == expected
