import telebot,pyowm,requests
from telebot import types
temp = ''
bot = telebot.TeleBot('ваш токен')
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    print(message.text + ' от ' + str(message.from_user.id))
    if message.text.lower() == '/start':
        bot.send_message(message.chat.id, 'Привет, чтобы продожить, напиши "Погода"')
    if message.text.lower() == 'погода':
        bot.send_message(message.chat.id, 'Введи свой город:')
        bot.register_next_step_handler(message, get_ass)
def get_ass(message):
    global temp
    g = message.text
    temp = g
    ow = pyowm.OWM('ваш токен')
    try:
        mrg = ow.weather_manager()
        observation = mrg.weather_at_place(g)
        w = observation.weather
        temperature = w.temperature('celsius')['temp']
        weter = w.wind()['speed']
        gg = w.pressure['press']
        wete = w.wind()['deg']
        print(wete)
        davl = int(gg) - 11
        rtst = str(davl/1.333)
        gay = ''
        if int(wete) < 45:
            gay = 'Север'
        if int(wete) < 90:
            gay = 'Северо-восток'
        if int(wete) < 135:
            gay = 'Восток'
        if int(wete) < 180:
            gay = 'Юго-восток'
        if int(wete) < 225:
            gay = 'Юг'
        if int(wete) < 270:
            gay = 'Юго-запад'
        if int(wete) < 315:
            gay = 'Запад'
        if int(wete) < 360:
            gay = 'Северо-запад'
        print("В городе " + g + " сейчас " + str(temperature) + "°С")
        bot.send_message(message.chat.id, 'В городе ' + g + ' сейчас ' + str(temperature) + '°C')
        bot.send_message(message.chat.id, 'Скорость ветра: ' + str(weter) + 'м/с, нпаравление ветра: ' + str(wete) + ' градусов = ' + gay)
        bot.send_message(message.chat.id, 'Давление: ' + str(davl) + ' миллибар = ' + str(rtst[:-14]) + ' мм.рт.ст')
    except Exception as e:
        print(e)
        bot.send_message(message.chat.id, 'Город не найден')
    keyboard = types.InlineKeyboardMarkup() #наша клавиатура
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no= types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    bot.send_message(message.chat.id, text='Еще раз?', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes": #call.data это callback_data, которую мы указали при объявлении кнопки
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'Хорошо, введи город (прошедшее было: '+ str(temp) + ')')
        bot.register_next_step_handler(call.message, get_ass)
    elif call.data == "no":
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, 'Ок.')
bot.polling(none_stop=True)
