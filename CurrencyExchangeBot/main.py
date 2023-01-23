import telebot
import traceback

# импортируем наш бот-токен, класс API-исключений и метод расчёта значения конвертации
from CurrencyExchangeBot.config import TOKEN
from CurrencyExchangeBot.extensions import *


# инициализация бота на основе импортированного токена
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    """Обработчик сообщения команды /start."""
    text = "Приветствую Вас!\n\n" \
           "Введите команду /help чтобы увидеть инструкцию по использованию данного бота."
    bot.reply_to(message, text)


@bot.message_handler(commands=["help"])
def get_help(message: telebot.types.Message):
    """Обработчик сообщения команды /help."""
    text = 'Команда /values - просмотреть список доступных для конвертации валют '\
           'и их правильное написание.\n\n'\
           'Чтобы воспользоваться конвертором валют, введите сообщение в следующем формате:\n'\
           '<название исходной валюты>(пробел)<название конечной валюты>'\
           '(пробел)<количество исходной валюты>.\n\n'\
           'Чтобы бот работал корректно, используйте наименования валют из списка /values, '\
           'вне зависимости от количества.\n'\
           'Пример: "15 рубль" - верно, "15 рублей" - неверно.'
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    """Обработчик сообщения команды /values."""
    text = "Доступные валюты и их правильное написание для данного бота:\n"
    # с помощью цикла выдаём список
    for key in currencies.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def exchange(message: telebot.types.Message):
    """Обработчик сообщения по шаблону команды запроса конвертации."""
    # делим сообщение на раздельные строки
    data = message.text.split()
    try:
        # и если этих строк не 3
        if len(data) != 3:
            # то сабж
            raise APIException("Неверное количество параметров!")
        # но если их 3, то они становятся аргументами для нашего статического метода get_price
        answer = Converter.get_price(*data)
        # отлавливаем наши и не наши исключения и выводим их пользователю
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        # и если всё ок, отправляем ответ пользователю в виде сообщения
        bot.reply_to(message, answer)


bot.polling()
