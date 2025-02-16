import pandas as pd
import utils as utils


class Deposits:


    def __init__(self, deposit_dir : str):

        df = utils.records_to_dataframe(record_dir = deposit_dir, record_type = 'deposit')
        df['date'] = utils.date_columns_to_datetime(df)
        df = df.drop(['date.year', 'date.month', 'date.day'], axis=1)
        self.deposits = df

    def all(self) -> pd.DataFrame:
        return self.deposits
    
    def all_for(self, broker : str) -> pd.DataFrame:
        df = self.deposits[self.deposits['broker'] == broker]
        return df
    

    def sum_for(self, broker : str) -> tuple:
        df = self.all_for(broker)
        df = df.drop(['date'], axis=1)
        df = df.groupby(['broker', 'type', 'src_currency', 'dest_currency'])[['src_value', 'dest_value']].sum().reset_index()

        s = df.iloc[0]
        src_value = s['src_value']
        src_currency = s['src_currency']

        dest_value = s['dest_value']
        dest_currency = s['dest_currency']


        return (src_value, src_currency, dest_value, dest_currency)
       
    def cumulated_sum_for(self, broker : str)  -> pd.DataFrame:

        df = self.all_for(broker)

        df['src_value'] = df['src_value'].cumsum()
        df['dest_value'] = df['dest_value'].cumsum()

        return df


        








