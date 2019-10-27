import requests


class RUBCurrencyParser:

    def __init__(self):
        self.url = 'https://www.cbr-xml-daily.ru/daily_json.js'
        self.response = requests.get(self.url).json()
        self.rates = self.response['Valute']

    def _get_currency_rates(self):
        currency_rates = {}
        for currency_code in self.rates:
            # rates presented in this format: [nominal] [currency] = [rate] RUB
            # example: 100 AMD = 13.6698 RUB
            # to convert '[nominal] [currency] = [rate] RUB' format to '[currency] = [rate] RUB'
            # need to divide rate by nominal
            # example: AMD = 0.136698 RUB (13.6698 / 100)
            currency_rate = round(self.rates[currency_code]['Value'] / self.rates[currency_code]['Nominal'], 2)
            currency_rates[currency_code] = currency_rate
        return currency_rates

    def _get_currency_changes(self):
        changes = {}
        for currency_code in self.rates:
            current_rate = self.rates[currency_code]['Value'] / self.rates[currency_code]['Nominal']
            previous_rate = self.rates[currency_code]['Previous'] / self.rates[currency_code]['Nominal']
            change = round(current_rate - previous_rate, 2)
            # change format: +non negative, -negative
            # examples: +0.0; +0.1; -0.1
            if '-' not in str(change):
                change = '+' + str(change)
            changes[currency_code] = change
        return changes

    def get_currency_inf(self):
        currency_inf = ''
        rates = self._get_currency_rates()
        changes = self._get_currency_changes()
        for currency_code in self.rates:
            # line example: AUD = 44.16 RUB (+0.38)
            currency_inf += f'{currency_code} = {rates[currency_code]} RUB ({changes[currency_code]}) \n'
        return currency_inf
