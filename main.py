from email.quoprimime import quote
import telebot
from config import keys, TOKEN
from extensions import ConvertionException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"Добро пожаловать в бот-конвертер валют!\n\nЧтобы начать работу введите команду боту в следующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количестко переводимой валюты>\n\nУидеть список всех доступных валют по команде: /values")


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Слишком много параметров.')

        base, quote, amount = values
        price = CryptoConverter.get_price(base, quote, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {price}'
        bot.send_message(message.chat.id, text)


def main():
    print('Bot started...')
    bot.polling(none_stop=True)


if __name__ == "__main__":
    main()
