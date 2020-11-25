import pytest
from src.instruments import get_adjusted_dom

@pytest.mark.parametrize("year, month, day, expected", [
    (2020, 2, 29, 29), # Feb. in leap year
    (2019, 2, 29, 28), # Feb. in non-leap year
    (2020, 1, 29, 29), # Jan. in leap year
])
def test_get_adjusted_dom(year, month, day, expected):
    actual = get_adjusted_dom(year, month, day)
    assert actual == expected
