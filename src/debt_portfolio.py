import pandas as pd
import numpy as np
from datetime import date
from calendar import monthrange
from pandas import DataFrame


class Position:
    def __init__(self, bond, amount):
        self.bond = bond
        self.amount = amount

    def get_CFs(self):
        CFs, dates = self.bond.get_CFs()
        df = DataFrame(data = [c * self.amount for c in CFs],
         index = dates, columns = [self.bond.symbol])
        return df

    def get_CFs_period(self, begin, end):
        return self.bond.get_CFs_period(begin, end) * self.amount        

    def get_cost_period(self, begin, end):
        return self.bond.get_cost_period(begin, end) * self.amount


class DebtPortfolio:
    def __init__(self):
        self.positions = []
        
    def add_position(self, position):
        self.positions.append(position)
        
    def get_CFs(self, eval_date):
        CFs = [p.get_CFs() for p in self.positions]
        df = pd.concat(CFs, axis=1)
        df = df.fillna(value=0)
        return df.iloc[df.index >= eval_date, :]

    def get_CF_period(self, begin, end):
        CFs = [p.get_CFs_period(begin, end) for p in self.positions]
        return np.sum(CFs)

    def get_cost_period(self, begin, end):
        cost = [p.get_cost_period(begin, end) for p in self.positions]
        return np.sum(cost)


class IssuanceProjector:
    def __init__(self, eval_date, end_date, step_size = 12):
        self.eval_date = eval_date
        self.end_date = end_date
        self.step_size = step_size
        self.current_debt = DebtPortfolio()        
        self.new_debt = DebtPortfolio()

    def add_current_debt(self, current_debt):
        self.current_debt = current_debt

    def get_issuance(self, primary_deficit, issuance_strategy, yield_curve):
        # build up debt portfolio
        dates = self.get_dates()
        dates.insert(0, self.eval_date)

        amount_needed_ = []
        deficit_financing_ = []
        cur_debt_financing_ = []
        new_debt_financing_ = []
        for j, d in enumerate(dates[1:]):
          # calculate eom issuance needs
          # primary deficit
          deficit_financing = primary_deficit.get(dates[j], d)
          
          # cur_debt
          cur_debt_financing = self.current_debt.get_CF_period(dates[j], d)

          # new_debt
          new_debt_financing = self.new_debt.get_CF_period(dates[j], d)

          amount_needed = deficit_financing + cur_debt_financing 

          # issue new_debt and add to new_debt_portfolio
          issuance = issuance_strategy.get_issuance(d, amount_needed, yield_curve)
          for p in issuance:
            self.new_debt.add_position(p)

          amount_needed_.append(amount_needed)
          deficit_financing_.append(deficit_financing)
          cur_debt_financing_.append(cur_debt_financing)
          new_debt_financing_.append(new_debt_financing)

        return DataFrame(data = list(zip(*[amount_needed_, deficit_financing_, cur_debt_financing_, new_debt_financing_])),
         index = dates[1:], columns= ['total issuance', 'deficit financing', 'current debt financing', 'new debt financing'])


    def get_dates(self):
        end = self.end_date
        end = date(end.year, end.month, monthrange(end.year, end.month)[1])
        dates = pd.date_range(self.eval_date, end, freq = 'M')
        return [d.date() for d in dates[1:]]
