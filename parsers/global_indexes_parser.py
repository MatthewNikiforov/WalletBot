import requests
from bs4 import BeautifulSoup


class GlobalIndexesParser:

    def __init__(self):
        self.url = 'https://investfunds.ru/indicators/global-stock-market/'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'xml')
        self.indexes = self.soup.find_all('a', {'class': "ttl left"})[:-3]

    def _get_indexes_values(self):
        values = self.soup.find_all('div', {'class': 'price'})[:-3]
        return values

    def _get_indexes_changes(self):
        changes = self.soup.find_all('div', {'class': 'differ '})[:-3]
        for index_number in range(len(self.indexes)):
            change = str(changes[index_number].text)[:-1]
            if '-' not in change:
                change = '+' + change
            changes[index_number] = change
        return changes

    def get_indexes_inf(self):
        indexes_inf = ''
        values = self._get_indexes_values()
        changes = self._get_indexes_changes()
        for index_numb in range(len(self.indexes)):
            # line example: Dow Jones: 26 304.68 (+1.14%)
            indexes_inf += f'{self.indexes[index_numb].text}: {values[index_numb].text} ({changes[index_numb]}%)\n'
        return indexes_inf
