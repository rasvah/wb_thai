from src.instruments import get_adjusted_dom

# Run from the wb_thai root folder with the command 'pytest test/test_instruments_1a.py'

def test_get_adjusted_dom_feb_leap_year():
    actual = get_adjusted_dom(year=2020, month=2, day=29)
    expected = 29
    assert actual == expected

def test_get_adjusted_dom_feb_non_leap_year():
    actual = get_adjusted_dom(year=2019, month=2, day=29)
    expected = 28
    assert actual == expected

def test_get_adjusted_dom_jan_non_leap_year():
    actual = get_adjusted_dom(year=2019, month=1, day=29)
    expected = 29
    assert actual == expected
