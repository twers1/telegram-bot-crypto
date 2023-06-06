# def get_data():
#     req = requests.get('https://yobit.net/api/3/ticker/ltc_btc')
#     response = req.json()
#     print(response)
#     sell_price = response["ltc_btc"]["sell"]
#     print(f"{datetime.now().strftime('%Y-%m-%d %H:%H')}\nSell BTC price: {sell_price}")