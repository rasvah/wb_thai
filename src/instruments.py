from datetime import date, datetime, timedelta
from pandas import DataFrame
from calendar import monthrange
import numpy as np

class Instrument():
    """ Abstract class/interface for instruments """
    def __init__(self):
        raise NotImplementedError

    def get_CFs_period(self, begin, end):
        raise NotImplementedError

    def get_cost_period(self, begin, end):
        raise NotImplementedError

    def get_days_to_maturity(self, eval_date):
        return (self.maturity - eval_date).days

class Bond(Instrument):
    """ Bond instrument class """
    def __init__(self, settle, maturity, issuance_cost, coupon, symbol):
        self.settle = settle
        self.maturity = maturity
        self.issuance_cost = issuance_cost
        self.coupon = coupon
        self.symbol = symbol
        self.secondary_cashflow_month = self._get_secondary_cashflow_month()

    def get_CFs_period(self, begin, end):
        CFs, dates = self.get_CFs()
        index = [(d <= end) & (d > begin) for d in dates]
        return np.array(CFs)[index].sum()    

    def get_cost_period(self, begin, end):
        begin = min(max(begin, self.settle), self.maturity)
        end = max(min(end, self.maturity), self.settle)
        return self._get_cost_period(begin, end)

    def get_coupons(self):
        dates = self._get_CF_dates()
        amounts = [self.coupon / 2 for _ in dates]
        return amounts, dates

    def get_CFs(self):
        amounts, dates = self.get_coupons()
        if len(amounts) != 0:
          amounts[-1] += 1 # Add principal
        return amounts, dates

    def _get_amortized_cost_period(self, begin, end):
        return self.issuance_cost * (end - begin).days / (self.maturity - self.settle).days

    def _get_cost_period(self, begin, end):
        amortizing = self._get_amortized_cost_period(begin, end)
        coupon_cost = self.coupon * (end - begin).days/365
        return amortizing + coupon_cost
    
    def _get_CF_dates(self):
        year_range = range(self.settle.year, self.maturity.year + 1)
        CF_dates = []
        for y in year_range:
            m = self.maturity.month
            d =  self._get_adjusted_dom(y, m, self.maturity.day)
            CF_dates.append(date(y, m, d))
            m =  self.secondary_cashflow_month
            d = self._get_adjusted_dom(y, m, self.maturity.day)
            CF_dates.append(date(y, m, d))
        return sorted([d for d in CF_dates if d >= self.settle and d <= self.maturity])
    
    def _get_secondary_cashflow_month(self):
        if self.maturity.month > 6:
            return self.maturity.month - 6
        else:
            return self.maturity.month + 6

    def _get_adjusted_dom(self, y, month, day):
        _, eom = monthrange(y, month)
        return min(day, eom)


class TBill(Bond):
    def __init__(self, settle, maturity, residual_issuance_cost, symbol):
        super().__init__(settle, maturity, residual_issuance_cost, 0, symbol)
 
    def _get_cost_period(self, begin, end):
        return self._get_amortized_cost_period(begin, end)
    
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

