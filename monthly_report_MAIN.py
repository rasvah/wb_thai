from datetime import date

from src.instruments import Bond
from src.debt_portfolio import Position, DebtPortfolio


if __name__ == '__main__':

    eval_date = date(2021, 1, 14)

    # Data source: http://www.thaibma.or.th/EN/Market/YieldCurve/Government.aspx

    # Bond 1: 2025
    settle = eval_date
    maturity = date(2025, 6, 17)
    issuance_cost = 0
    coupon = 0.0095
    symbol = "LB256A"
    bond_1 = Bond(settle, maturity, issuance_cost, coupon, symbol)
    amount_1 =  71.630
    position_1 = Position(bond_1, amount_1)

    # Bond 2: 2029
    settle = eval_date
    maturity = date(2029, 12, 17)
    issuance_cost = 0
    coupon = 0.016
    symbol = "LB29DA"
    bond_2 = Bond(settle, maturity, issuance_cost, coupon, symbol)
    amount_2 = 188.751
    position_2 = Position(bond_2, amount_2)

    # Create portfolio
    pf = DebtPortfolio()
    pf.add_position(position_1)
    pf.add_position(position_2)

    print(f"ATM (in years): {pf.get_ATM(eval_date):.2f}")
