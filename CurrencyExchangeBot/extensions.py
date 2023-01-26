import requests
import json

# импорт API-ключа и словаря валют
from CurrencyExchangeBot.config import currencies
from CurrencyExchangeBot.personal import API_KEY


class APIException(Exception):
    """Кастомный класс для вызова будущих собственных исключений."""
    pass


class Converter:
    """Класс для создания статического метода для вытаскивания
    итогового значения конвертации валют."""

    @staticmethod
    def get_price(base: str, quote: str, amount: str) -> str:
        # если не нашли совпадений по первой введённой валюте
        try:
            base_key = currencies[str(base.lower())]
        except KeyError:
            raise APIException(f"Валюта под названием {base} не найдена!")
        # аналогично для второй валюты
        try:
            quote_key = currencies[str(quote.lower())]
        except KeyError:
            raise APIException(f"Валюта под названием {quote} не найдена!")
        # если валюты совпали
        if base_key == quote_key:
            raise APIException(f"Вы конвертируете две одинаковых валюты!")
        # если третьим значением ввели не (совсем) число
        try:
            amount = float(amount.replace(",", "."))
        except ValueError:
            raise APIException(f"Некорректное значение количества валюты {amount}!")
        # если ввели ноль
        if not amount:
            raise APIException(f"Вы ничего не конвертируете!")
        # если значение слишком мало
        if 0 < amount < 0.001:
            raise APIException(f"Введённое значение слишком мало!")
        # если ввели отрицательное количество
        if amount < 0:
            raise APIException(f"Нельзя конвертировать отрицательное количество валюты!")
        # ограничитель количества конвертируемой валюты
        if amount > 1000000000000:
            raise APIException(f"Введите значение поменьше, иначе Вы сломаете бота. :)")
        # если все проверки пройдены, то формируем запрос,
        # подставляя API-ключ, и введённые значения
        req = requests.get(f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair/"
                           f"{base_key}/{quote_key}/{amount}")
        # по формулам не будем считать - дёргаем результат конвертации напрямую
        # из результата нашего запроса по нужному ключу - conversion_result,
        # и округляем до 3 знака после точки, чтобы было читаемо
        result = round(json.loads(req.content)["conversion_result"], 3)
        # формируем строку-сообщение и возвращаем её как результат метода
        message = f"{amount} ед. в валюте {base} = {result} ед. в валюте {quote}."
        return message
