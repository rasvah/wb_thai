from datetime import date

from src.report_generator import ReportGenerator


datafile='data/bonds.csv'
eval_date=date(2020, 12, 31)

report = ReportGenerator(datafile, eval_date)
