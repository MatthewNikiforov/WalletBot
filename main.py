import datetime
import telebot

# import all parsers from the parsers package
from parsers.rub_currency_parser import RUBCurrencyParser
from parsers.currency_converter import CurrencyConverter
from parsers.crypto_parser import CryptoParser
from parsers.precious_metals_parser import PreciousMetalsParser
from parsers.global_stock_parser import GlobalStockParser
from parsers.rus_stock_parser import RusStockParser
from parsers.global_indexes_parser import GlobalIndexesParser
from parsers.rus_indexes_parser import RusIndexesParser
from parsers.commodity_parser import CommodityParser


# crete a main bot object
TOKEN = '-'
bot = telebot.TeleBot(TOKEN)

# date in russian date format (dd.mm.yyyy, example: 01.01.1970) will be used in a bot's response message
date = datetime.date.today().strftime('%d.%m.%Y')

# create a commands keyboard
keyboard = telebot.types.ReplyKeyboardMarkup(True)
keyboard.row('/help', '/codes')
keyboard.row('/rates', '/crypto', '/stocks')
keyboard.row('/commodities', '/metals', '/indexes')

# commands handlers
@bot.message_handler(commands=['start'])
def command_start(message):
    bot.send_message(message.chat.id, text='Hello! Write "/help" to see all commands!', reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def command_help(message):
    bot_response = open('help_message.txt', 'r', encoding='UTF-8').read()
    bot.send_message(message.chat.id, bot_response, reply_markup=keyboard)


@bot.message_handler(commands=['codes'])
def command_codes(message):
    bot_response = open('codes_message.txt', 'r', encoding='UTF-8').read()
    bot.send_message(message.chat.id, bot_response)


@bot.message_handler(commands=['crypto'])
def command_crypto(message):
    bot_response = f'📈Date: {date}\n' + CryptoParser().get_crypto_inf()
    bot.send_message(message.chat.id, bot_response)


@bot.message_handler(commands=['stocks'])
def command_stocks(message):
    bot_response = f'📈Date: {date}\n' + GlobalStockParser().get_stock_inf() + RusStockParser().get_stock_inf()
    bot.send_message(message.chat.id, bot_response)


@bot.message_handler(commands=['commodities'])
def command_commodities(message):
    bot_response = f'📈Date: {date}\n' + CommodityParser().get_commodity_inf()
    bot.send_message(message.chat.id, bot_response)


@bot.message_handler(commands=['metals'])
def command_metals(message):
    bot_response = f'📈Date: {date}\n' + PreciousMetalsParser().get_metal_inf()
    bot.send_message(message.chat.id, bot_response)


@bot.message_handler(commands=['indexes'])
def command_indexes(message):
    bot_response = f'📈Date: {date}\n' + GlobalIndexesParser().get_indexes_inf() + RusIndexesParser().get_indexes_inf()
    bot.send_message(message.chat.id, bot_response)


@bot.message_handler(commands=['rates'])
    bot_response = f'💱Date: {date}\n' + RUBCurrencyParser().get_currency_inf()
    bot.send_message(message.chat.id, bot_response)


@bot.message_handler(content_types=['text'])
def command_convert(message):
    """This command converts amount from one currency into another
    request example: 10 USD into JPY
    response example: 10 USD = 1 084.94 JPY"""

    if 'into' in message.text:
        try:
            request = message.text.split()
            # first possible exception (ValueError)
            # error example: aaa eur into rub
            amount = float(request[0])

            if amount < 0:
                # error example: -100 eur into rub
                bot_response = 'Error: invalid amount'

            else:
                from_currency = request[1].upper()
                into_currency = request[3].upper()
                # second possible exception (KeyError)
                # error examples: 100 eur into aaa; 100 aaa into rub
                result = CurrencyConverter().convert(amount, from_currency, into_currency)
                amount = "{:,}".format(amount).replace(",", " ")
                bot_response = f'{amount} {from_currency} = {result} {into_currency}'

        except ValueError:
            bot_response = 'Error: invalid amount'

        except KeyError:
            bot_response = 'Error: invalid currency code'

    else:
        bot_response = 'Error: unknown command'

    bot.send_message(message.chat.id, bot_response)


bot.polling(none_stop=True)
