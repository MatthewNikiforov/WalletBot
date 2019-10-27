import datetime
import requests


class CurrencyParser:

    def __init__(self, currency_base):
        self.base = currency_base  # EUR or USD
        self.today = str(datetime.date.today())
        # data isn't uploaded every day, so need to take data from 7 days in order to avoid getting an empty data
        self.previous_date = str(datetime.date.today() - datetime.timedelta(days=7))
        self.url = (f'https://api.exchangeratesapi.io/history?start_at={self.previous_date}&end_at={self.today}' 
                    f'&base={self.base}')

    def _get_currency_rates(self):
        rates = {}
        # list of rates per each date from today to previous_date (today - 0 index, last upload date index - 1, etc.)
        dates_list = list(requests.get(self.url).json()['rates'].keys())
        data = requests.get(self.url).json()['rates'][dates_list[0]]
        for currency_code in data:
            if currency_code != self.base:
                rate = str(round(data[currency_code], 2))
                rates[currency_code] = rate
        return rates

    def _get_currency_changes(self):
        changes = {}
        # list of rates per each date from today to previous_date (today - 0 index, last upload date index - 1, etc.)
        dates_list = list(requests.get(self.url).json()['rates'].keys())
        current_data = requests.get(self.url).json()['rates'][dates_list[0]]
        previous_data = requests.get(self.url).json()['rates'][dates_list[1]]
        for currency_code in current_data:
            if currency_code != self.base:
                change = round(current_data[currency_code] - previous_data[currency_code], 2)
                # change format: +non-negative, -negative
                # examples: +0.0; +0.1; -0.1
                if '-' not in str(change):
                    change = '+' + str(change)
                changes[currency_code] = change
        return changes

    def get_currency_inf(self):
        currency_inf = ''
        rates = self._get_currency_rates()
        changes = self._get_currency_changes()
        for currency_code in rates:
            # line example: USD = 1.33 CAD (+0.01)
            currency_inf += f'{self.base} = {rates[currency_code]} {currency_code} ({changes[currency_code]})\n'
        return currency_inf
