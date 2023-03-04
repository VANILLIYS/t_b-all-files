#стратегия пересечения скользящей средней

import numpy as np
import pandas as pd
from binance.client import Client
import time

# Определить параметры торговли
symbol = 'BTCUSDT'
fast_ma = 50
slow_ma = 200
quantity = 0.001
sleep_time = 10  # Время сна между сделками в секундах

# Подключение к API Binance
api_key = 'your_api_key'
api_secret = 'your_api_secret'
client = Client(api_key, api_secret)

# Определите торговую функцию
def trade(symbol, fast_ma, slow_ma, quantity):
    # Получить исторические данные
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "1 day ago UTC")
    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)

    # Рассчитать скользящие средние
    df['fast_ma'] = df['close'].rolling(window=fast_ma).mean()
    df['slow_ma'] = df['close'].rolling(window=slow_ma).mean()

    # Покупайте или продавайте на основе пересечений
    if df['fast_ma'].iloc[-1] > df['slow_ma'].iloc[-1]:
        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print('Размещен заказ на покупку')
    elif df['fast_ma'].iloc[-1] < df['slow_ma'].iloc[-1]:
        order = client.create_order(
            symbol=symbol,
            side=Client.SIDE_SELL,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quantity
        )
        print('Размещен ордер на продажу')
    else:
        print('Нет торговли')

# Запуск торговой функции до бесконечности
while True:
    try:
        trade(symbol, fast_ma, slow_ma, quantity)
    except Exception as e:
        print(e)
    time.sleep(sleep_time)
