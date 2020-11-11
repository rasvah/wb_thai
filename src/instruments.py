from datetime import date, datetime, timedelta
from pandas import DataFrame
from calendar import monthrange
import numpy as np


class TBill():
    def __init__(self, settle, maturity, price, symbol):
        self.settle = settle
        self.maturity = maturity
        self.price = price
        self.symbol = symbol

    def get_days_to_maturity(self):
        return (self.maturity - self.settle).days

    def get_cost_period(self, begin, end):
        begin = min(max(begin, self.settle), self.maturity)
        end = min(min(end, self.maturity), self.settle)
        return self._get_cost_period(being, end)

    def get_CFs_period(self, begin, end):
        CFs, dates = self.get_CFs()
        index = [(d <= end) & (d > begin) for d in dates]
        return np.array(CFs)[index].sum()

    def _get_cost_period(self, begin, end):
        return self.get_ptp_period(begin, end)

    def get_ptp_period(self, begin, end):
        return (1 - self.price) * (end - begin) / (self.maturity - self.settle)
    
    def get_CFs(self):
        dates = self.get_CF_dates()
        amounts = []
        if len(dates) != 0:
            amounts = [1] # Add principal
        return amounts, dates

    def get_CF_dates(self):
        CF_dates = []
        CF_dates.append(self.maturity)
        return sorted([d for d in CF_dates if d >= self.settle and d <= self.maturity])

class Bond(TBill):
    def __init__(self, settle, maturity, price, coupon, symbol):
        super().__init__(settle, maturity, price, symbol)
        self.coupon = coupon
        self.secondary_cashflow_month = self.get_secondary_cashflow_month()

    def get_CF_dates(self):
        year_range = range(self.settle.year, self.maturity.year + 1)
        CF_dates = []
        for y in year_range:
            m = self.maturity.month
            d =  self.get_adjusted_dom(y, m, self.maturity.day)
            CF_dates.append(date(y, m, d))
            m =  self.secondary_cashflow_month
            d = self.get_adjusted_dom(y, m, self.maturity.day)
            CF_dates.append(date(y, m, d))
        return sorted([d for d in CF_dates if d >= self.settle and d <= self.maturity])
    
    def _get_cost_period(self, begin, end):
        ptp = self.get_ptp_period(begin, end)
        coupon_cost = self.coupon * (end - begin)/360
        return ptp + coupon_cost

    def get_coupons(self):
        dates = self.get_CF_dates()
        amounts = [self.coupon / 2 for _ in dates]
        return amounts, dates

    def get_CFs(self):
        amounts, dates = self.get_coupons()
        if len(amounts) != 0:
          amounts[-1] += 1 # Add principal
        return amounts, dates

    def get_secondary_cashflow_month(self):
        if self.maturity.month > 6:
            return self.maturity.month - 6
        else:
            return self.maturity.month + 6

    def get_adjusted_dom(self, y, month, day):
        _, eom = monthrange(y, month)
        return min(day, eom)