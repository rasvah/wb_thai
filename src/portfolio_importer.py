from datetime import datetime
import pandas as pd
from pandas import DataFrame


SELECTED_INSTRUMENTS = ['BOND']

SELECTED_COLS = ['Instrument', 'Contract name', 'External Ref.', 'End date',
                  'Interest', 'Debt Outstanding 09/2020', 'TCurr']
NEW_COL_NAMES = ['instrument_type', 'full_name', 'symbol', 'maturity', 
                 'coupon', 'nominal_amount', 'currency']

NAME_MAPPINGS = dict(zip(SELECTED_COLS, NEW_COL_NAMES))


def extract_date(x):
    return datetime.strptime(x, "%m/%d/%y").date()




class PortfolioImporter:

    def __init__(self, filename):
        data = pd.read_csv(filename)[SELECTED_COLS].rename(columns=NAME_MAPPINGS)
        data = data[data['instrument_type'].isin(SELECTED_INSTRUMENTS)]
        data = self.format_columns(data)
        self.data = data

    def format_columns(self, data: DataFrame):
        df = data.copy()
        df['maturity'] = df['maturity'].apply(extract_date)
        df['nominal_amount'] = df['nominal_amount'].apply(lambda x: x / 1e9)
        df['coupon'] = df['coupon'].apply(lambda x: x / 100)
        return df

