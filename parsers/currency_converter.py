import requests


class CurrencyConverter:

    def __init__(self):
        self.api_key = '-'
        self.main_url = 'https://free.currconv.com/api/v7/convert?q={}&compact=ultra&apiKey=' + self.api_key

    def convert(self, amount, from_currency, into_currency):
        # url requires this format of currency codes: USD_EUR
        convert_codes = from_currency.upper() + '_' + into_currency.upper()
        convert_url = self.main_url.format(convert_codes)
        convert_data = requests.get(convert_url).json()
        result = round(amount * convert_data[convert_codes], 2)
        # to separate digits to groups of three
        # example: 123456789 -> 1 234 567.89
        result = str('{:,}'.format(result).replace(',', ' '))
        return result
