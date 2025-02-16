import requests
import logging
import pandas as pd
import json


class FxQuotesAPI:

    def __init__(self):
        self.log = logging.getLogger()
        self.api_key = '1RRQF85Z3P07AHPL'
        self.to_currency = 'CHF'
        self.from_currencies = ['USD','EUR']

        self.base_obj_key = "Realtime Currency Exchange Rate"
        self.fx_key = "5. Exchange Rate"
        self.date_key = "6. Last Refreshed"


    def query(self):

        df = pd.DataFrame()
   
        for from_currency in self.from_currencies:

            url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={self.to_currency}&apikey=={self.api_key}'

            response = requests.get(url)

            self.log.debug(response.text)

            data = response.json()[self.base_obj_key]

            fx_rate = float(data[self.fx_key])
            date = data[self.date_key].split(' ')[0].split('-')

            year = int(date[0])
            month = int(date[1])
            day = int(date[2])

            new_dict = {"src_currency": from_currency,  "dest_currency": self.to_currency ,"fx_rate": fx_rate, 'date.year' : year, 'date.month' : month,'date.day' : day}
            new_record = pd.json_normalize(new_dict)
            df = pd.concat([df, new_record], ignore_index=True)



        return df

