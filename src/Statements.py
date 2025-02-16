import pandas as pd
import utils as utils

class Statements:

    def __init__(self, statement_dir : str):
        df = utils.records_to_dataframe(record_dir = statement_dir, record_type = 'statement')
        df['date'] = utils.date_columns_to_datetime(df)
        df = df.drop(['date.year', 'date.month', 'date.day'], axis=1)
        self.statements = df


    def all(self) -> pd.DataFrame:
        return self.statements
    
    def all_for(self, broker : str) -> pd.DataFrame:
        df = self.statements[self.statements['broker'] == broker]
        return df
    
    def latest_for(self, broker : str) -> pd.Series:
        df = self.statements[self.statements['broker'] == broker]
        df = df.sort_values(by=['date'], ascending=[False])
   
        return df.iloc[0]





