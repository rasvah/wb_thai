from datetime import date, datetime, timedelta
from pandas import DataFrame
from calendar import monthrange
import numpy as np

class Bond:
    def __init__(self, settle, maturity, coupon, symbol):
        self.settle = settle
        self.maturity = maturity
        self.coupon = coupon
        self.symbol = symbol
        self.secondary_cashflow_month = self.get_secondary_cashflow_month()

    def get_days_to_maturity(self):
        return (self.maturity - self.settle).days
    
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
    
    def get_cost_period(self, begin, end):
        coupons, dates = self.get_coupons()
        index = [(d <= end) & (d > begin) for d in dates]
        return np.array(coupons)[index].sum()

    def get_CFs_period(self, begin, end):
        CFs, dates = self.get_CFs()
        index = [(d <= end) & (d > begin) for d in dates]
        return np.array(CFs)[index].sum()

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

class TBill():
    def __init__(self):
        pass