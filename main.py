import os
import requests
import telebot

from binance import Client
from telebot import types
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv

import pandas as pd

client = Client(os.getenv('apikey_binance'), os.getenv('secret_binance'))
cg = CoinGeckoAPI()
tickers = client.get_all_tickers()
print(tickers)
ticker_df = pd.DataFrame(tickers)
print(ticker_df)
float(ticker_df.loc['ETHBTC']['price'])
depth = client.get_order_book(symbol='BTCUSDT')
print(depth)
historical = client.get_historical_klines('ETHBTC', Client.KLINE_INTERVAL_1DAY, '8 June 2023')

load_dotenv()
bot = telebot.TeleBot(os.getenv('TOKEN'))


# Данная функция при нажатии "START" - выводит текст приветствия и кнопки с выбором биржи
@bot.message_handler(commands=['start'])
def main(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton(text='Coin Gecko'), types.KeyboardButton(text='Binance'))
    cr = bot.send_message(message.chat.id,
                          text='Привет! Я бот, который занимается криптовалютой\nВы сможете тут узнать курс любой валюты\n',
                          reply_markup=b1)
    bot.register_next_step_handler(cr, step)


# Функция для выбора биржи
def step(message):
    if message.text == 'Coin Gecko':
        step1(message)
    elif message.text == 'Binance':
        pass


# Данная функция даёт выбрать нужную криптовалюту
def convert1(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Bitcoin'), types.KeyboardButton('Ethereum'), types.KeyboardButton('Litecoin'),
           types.KeyboardButton('Polygon'), types.KeyboardButton('Uniswap'), types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, 'Выберите криптовалюту', reply_markup=b1)
    bot.register_next_step_handler(msg, convert2)


# Данная функция предалагает конвертировать нужную криптовалюту
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


# Данная функция конвертирует криптовалюту BTC в доллары
def bbtc(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='bitcoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} BTC == {price["bitcoin"]["usd"] * convert2} $')
    main(message)


# Данная функция конвертирует криптовалюту ETH в доллары
def eeth(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='ethereum', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} ETH == {price["ethereum"]["usd"] * convert2} $')
    main(message)


# Данная функция конвертирует криптовалюту LTC в доллары
def lltc(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='litecoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} LTC == {price["litecoin"]["usd"] * convert2} $')
    main(message)


# Данная функция конвертирует криптовалюту MATIC в доллары
def mmatic(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='matic-network', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} Matic == {price["matic-network"]["usd"] * convert2} $')
    main(message)


# Данная функция конвертирует криптовалюту UNI в доллары
def uuni(message):
    convert2 = message.text
    convert2 = int(convert2)

    price = cg.get_price(ids='uniswap', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{convert2} UNI == {price["uniswap"]["usd"] * convert2} $')
    main(message)


# Функция предлагает выбрать дальнейшие действия для работы с биржей
def step1(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Курс криптовалюты'), types.KeyboardButton('Конвертер'))
    msg = bot.send_message(message.chat.id, 'Выберите что вы хотите', reply_markup=b1)
    bot.register_next_step_handler(msg, choice_buttons)


def choice_buttons(message):
    if message.text == 'Курс криптовалюты':
        step3(message)
    elif message.text == 'Конвертер':
        convert1(message)


# Функция выбора дальнейших действий для работы с криптовалютой
def step3(message):
    b2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b2.add(types.KeyboardButton('Курс к USD'), types.KeyboardButton('Курс к RUB'), types.KeyboardButton('Главное меню'))
    q = bot.send_message(message.chat.id, 'Выберите курс: ', reply_markup=b2)
    bot.register_next_step_handler(q, step4)


# Функция для вывода курса криптовалюты к USD и RUB
def step4(message):
    if message.text == 'Курс к USD':
        price = cg.get_price(ids='bitcoin-cash, ethereum, litecoin, matic-network, uniswap, bitcoin', vs_currencies='usd')
        bot.send_message(message.chat.id, f'Bitcoin Cash== {price["bitcoin-cash"]["usd"]} $\n'
                                      f'Ethereum == {price["ethereum"]["usd"]} $\n'
                                      f'Litecoin == {price["litecoin"]["usd"]} $\n'
                                      f'Polygon == {price["matic-network"]["usd"]} $\n'
                                      f'Uniswap == {price["uniswap"]["usd"]} $\n'
                                      f'Bitcoin == {price["bitcoin"]["usd"]} $')
        step3(message)

    elif message.text == 'Курс к RUB':
        price = cg.get_price(ids='bitcoin-cash, ethereum, litecoin, matic-network, uniswap, bitcoin', vs_currencies='rub')
        bot.send_message(message.chat.id, f'Bitcoin Cash== {price["bitcoin-cash"]["rub"]} ₽\n'
                                      f'Ethereum == {price["ethereum"]["rub"]} ₽\n'
                                      f'Litecoin == {price["litecoin"]["rub"]} ₽\n'
                                      f'Polygon == {price["matic-network"]["rub"]} ₽\n'
                                      f'Uniswap == {price["uniswap"]["rub"]} ₽\n'
                                      f'Bitcoin == {price["bitcoin"]["rub"]} ₽')
        step3(message)

    elif message.text == 'Главное меню':
        main(message)


# Запуск бота в телеграм
if __name__ == '__main__':
    # get_data()
    bot.polling()

