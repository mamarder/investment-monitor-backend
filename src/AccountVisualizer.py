


import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np


class AccountVisualizer:

    def __init__(self, broker : str, statements : pd.DataFrame, deposits : pd.DataFrame) -> None:
        self.broker = broker
        self.statements = statements
        self.deposits = deposits
        self.cum_deposits = deposits
        self.cum_deposits.loc[:, 'src_value'] = deposits['src_value'].cumsum()
        self.cum_deposits.loc[:, 'dest_value'] = deposits['dest_value'].cumsum()
        self.date_formatter = mdates.DateFormatter('%Y-%m')

    def _results_for_statement_(self, statement) -> float:
            filtered_deposits =  self.cum_deposits[ self.cum_deposits['date'] <= statement.date]
            
            if filtered_deposits.empty:
                raise Exception('Error: No deposits found in account before first account statement.')

            latest_deposit = filtered_deposits.tail(n=1) # latest deposit before the statement
            latest_deposit_value = latest_deposit['dest_value'].item()

            result_abs = statement.value - latest_deposit_value
            result_rel = result_abs/latest_deposit_value

            return  (result_abs, result_rel)
    

    def _plot_result_(self, ax, x, y, y_label, legend):
         
      
        spacing = np.diff(x).min()  # Find the minimum spacing between x-values
        bar_width = 0.25 * spacing

       
        colors = ['green' if _y >= 0 else 'red' for _y in y]

        ax.bar(x, y, label = legend,  color = colors, width = bar_width)
        ax.set_xlabel('Date')
        ax.set_ylabel(y_label)
        ax.legend()
        ax.grid()
        ax.xaxis.set_major_formatter(self.date_formatter)
    
         
    def _plot_value_(self, ax, x_sta, y_sta, x_dep, y_dep, y_label):
         
        ax.scatter(x_sta, y_sta, label = 'account value (incl. unrealized)',  color = 'blue', marker='o')
        ax.scatter(x_dep, y_dep, label = 'deposits (cumulated)', color = 'green', marker='o')
        ax.set_xlabel('Date')
        ax.set_ylabel(y_label)
        ax.legend()
        ax.grid()
        ax.xaxis.set_major_formatter(self.date_formatter)


    def create(self, image_filename : str):

        statements_currency = self.statements['currency'].to_list()[0]


        deposits_src_values =  self.cum_deposits['src_value'].to_list()
        deposits_src_currency =  self.cum_deposits['src_currency'].to_list()[0]

        deposits_dest_values =  self.cum_deposits['dest_value'].to_list()
        deposits_dest_currency =  self.cum_deposits['dest_currency'].to_list()[0]

        deposits_dates =  self.cum_deposits['date'].to_list()

        results = pd.DataFrame(columns=['date','result_abs','result_rel'])
        results['date'] = self.statements['date']

        for index, statement in self.statements.iterrows():

            result_abs, result_rel = self._results_for_statement_(statement)

            results.loc[index, 'result_abs'] = result_abs
            results.loc[index, 'result_rel'] = result_rel

                
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(10,6), sharex=True)

        plt.suptitle(f'{self.broker} Account Overview')

        # plot account value (deposits and statements)
        x_sta = self.statements['date'].to_list()
        y_sta = self.statements['value'].to_list()
        x_dep =  self.cum_deposits['date'].to_list()
        y_dep =  self.cum_deposits['dest_value'].to_list()
        y_label = f'[{statements_currency}]'
        self._plot_value_(ax[0], x_sta, y_sta, x_dep, y_dep, y_label)

        # plot account result (abs)
        x_values = results['date'].to_list()
        y_values = results['result_abs'].to_list()
        y_label = f'[{statements_currency}]'
        self._plot_result_(ax[1], x_values, y_values, y_label, 'result (abs)')

        #y_values = results['result_rel'].to_list()
        #y_label = '[-]'
        #self._plot_result_(ax[2], x_values, y_values, y_label, 'result (rel)')


        plt.tight_layout()
        plt.savefig(image_filename)

