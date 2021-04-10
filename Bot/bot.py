import telebot
import config
from telebot import types
from Parser.shops import find
from Parser.Promocodes import get_content
from Parser.categories import get_categories, get_category_shops

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    categories = get_categories()
    markup = types.InlineKeyboardMarkup()
    pair = []
    for cat in categories:
        category = types.InlineKeyboardButton(cat['name'], callback_data=cat['href'])
        pair.append(category)
        if len(pair) == 2:
            markup.add(pair[0], pair[1])
            pair.clear()
    if len(pair) != 0:
        markup.add(pair[0])

    msg = bot.send_message(message.chat.id,
                           'Приветствую. Напишите название магазина или выберите категорию.', reply_markup=markup)
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
                           'Наиболее подходящие по вашему запросу магазины. Выберите один или введите другое название.',
                           reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data.find('category') != -1)
def category_shops(call):
    shops = get_category_shops(call.data)
    markup = types.InlineKeyboardMarkup()
    triple = []
    for shop in shops:
        btn = types.InlineKeyboardButton(shop['name'], callback_data=shop['href'])
        triple.append(btn)
        if len(triple) == 3:
            markup.add(triple[0], triple[1], triple[2])
            triple.clear()
    if len(triple) == 2:
        markup.add(triple[0], triple[1])
    elif len(triple) == 1:
        markup.add(triple[0])
    msg = bot.send_message(call.message.chat.id,
                           'Магазины по выбранной категории:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: not call.data.isnumeric())
def choose(call):
    global promos
    promos = (get_content(call.data))
    markup = types.InlineKeyboardMarkup()
    for i in promos:
        if type(i) == str:
            break
        code = types.InlineKeyboardButton('🎁' + i['title'], callback_data=str(promos.index(i)))
        markup.add(code)
    msg = bot.send_message(call.message.chat.id,
                           'Промокоды по выбранному магазину:',
                           reply_markup=markup)
    bot.send_message(call.message.chat.id, 'Жмите на любой👆')


@bot.callback_query_handler(func=lambda call: call.data.isnumeric())
def show(call):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти в магазин", url=promos[int(call.data)]['link'])
    keyboard.add(url_button)
    bot.send_message(call.message.chat.id,
                     promos[int(call.data)]['description'])
    if promos[int(call.data)]['promo'] != '':
        bot.send_message(call.message.chat.id,
                         '✅Промокод: ' + promos[int(call.data)]['promo'], reply_markup=keyboard)
    else:
        bot.send_message(call.message.chat.id,
                         '✅Промокод не требуется. Прочтите условия акции и перейдите на сайт магазина.',
                         reply_markup=keyboard)
    bot.send_message(call.message.chat.id, 'Введите новый магазин или выберите другой промокод')


bot.polling(none_stop=True, interval=0)
