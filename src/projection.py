from scipy.interpolate import interp1d

class YieldCurve:
    def __init__(self, dates, yields, mats):
      self.dates = dates
      self.yields = yields
      self.mats = mats
      self.interpolator = interp1d(mats, yields)

    def get_yield(self, date_, mat):
      y = self.interpolator(mat)
      year_start = date(date_.year-1, 12, 31)
      if year_start < self.dates[0]:
        year_start = self.dates[0]

      y_start = y[self.dates.index(year_start)]
      year_end = date(date_.year, 12, 31)
      if self.dates[-1] < date_:
        y = y[-1]

      else:
        y_end = y[self.dates.index(year_end)]
        days_in_year =(year_end - year_start)
        y = y_start * (date_ - year_start) / days_in_year + y_end * (year_end - date_) / days_in_year

      return y
     
class PrimaryDeficit:
    def __init__(self, dates, deficit):
        self.dates = dates
        self.deficit = deficit

    def get(self, begin, end):
        year_end = date(end.year, 12, 31)
        deficit_year = self.deficit[self.dates.index(year_end)]
        year_start = self.dates[self.dates.index(year_end)-1]

        return deficit_year * (end-begin) / (year_end - year_start)