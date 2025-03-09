import os
import json
import pandas as pd
import datetime

def records_to_dataframe(record_dir : str, record_type : str) -> pd.DataFrame:

    df = pd.DataFrame() # create empty dataframe

    def append_to_dataframe(file, df):
        with open(file, 'r') as f:
            data = json.load(f)
        norm_data = pd.json_normalize(data)
        if norm_data['type'].iloc[0] == record_type:
            df = pd.concat([df, norm_data], ignore_index=True)
        return df

    for root, dirs, files in os.walk(record_dir):
        for file in files:
            # iterate through files in root dir
            if file.endswith('.json'):
                filepath = os.path.join(root, file)
                df = append_to_dataframe(filepath, df)


    return df

def date_columns_to_datetime(df : pd.DataFrame) -> list:

        dates = []

        for _, row in df.iterrows():
            year =  row['date.year']
            month = row['date.month']
            day =   row['date.day']

            date = (datetime.datetime(year=year, month=month, day=day))
            iso_date =  date.strftime('%Y-%m-%d')
            dates.append(iso_date)

        return dates