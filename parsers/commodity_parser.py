import requests
from bs4 import BeautifulSoup


class CommodityParser:

    def __init__(self):
        self.url = 'https://markets.businessinsider.com/commodities'
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'lxml')
        self.commodities = ("Natural Gas", "Ethanol", "Heating Oil", "Coal", "RBOB Gasoline", "Uranium", "Oil (Brent)",
                            "Oil (WTI)", "Aluminium", "Lead", "Iron Ore", "Copper", "Nickel", "Zinc", "Tin")
        self.units = {"Natural Gas": 'MMBtu', "Ethanol": 'gallon', "Heating Oil": '100 liter',
                      "Coal": 'ton', "RBOB Gasoline": 'gallon', "Uranium": '250 Pfund',
                      "Oil (Brent)": 'barrel', "Oil (WTI)": 'barrel', "Aluminium": 'ton',
                      "Lead": 'ton', "Iron Ore": 'ton', "Copper": 'ton',
                      "Nickel": 'ton', "Zinc": 'ton', "Tin": 'ton'}

    def _get_commodity_prices(self):
        div_tags = self.soup.find_all('div', {'data-field': "Mid"})[9:24]
        prices = {}
        commodity_index = 0
        for tag in div_tags:
            commodity = self.commodities[commodity_index]
            prices[commodity] = tag.find('span').text.replace(',', ' ')
            commodity_index += 1
        return prices

    def _get_commodity_changes(self):
        div_tags = self.soup.find_all('div', {'data-field': "ChangeAbs"})[5:20]
        changes = {}
        commodity_index = 0
        for tag in div_tags:
            commodity = self.commodities[commodity_index]
            changes[commodity] = tag.find('span').text.replace(',', ' ')
            if '-' not in changes[commodity]:
                changes[commodity] = '+' + changes[commodity]
            commodity_index += 1
        return changes

    def _get_commodity_percent_changes(self):
        div_tags = self.soup.find_all('div', {'data-field': "ChangePer"})[5:20]
        percent_changes = {}
        commodity_index = 0
        for tag in div_tags:
            commodity = self.commodities[commodity_index]
            percent_changes[commodity] = tag.find('span').text.replace(' ', '')
            if '-' not in percent_changes[commodity]:
                percent_changes[commodity] = '+' + percent_changes[commodity]
            commodity_index += 1
        return percent_changes

    def get_commodity_inf(self):
        prices = self._get_commodity_prices()
        changes = self._get_commodity_changes()
        percent_changes = self._get_commodity_percent_changes()
        commodity_inf = ''
        for commodity in self.commodities:
            # line example: Natural Gas (MMBtu) = 2.12 USD (+0.03; +1.63%)
            commodity_inf += (f'{commodity} ({self.units[commodity]}) = {prices[commodity]} USD ({changes[commodity]};'
                              f' {percent_changes[commodity]})\n')
        return commodity_inf
