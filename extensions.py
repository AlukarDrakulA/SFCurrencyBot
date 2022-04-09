import requests
import json
from config import keys


class ConvertionException(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):
        if quote == base:
            raise ConvertionException(
                f'Невозможно перевести одинаковые валюты {base}.')

        try:
            base_currancy = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}.')

        try:
            quote_currancy = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}.')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(
                f'Не удалось обработать количество {amount}.')

        r = requests.get(
            f'https://api.binance.com/api/v3/ticker/price?symbol={base_currancy}{quote_currancy}')
        price = json.loads(r.content)['price']
        total_price = float(price) * float(amount)

        return total_price
