import telebot
import config
from telebot import types
from Parser.shops import find, get_link
from Parser.Promocodes import get_content, get_promo

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    msg = bot.send_message(message.chat.id,
                           'Приветствую. Напиши название магазина, а я скину актуальные промокоды для него.')
    bot.register_next_step_handler(msg, shop_choosing)


@bot.message_handler(content_types=['text'])
def shop_choosing(message):
    shop = message.text.strip().lower()
    result = find(shop)
    markup = types.InlineKeyboardMarkup()
    shop1 = types.InlineKeyboardButton(result[0][0]['name'], callback_data=result[0][0]['href'])
    markup.add(shop1)
    shop2 = types.InlineKeyboardButton(result[1][0]['name'], callback_data=result[1][0]['href'])
    markup.add(shop2)
    shop3 = types.InlineKeyboardButton(result[2][0]['name'], callback_data=result[2][0]['href'])
    markup.add(shop3)
    msg = bot.send_message(message.chat.id,
                           'Наиболее подходящие по вашему запросу магазины. Выберите один.',
                           reply_markup=markup)


@bot.callback_query_handler(func=lambda call: not call.data.isnumeric())
def choose(call):
    global PROMOS
    PROMOS = (get_content(get_link(call.data)))
    markup = types.InlineKeyboardMarkup()
    for i in PROMOS:
        if type(i) == str:
            break
        code = types.InlineKeyboardButton('🎁' + i['title'], callback_data=str(PROMOS.index(i)))
        markup.add(code)
    msg = bot.send_message(call.message.chat.id,
                           'Промокоды по выбранному магазину:',
                           reply_markup=markup)
    bot.send_message(call.message.chat.id, 'Тыкай на любой👆')


@bot.callback_query_handler(func=lambda call: call.data.isnumeric())
def show(call):
    bot.send_message(call.message.chat.id, 'Секунду...')
    result = get_promo(PROMOS[int(call.data)]['title'], PROMOS[-1])
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти в магазин", url=result[2])
    keyboard.add(url_button)
    bot.send_message(call.message.chat.id,
                     result[1])
    bot.send_message(call.message.chat.id,
                     '✅Промокод: ' + result[0], reply_markup=keyboard)
    bot.send_message(call.message.chat.id, 'Введи новый магазин или выбери другой промокод')


bot.polling(none_stop=True, interval=0)
