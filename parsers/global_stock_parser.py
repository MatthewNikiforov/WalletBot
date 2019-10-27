import datetime
import requests


class GlobalStockParser:

    def __init__(self):
        self.token = '-'
        self.date = str(datetime.datetime.today() - datetime.timedelta(days=7))
        self.main_url = 'https://api.tiingo.com/tiingo/daily/{}/prices?startDate=' + self.date + '&token=' + self.token
        self.company_codes = {'GOOGL': 'Google', 'INTC': 'Intel', 'AAPL': 'Apple', 'MSFT': 'Microsoft',
                              'HPQ': 'HP', 'NVDA': 'Nvidia', 'FB': 'Facebook', 'ORCL': 'Oracle',
                              'TWTR': 'Twitter', 'TSLA': 'Tesla', 'V': 'Visa', 'PYPL': 'PayPal',
                              'WMT': 'Walmart', 'BA': 'Boeing', 'EBAY': 'eBay', 'AMZN': 'Amazon'}

    def _get_stock_prices(self):
        prices = {}
        for company_code in self.company_codes:
            url = self.main_url.format(company_code)
            data = requests.get(url).json()[-1]
            price = data['close']
            price = str('{:,}'.format(price).replace(',', ' '))
            prices[company_code] = price
        return prices

    def _get_stock_changes(self):
        changes = {}
        for company_code in self.company_codes:
            url = self.main_url.format(company_code)
            data = requests.get(url).json()
            current_price = data[-1]['close']
            previous_price = data[-2]['close']
            change = current_price - previous_price
            change = str(round(change, 2))
            if '-' not in change:
                change = '+' + change
            changes[company_code] = change
        return changes

    def _get_stock_percent_changes(self):
        percent_changes = {}
        for company_code in self.company_codes:
            url = self.main_url.format(company_code)
            data = requests.get(url).json()
            current_price = data[-1]['close']
            previous_price = data[-2]['close']
            # proportion: previous_price / 100(%) = current_price / current_percent(%) ->
            # current_percent = current_price / (previous_price / 100) = (current_price * 100) / previous_price
            # example: 300 / 100 = 600 / current_percent -> current_percent = 200 % (600 = 200 % of 300)
            current_percent = (current_price * 100) / previous_price
            # example: 200 % - 100 % = 100 % (from 300 to 600 - 100 % increase)
            percent_change = current_percent - 100
            percent_change = str(round(percent_change, 2))
            if '-' not in percent_change:
                percent_change = '+' + percent_change
            percent_changes[company_code] = percent_change
        return percent_changes

    def get_stock_inf(self):
        prices = self._get_stock_prices()
        changes = self._get_stock_changes()
        percent_changes = self._get_stock_percent_changes()
        stock_inf = ''
        for company_code in self.company_codes:
            # line example: Google: 1 175.91 USD (+4.83; +0.41%)
            stock_inf += (f'{self.company_codes[company_code]}: {prices[company_code]} USD ' 
                          f'({changes[company_code]}; {percent_changes[company_code]}%)\n')
        return stock_inf
