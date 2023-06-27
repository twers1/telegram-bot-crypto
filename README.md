# Crypto bot parsing

## What exchanges are there? 

Used binance and coin gecko to get current values in crypto

## Features in CoinGecko

- viewing exchange rates in USD
- Viewing exchange rates in RUB 
- conversion  

## Features in Binance 

- top cryptocurrency at the moment
- recent data

## Demo 


## Docker

```
docker build -t parsing-bot .

docker run -e TOKEN= -e apikey_binance= -e secret_binance= parsing-bot
```


# Бот, занимающийся парсингом криптовалютных бирж

## Какие биржи были использованы? 

Использованы биржи: Binance и CoinGecko(для получения актуальных данных)

## Функции в CoinGecko

- просмотр обменных курсов в долларах 
- просмотр обменных курсов в рублях 
- конвертация

## Функции в Binance

- просмотр текущей топовой криптовалюты 
- последние данные


## Демонстрация 

## Docker

```
docker build -t parsing-bot .

docker run -e TOKEN= -e apikey_binance= -e secret_binance= parsing-bot
```