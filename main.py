import os
import time

import requests
import telebot

from binance import Client
from telebot import types
from pycoingecko import CoinGeckoAPI
from dotenv import load_dotenv

import pandas as pd

# Забираем клиента(его api и secret api)
client = Client(os.getenv('apikey_binance'), os.getenv('secret_binance'))

# Подключение api CoinGecko
cg = CoinGeckoAPI()

# Получение текущих тикеров с помощью метода get_all_tickers()
tickers = client.get_all_tickers()
# В консоли показаны все тикеры
print(tickers)

# Мы обращаемся к библиотеке pandas и получаем данные, которые находятся в переменное tickers. Также показывает в консоли результат
ticker_df = pd.DataFrame(tickers)
print(ticker_df)

# Переменная depth хранит в себе информацию: получение глубину рынка, с помощью метода get_order_book(в параментрах указываем какую криптовалюту будем использовать)
# Также показываем результат в консоли
depth = client.get_order_book(symbol='BTCUSDT')
print(depth)

# Переменная historical хранит в себе информацию: получение исторических данных по клину из любого диапазона дат
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
        binance_keyboard(message)


# Все функции для работы с CoinGecko
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


# Все функции, которые принадлежат Binance
def binance_keyboard(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Топовая криптовалюта'), types.KeyboardButton('Последние данные'), types.KeyboardButton('strategy'))
    msg = bot.send_message(message.chat.id, 'Выберите что вы хотите', reply_markup=b1)
    bot.register_next_step_handler(msg, choice_buttons_binance)


def choice_buttons_binance(message, ):
    if message.text == 'Топовая криптовалюта':
        top_coin(message)
    elif message.text == 'Последние данные':
        symbol = 'BTCUSDT'
        interval = '1m'
        lookback = '30'
        last_data(symbol, interval, lookback, message)
    elif message.text == 'Strategy':
        strategy()


def top_coin(message):
    all_tickers = pd.DataFrame(client.get_ticker())
    usdt = all_tickers[all_tickers.symbol.str.contains('USDT')]
    work = usdt[~((usdt.symbol.str.contains('UP')) | (usdt.symbol.str.contains('DOWN')))]
    top_coin = work[work.priceChangePercent == work.priceChangePercent.max()]
    top_coin = top_coin.symbol.values[0]
    bot.send_message(message.chat.id, text=f'Самая топовая криптовалюта на текущее время: {top_coin}')


def last_data(symbol, interval, lookback, message):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + 'min ago UTC'))
    frame = frame.iloc[:,:6]
    frame.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
    frame = frame.set_index('Time')
    frame.index = pd.to_datetime(frame.index, unit= 'ms')
    bot.send_message(message.chat.id, f'Последние данные: {frame}')


def strategy(buy_amt, SL=0.985, Target=1.02, open_position=False):
    try:
        asset = top_coin()
        df = last_data(asset, '1m', '120')
    except:
        time.sleep(61)
        asset = top_coin()
        df = last_data(asset, '1m', '120')

    qty = round(buy_amt/df.Close.iloc[-1], 1)

    if ((df.Close.pct_change() + 1).cumprod()).iloc[-1] > 1:
        print(asset)
        print(df.Close.iloc[-1])
        print(qty)
        order = client.create_order(symbol=asset, side='BUY', type='MARKET', quantity = qty)
        print(order)
        buyprice = float(order['fills'][0]['price'])
        open_position = True

        while open_position:
            try:
                df = last_data(asset, '1m', '2')
            except:
                print('Restart after 1 min')
                time.sleep(61)
                df = last_data(asset, '1m', '2')

            print(f'Price ' + str(df.Close[-1]))
            print(f'Target ' + str(buyprice * Target))
            print(f'Stop ' + str(buyprice * SL))
            if df.Close[-1] <= buyprice * SL or df.Close[-1] >= buyprice * Target:
                order = client.create_order(symbol=asset, side='SELL', type='MARKET', quantity = qty)
                print(order)
                break

    else:
        print('No find')
        time.sleep(200)

    while True:
        strategy(15)




# Запуск бота в телеграм
if __name__ == '__main__':
    # get_data()
    print(
        "                                                      ████ \n ░░███                                               ░░███ \n ███████   █████ ███ █████  ██████  ████████   █████  ░███ \n░░░███░   ░░███ ░███░░███  ███░░███░░███░░███ ███░░   ░███ \n  ░███     ░███ ░███ ░███ ░███████  ░███ ░░░ ░░█████  ░███ \n  ░███ ███ ░░███████████  ░███░░░   ░███      ░░░░███ ░███ \n  ░░█████   ░░████░████   ░░██████  ░███████  ██████  █████\n   ░░░░░     ░░░░ ░░░░     ░░░░░░  ░░░░░     ░░░░░░  ░░░░░ \n                                                           \n                                                           \n                                                           \nBot started successfully")
    bot.polling()
    print("Bot stopped")
