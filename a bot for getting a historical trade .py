import binance
from binance.client import Client
import pandas as pd

# Установите учетные данные API
api_secret = 'bAHOwf4qeVRauAQothC68kDKmYs6Ygs3SrXEVjtpyzyiLMWhQ8mizB7XWx5EOUZO'
api_key = 'p3qbaeitQRkHv8ETwoCFwvPDoIhBUx0XQFY2cPwNeRkSdUKpjH6CDPeoCbB8rjJP'

# Создайте экземпляр клиента
client = Client(api_key, api_secret)

# Получение исторических ценовых данных для выбранной торговой пары
symbol = 'BTCUSDT'
timeframe = '1h'
csv_name = symbol + '_' + timeframe + '_historical_price_data.csv'

df = client.get_historical_klines(symbol, timeframe)

# Преобразование данных в DataFrame
df = pd.DataFrame(df, columns=['Open Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close Time', 'Quote Asset Volume', 'Number of Trades', 'Taker Buy Base Asset Volume', 'Taker Buy Quote Asset Volume', 'Ignore'])

# Создание торгового бота
def trading_bot(df):
    # Логика здесь

# Выполнить работу торгового бота
    trading_bot(df)

# Экспорт данных в файл CSV
df.to_csv(csv_name, index=False)

#Этот торговый бот позволит вам получить доступ к историческим ценовым данным для выбранной торговой пары, а затем использовать их для создания торгового бота, который может совершать сделки на основе вашей собственной логики.

