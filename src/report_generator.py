import xlsxwriter

# from instruments import Bond
# from portfolio_importer import PortfolioImporter
# from debt_portfolio import Position, DebtPortfolio

from src.instruments import Bond
from src.portfolio_importer import PortfolioImporter
from src.debt_portfolio import Position, DebtPortfolio

class ReportGenerator:

    def __init__(self, datafile, eval_date):
        self.eval_date = eval_date
        self.portfolio = self.extract_current_debt(datafile, eval_date)
        self.report_data = {}
        self.include_ATM()
        self.write_to_excel()
        
    def extract_current_debt(self, datafile, eval_date):
        importer = PortfolioImporter(datafile)
        portfolio = DebtPortfolio()
        for ix, row in importer.data.iterrows():
            if row.instrument_type == 'BOND':
                issuance_cost = 0
                instrument = Bond(eval_date, row.maturity, issuance_cost,
                                    row.coupon, row.symbol)
                portfolio.add_position(Position(instrument, row.nominal_amount))
                #print(f'Bond with index {index} added')
            else:
                print(f'Unknown type - instrument with index {index} not added')
        return portfolio

    def include_ATM(self):
        data_entry = dict(caption="Bond portfolio ATM (in years)",
                          value=self.portfolio.get_ATM(self.eval_date))
        self.report_data.update(dict(ATM=data_entry))

    def write_to_excel(self):
        date_str = self.eval_date.strftime('%Y%m%d')
        workbook = xlsxwriter.Workbook(f'MonthlyReport_{date_str}.xlsx')
        worksheet = workbook.add_worksheet()

        # Set column width as: set_column(first_col, last_col, width, cell_format, options)
        worksheet.set_column(0, 0, 30)
        
        # Color codes: https://www.w3schools.com/colors/colors_names.asp

        # Report title
        cell_format = workbook.add_format({'font_size': 18, 'bold': True, 'font_color': '#00008B'})
        worksheet.write('A1', f'Monthly Report (as of {self.eval_date})', cell_format)
        
        # Example of report data
        cell_format = workbook.add_format({'font_size': 14, 'bold': False, 
                                           'font_color': 'black',
                                           'num_format': '0.00'})
        worksheet.write('A3', self.report_data['ATM']['caption'], cell_format)
        worksheet.write('B3', self.report_data['ATM']['value'], cell_format)
        workbook.close()

