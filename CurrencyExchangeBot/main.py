import telebot
import traceback

from CurrencyExchangeBot.config import TOKEN
from CurrencyExchangeBot.extensions import *


# инициализация бота на основе импортированного токена
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    text = "Приветствую Вас!\n\n" \
           "Введите команду /help чтобы увидеть инструкцию по использованию данного бота."
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=["help"])
def get_help(message: telebot.types.Message):
    text = "Команда /values - просмотреть список доступных для конвертации валют" \
           "и их правильное написание.\n\n" \
           "Чтобы воспользоваться конвертором валют, введите сообщение в следующем формате:\n\n" \
           "<название исходной валюты>(пробел)<название конечной валюты>" \
           "(пробел)<количество исходной валюты>."
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Доступные валюты:\n"
    for key in currencies.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def exchange(message: telebot.types.Message):
    data = message.text.split(" ")
    try:
        if len(data) != 3:
            raise APIException("Неверное количество параметров!")
        answer = Converter.get_price(*data)
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")
    except Exception as e:
        traceback.print_tb(e.__traceback__)
        bot.reply_to(message, f"Неизвестная ошибка:\n{e}")
    else:
        bot.reply_to(message, answer)


bot.polling()
