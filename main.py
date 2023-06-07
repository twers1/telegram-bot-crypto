import os
import requests
import telebot

from telebot import types
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv



cg = CoinGeckoAPI()

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


@bot.message_handler(commands=['start'])
def main(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton(text='Курс крипты'), types.KeyboardButton(text='Курс фиата'), types.KeyboardButton(text='Конвертер'))
    cr = bot.send_message(message.chat.id,
                          text='Привет! Я бот, который занимается криптовалютой\nВы сможете тут узнать курс любой валюты\n',
                          reply_markup=b1)
    bot.register_next_step_handler(cr, step)


def step(message):
    if message.text == 'Курс крипты':
        step2(message)
    elif message.text == 'Курс фиата':
        fiat(message)
    elif message.text == 'Конвертер':
        convert1(message)


def convert1(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Bitcoin'), types.KeyboardButton('Ethereum'), types.KeyboardButton('Litecoin'),
           types.KeyboardButton('Polygon'), types.KeyboardButton('Uniswap'), types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, 'Выберите криптовалюту', reply_markup=b1)
    bot.register_next_step_handler(msg, convert2)


def convert2(message):
    if message.text == 'Bitcoin':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать BTC?')
        bot.register_next_step_handler(msg, bbtc)
    elif message.text == 'Ethereum':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать ETH?')
        bot.register_next_step_handler(msg, eeth)
    elif message.text == 'Litecoin':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать LTC?')
        bot.register_next_step_handler(msg, lltc)
    elif message.text == 'Polygon':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать MATIC?')
        bot.register_next_step_handler(msg, mmatic)
    elif message.text == 'Uniswap':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать UNI?')
        bot.register_next_step_handler(msg, uuni)
    elif message.text == 'Назад':
        main(message)


def bbtc(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='bitcoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} BTC == {price["bitcoin"]["usd"] * convert2} $')
    main(message)


def eeth(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='bitcoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} ETH == {price["ethereum"]["usd"] * convert2} $')


def lltc(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='bitcoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} BTC == {price["bitcoin"]["usd"] * convert2} $')


def mmatic(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='bitcoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} BTC == {price["bitcoin"]["usd"] * convert2} $')


def uuni(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='bitcoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} BTC == {price["bitcoin"]["usd"] * convert2} $')


def step2(message):
    b2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b2.add(types.KeyboardButton('Курс к USD'), types.KeyboardButton('Курс к RUB'), types.KeyboardButton('Главное меню'))
    q = bot.send_message(message.chat.id, 'Выберите курс: ', reply_markup=b2)
    bot.register_next_step_handler(q, step3)


def fiat(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('USD'), types.KeyboardButton('RUB'), types.KeyboardButton('Главная'))
    q = bot.send_message(message.chat.id, 'Курс фиата:', reply_markup=b1)
    bot.register_next_step_handler(q, fiat_step2)


def fiat_step2(message):
    if message.text == 'USD':
        price = convert(base='USD', amount=1, to=['RUB', 'EUR'])
        bot.send_message(message.chat.id, f'1 USD == {price["RUB"]}\n'
                                          f'1 USD == {price["EUR"]}')


def step3(message):
    b2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b2.add(types.KeyboardButton('Назад'))
    if message.text == 'Курс к USD':
        price = cg.get_price(ids='bitcoin-cash, ethereum, litecoin, matic-network, uniswap, bitcoin', vs_currencies='usd')
        bot.send_message(message.chat.id, f'Bitcoin Cash== {price["bitcoin-cash"]["usd"]} $\n'
                                      f'Ethereum == {price["ethereum"]["usd"]} $\n'
                                      f'Litecoin == {price["litecoin"]["usd"]} $\n'
                                      f'Polygon == {price["matic-network"]["usd"]} $\n'
                                      f'Uniswap == {price["uniswap"]["usd"]} $\n'
                                      f'Bitcoin == {price["bitcoin"]["usd"]} $', reply_markup=b2)
    elif message.text == 'Курс к RUB':
        price = cg.get_price(ids='bitcoin-cash, ethereum, litecoin, matic-network, uniswap, bitcoin', vs_currencies='rub')
        bot.send_message(message.chat.id, f'Bitcoin Cash== {price["bitcoin-cash"]["rub"]} ₽\n'
                                      f'Ethereum == {price["ethereum"]["rub"]} ₽\n'
                                      f'Litecoin == {price["litecoin"]["rub"]} ₽\n'
                                      f'Polygon == {price["matic-network"]["rub"]} ₽\n'
                                      f'Uniswap == {price["uniswap"]["rub"]} ₽\n'
                                      f'Bitcoin == {price["bitcoin"]["rub"]} ₽', reply_markup=b2)
    elif message.text == 'Главная':
        main(message)

    go_main = bot.send_message(message.chat.id, 'Вернуться назад: ', reply_markup=b2)
    bot.register_next_step_handler(go_main, step2)




if __name__ == '__main__':
    # get_data()
    bot.polling()

