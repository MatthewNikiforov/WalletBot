import requests
from bs4 import BeautifulSoup


class RusIndexesParser:

    def __init__(self):
        self.url = 'https://investfunds.ru/indicators/russian-stock-market/'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'xml')
        self.indexes = self.soup.find_all('a', {'class': "ttl left"})[:2]

    def _get_indexes_values(self):
        values = self.soup.find_all('div', {'class': 'price'})[:2]
        return values

    def _get_indexes_changes(self):
        changes = self.soup.find_all('div', {'class': 'differ '})[:2]
        for index_number in range(len(self.indexes)):
            change = str(changes[index_number].text)[:-1]
            if '-' not in change:
                change = '+' + change
            changes[index_number] = change
        return changes

    def get_indexes_inf(self):
        values = self._get_indexes_values()
        changes = self._get_indexes_changes()
        # example:
        # MoscowExchange: 2 696.69 (+0.81%)
        # RTS: 1 303.80 (+1.47%)
        indexes_inf = (f'MoscowExchange: {values[0].text} ({changes[0]}%)\n' 
                       f'RTS: {values[1].text} ({changes[1]}%)')
        return indexes_inf
