import telebot
from config import ru_c_dict, ru_greeting_mess, ru_help_mess,ru_err_mess, TOKEN
from extensions import Converter, UserException
bot = telebot.TeleBot(TOKEN)
greet_flag = False
err_message = ''


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    global greet_flag
    text = message.from_user.first_name
    if greet_flag:
        text = text + ru_greeting_mess[1]
    else:
        text = text + ru_greeting_mess[0] + '\n' + ru_help_mess[0] + ru_help_mess[1]
        greet_flag = True
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help_comm(message: telebot.types.Message):
    text = ru_help_mess[0] + ru_help_mess[1]
    bot.reply_to(message, text)


@bot.message_handler(commands=['available'])
def available(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in ru_c_dict:
        text = text + '\n' + key[0].upper() + key[1:] + ru_c_dict[key][1] + ' (' + ru_c_dict[key][0] + ')'
    bot.reply_to(message, text)


@bot.message_handler(commands=['mem'])
def mem(message: telebot.types.Message):
    text = Converter.convert(message.text)
    bot.send_message(message.chat.id, text)
    

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    text = Converter.convert(message.text)
    bot.send_message(message.chat.id, text)


bot.polling(non_stop=False)
