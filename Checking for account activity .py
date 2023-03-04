import binance
from binance.client import Client

api_key = 'your_api_key'
api_secret = 'your_api_secret'

client = Client(api_key, api_secret)

# Example: get account information
account = client.get_account()
print(account)
