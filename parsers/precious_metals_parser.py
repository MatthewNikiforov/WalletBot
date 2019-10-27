import requests
from bs4 import BeautifulSoup


class PreciousMetalsParser:

    def __init__(self):
        self.url = 'https://markets.businessinsider.com/commodities'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        # data_items - div tag attributes
        self.data_items = {'Gold': 'Y0306000000XAU', 'Palladium': 'Y0306000000XPD', 'Platinum': 'Y0306000000XPT',
                           'Rhodium': 'Y0306000000', 'Silver': 'Y0306000000XAG'}

    def _get_metal_prices(self):
        prices = {}
        for data_item in self.data_items:
            price = self.soup.find('div', {'data-field': "Mid", 'data-item': self.data_items[data_item]}).find('span')
            prices[data_item] = price.text.replace(',', ' ')
        return prices

    def _get_metal_changes(self):
        changes = {}
        for data_item in self.data_items:
            change = (self.soup.find('div', {'data-field': "ChangeAbs", 'data-item': self.data_items[data_item]}).
                      find('span').text.replace(',', ' '))
            if '-' not in change:
                change = '+' + change
            changes[data_item] = change
        return changes

    def get_metal_inf(self):
        prices = self._get_metal_prices()
        changes = self._get_metal_changes()
        metal_inf = ''
        for metal in self.data_items:
            # line example: Gold (troy ounce) = 1 506.90 USD (+5.45)
            metal_inf += f'{metal} (troy ounce) = {prices[metal]} USD ({changes[metal]})\n'
        return metal_inf
