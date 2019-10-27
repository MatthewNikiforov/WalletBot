import requests
from bs4 import BeautifulSoup


class RusStockParser:

    def __init__(self):
        self.url = 'https://www.finanz.ru/aktsii/realnom-vremeni-spisok/micex'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        self.stock_data_items = {'Gazprom': 'Y0101225000112009', 'Sberbank': 'Y0101225000541354',
                                 'Yandex': 'Y010122500012955842', 'Aeroflot': 'Y0101225000587479',
                                 'Lukoil': 'Y0101225000273916', 'Rosneft': 'Y01012250002613889',
                                 'Rostelecom': 'Y0101225000420385', 'VTB': 'Y01012250002756931'}

    def _get_stock_prices(self):
        prices = {}
        for company_key in self.stock_data_items:
            price = self.soup.find('div', {'data-item': self.stock_data_items[company_key],
                                           'data-field': 'Mid'}).find('span')
            prices[company_key] = str(price.text).replace(',', '.').replace('Т', '')
        return prices

    def _get_stock_changes(self):
        changes = {}
        for company_key in self.stock_data_items:
            change = self.soup.find('div', {'data-item': self.stock_data_items[company_key],
                                            'data-field': 'ChangeAbs'}).find('span')
            change = str(change.text).replace(',', '.').replace('Т', '')
            if '-' not in change:
                change = '+' + change
            changes[company_key] = change
        return changes

    def _get_stock_percent_changes(self):
        percent_changes = {}
        for company_key in self.stock_data_items:
            percent_change = self.soup.find('div', {'data-item': self.stock_data_items[company_key],
                                                    'data-field': 'ChangePer'}).find('span')
            percent_change = str(percent_change.text).replace(' ', '')
            if '-' not in percent_change:
                percent_change = '+' + percent_change
            percent_changes[company_key] = percent_change.replace(',', '.')
        return percent_changes

    def get_stock_inf(self):
        prices = self._get_stock_prices()
        changes = self._get_stock_changes()
        percent_changes = self._get_stock_percent_changes()
        stock_inf = ''
        for company_key in self.stock_data_items:
            # line example: Yandex: 2 413.20 RUB (-15.60; -0.64%)
            stock_inf += (f'{company_key}: {prices[company_key]} RUB ({changes[company_key]}; '
                          f'{percent_changes[company_key]})\n')
        return stock_inf
