from datetime import date

from src.instruments import Bond
from src.portfolio_importer import PortfolioImporter
from src.debt_portfolio import Position, DebtPortfolio



if __name__ == '__main__':

    importer = PortfolioImporter('data/bonds.csv')
    eval_date = date(2021, 1, 14)

    # Create portfolio
    current_debt = DebtPortfolio()

    for ix, row in importer.data.iterrows():
        if row.instrument_type == 'BOND':
            issuance_cost = 0
            instrument = Bond(eval_date, row.maturity, issuance_cost,
                              row.coupon, row.symbol)
            current_debt.add_position(Position(instrument, row.nominal_amount))
            #print(f'Bond with index {index} added')
        else:
            print(f'Unknown type - instrument with index {index} not added')


    print(f"Bond portfolio ATM (in years): {current_debt.get_ATM(eval_date):.2f}")

    