import requests


class CryptoParser:

    def __init__(self):
        self.api_key = '-'
        self.symbols = ('BTC', 'ETH', 'EOS', 'MIOTA', 'LTC', 'XRP', 'NMC', 'PPC', 'NVC')
        self.url = (f'https://min-api.cryptocompare.com/data/pricemulti?fsyms={",".join(self.symbols)}&'
                    f'tsyms=USD&api_key={self.api_key}')
        self.response = requests.get(self.url)
        self.data = self.response.json()

    def _get_crypto_rates(self):
        rates = {}
        for crypto_code in self.symbols:
            crypto_rate = round(self.data[crypto_code]['USD'], 2)
            crypto_rate = str('{:,}'.format(crypto_rate).replace(',', ' '))
            rates[crypto_code] = crypto_rate
        return rates

    def _get_crypto_changes(self):
        changes = {}
        for crypto_code in self.symbols:
            previous_data_url = f'https://min-api.cryptocompare.com/data/histoday?fsym={crypto_code}&tsym=USD&limit=2'
            previous_data = requests.get(previous_data_url).json()
            previous_price = previous_data['Data'][1]['close']
            changes[crypto_code] = round(self.data[crypto_code]['USD'] - previous_price, 2)
            if '-' not in str(changes[crypto_code]):
                changes[crypto_code] = '+' + str(changes[crypto_code])
        return changes

    def get_crypto_inf(self):
        crypto_inf = ''
        rates = self._get_crypto_rates()
        changes = self._get_crypto_changes()
        for crypto_code in self.data:
            # line example: BTC = 11 652.39 USD (-321.89)
            crypto_inf += f'{crypto_code} = {rates[crypto_code]} USD ({changes[crypto_code]})\n'
        return crypto_inf
