import time
import numpy as np
from binance.client import Client
from binance.enums import *

# Инициализируйте клиент Binance с вашими ключами API
api_key = 'your_api_key'
api_secret = 'your_api_secret'
client = Client(api_key, api_secret)

# Установите торговый символ, например, "BTCUSDT".
symbol = "BTCUSDT"

# Установите временной интервал для ценовых данных, например, "1h" для 1 часовой свечи
interval = KLINE_INTERVAL_1HOUR

# Установите длину периода SMA, например, 50
sma_period = 50

# Установите количество актива для покупки/продажи, например, 0.001 BTC
trade_quantity = 0.001

# Определите функцию для получения последних данных о цене и вычисления SMA
def get_sma():
    # Получить последние данные о ценах с Binance
    klines = client.get_historical_klines(symbol, interval, "1000 hours ago UTC")

    # Извлечение цен закрытия
    prices = np.array([float(kline[4]) for kline in klines])

    # Вычислите SMA с помощью numpy
    sma = np.mean(prices[-sma_period:])

    return sma

# Определите функцию для покупки актива, если цена пересекает выше SMA
def buy():
    # Получить текущий баланс активов
    asset_balance = float(client.get_asset_balance(asset=symbol[:-4])['free'])

    # Получить текущую цену
    price = float(client.get_symbol_ticker(symbol=symbol)['price'])

    # Рассчитать сумму сделки
    amount = trade_quantity / price

    # Разместить рыночный ордер на покупку актива
    order = client.create_order(
        symbol=symbol,
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=amount
    )

    print("Bought", trade_quantity, symbol[:-4], "at", price, "for", order['cummulativeQuoteQty'], "USDT")

# Определите функцию для продажи актива, если цена пересекает ниже SMA
def sell():
    # Получить текущий баланс активов
    asset_balance = float(client.get_asset_balance(asset=symbol[:-4])['free'])

    # Получить текущую цену
    price = float(client.get_symbol_ticker(symbol=symbol)['price'])

    # Разместить рыночный ордер на покупку актива
    order = client.create_order(
        symbol=symbol,
        side=SIDE_SELL,
        type=ORDER_TYPE_MARKET,
        quantity=asset_balance
    )

    print("Sold", asset_balance, symbol[:-4], "at", price, "for", order['cummulativeQuoteQty'], "USDT")

# Запустите бесконечный цикл, чтобы постоянно проверять цену и заключать сделки
while True:
    try:
        # Получить текущую SMA
        sma = get_sma()

        # Получить текущую цену
        price = float(client.get_symbol_ticker(symbol=symbol)['price'])

        # Проверьте, пересеклась ли цена над SMA.
        if price > sma:
            buy()

        # Проверьте, пересекается ли цена ниже SMA
        if price < sma:
            sell()

        # Дождитесь закрытия следующей свечи
        time.sleep(3600)  # подождите 1 час для свечей 1h
    except Exception as e:
        print(e)
        time.sleep(60) # подождите 1 минуту, если произошла ошибка
