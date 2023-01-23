import requests
import json

from CurrencyExchangeBot.config import api_key, currencies


class APIException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(base, quote, amount):

        try:
            base_key = currencies[str(base.lower())]
        except KeyError:
            raise APIException(f"Валюта под названием {base} не найдена!")

        try:
            quote_key = currencies[str(quote.lower())]
        except KeyError:
            raise APIException(f"Валюта под названием {quote} не найдена!")

        if base_key == quote_key:
            raise APIException(f"Вы конвертируете две одинаковых валюты!")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Некорректное значение количества валюты {amount}!")

        # try:
        #     amount = float(amount.replace(",", "."))
        # except ValueError:
        #     raise APIException(f"Не удалось обработать количество валюты {amount}!")

        if not amount:
            raise APIException(f"Вы ничего не конвертируете!")

        if amount <= 0:
            raise APIException(f"Нельзя конвертировать отрицательное количество валюты!")

        req = requests.get(f"https://v6.exchangerate-api.com/v6/{api_key}/pair/"
                           f"{base_key}/{quote_key}/{amount}")
        result = json.loads(req.content)["conversion_result"]
        message = f"{amount} {base} = {result} {quote}."
        return message
