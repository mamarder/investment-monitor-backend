from Deposits import Deposits
from Statements import Statements
from AccountVisualizer import AccountVisualizer
from FxQuotesAPI import FxQuotesAPI
import pandas as pd

import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s' 
)

logging.getLogger('matplotlib.font_manager').setLevel(logging.ERROR)

log = logging.getLogger()

dir = os.getcwd()

deposit_dir = os.path.join(dir, 'deposit','real')
statement_dir = os.path.join(dir, 'statement','real')

deposits = Deposits(deposit_dir=deposit_dir)
statements = Statements(statement_dir=statement_dir)

brokers = ['eToro','Flatex']







#fxQuotesAPI = FxQuotesAPI()
#fxQuotes = fxQuotesAPI.query()

fxQuotes = pd.DataFrame()
record_a = pd.json_normalize({"src_currency": 'USD',  "dest_currency": 'CHF' ,"fx_rate": 0.87, 'date.year' : 24, 'date.month' : 8,'date.day' : 15})
record_b = pd.json_normalize({"src_currency": 'USD',  "dest_currency": 'CHF' ,"fx_rate": 0.95, 'date.year' : 24, 'date.month' : 8,'date.day' : 12})

fxQuotes = pd.concat([fxQuotes, record_a], ignore_index=True)
fxQuotes = pd.concat([fxQuotes, record_b], ignore_index=True)



src_currencies = fxQuotes['src_currency']

for idx, src_currency in enumerate(src_currencies):

    year = fxQuotes['date.year'].iloc[idx]
    month = fxQuotes['date.month'].iloc[idx]
    day = fxQuotes['date.day'].iloc[idx]
    dest_currency = fxQuotes['dest_currency'].iloc[idx]
    fx_rate = fxQuotes['fx_rate'].iloc[idx]

    log.info(f'{src_currency}->{dest_currency} {year}-{month}-{day}: {fx_rate:.2f}')





for i, broker in enumerate(brokers):


    # deposit data for broker
    (src_deposit, src_currency, dest_deposit, dest_currency) = deposits.sum_for(broker)

    fx_rate_avg = dest_deposit/src_deposit

    # actual data for broker
    statement = statements.latest_for(broker)
    dest_value = statement['value']
    currency = statement['currency']

    # fx data for currency of broker
    fxQuote = fxQuotes[fxQuotes['src_currency'] == currency]
    dest_currency_actual = fxQuotes['dest_currency'].iloc[i]
    fx_rate_actual = fxQuotes['fx_rate'].iloc[i]

    src_value = dest_value * fx_rate_actual

    src_result_abs = src_value - src_deposit
    src_result_rel = src_value / src_deposit

    dest_result_abs = dest_value - dest_deposit
    dest_result_rel = dest_value / dest_deposit
    
    log.info(f'\nBroker: {broker}')
    log.info(f'Deposit: {src_deposit:.2f} {src_currency} --{fx_rate_avg:.3f}--> {dest_deposit:.2f} {dest_currency}')
    log.info(f'Value:   {src_value:.2f} {dest_currency_actual} --{1/fx_rate_actual:.3f}--> {dest_value:.2f} {currency}')
    log.info(f'Result:  {src_result_rel:.2f}                   {dest_result_rel:.2f}')


    table = {
        '' : ['Deposit','Value', 'Result (abs.)', 'Result (rel.)'],
        f'{src_currency}': [src_deposit, src_value, src_result_abs, src_result_rel],
        'FX': [fx_rate_avg, 1/fx_rate_actual,'', '' ],
        f'{dest_currency}': [ dest_deposit, dest_value, dest_result_abs, dest_result_rel]
    }

    table = pd.DataFrame(table).style

    styles =     [
        {
            'selector': 'thead',
            'props': [
                ('border', '1px solid black'),
            ]
        },
        {
            'selector': 'th,td',
            'props': [
                ('text-align', 'right'),
                #('border', '1px solid black'),
                ('width', '100px'),
                #('border-spacing', '0'),
                #('border-collapse', 'collapse'),
            ]
        }
    ]

    table.set_table_styles(styles)
    table.format(precision=2, decimal=".")
    table.hide(axis='index')


    html_table = table.to_html()

    with open(f'{broker.lower()}_table.html', "w") as f:
        f.write(html_table)


for broker in brokers:
    s = statements.all_for(broker)
    d = deposits.all_for(broker)
    visu = AccountVisualizer(broker, s, d)
    image_filename = os.path.join(dir, broker.lower() + '.png')
    visu.create(image_filename)