from random import choice
import telebot
from telebot import types

token = '???' #вместо "???" вставить ключ телеграм бота 

bot = telebot.TeleBot(token)  #объявляю переменную bot для использования функций библиотеки telebot

todos = dict()

RANDOM_TASKS = [
    'Поспать',
    'Погулять',
    'Побренчать',
    'Пообедать',
    'Свернуться на тапках',
    'Помыть лапы',
    'Навести суету'
    ]

HELP = '''
/help - вывести список команд

/add - добавить задачу в список в формате "Дата Задача"

/print - вывести все задачи на конкретную дату

/random - добавляет случайную задачу из списка на дату "Сегодня"

'''

def add_todo(date, task):   #функция добавления задачи в словарь
    date = date.lower()
    if todos.get(date) is not None: #Дата уже есть в словаре, значит добавляем в список этой даты задачу
        todos[date].append(task)
    else:
        todos[date] = [task] #Даты в словаре нет, добавляем ключ-дату и к ней список с задачей

@bot.message_handler(commands=['start'])                 #/start
def start_message(message):
    bot.send_message(message.chat.id,"Салют!")

@bot.message_handler(commands=['help'])                  #/help
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=['random'])                #/random
def random(message):
    task = choice(RANDOM_TASKS)
    add_todo('сегодня', task)
    bot.send_message(message.chat.id, f'Задача {task} добавлена на сегодня')

@bot.message_handler(commands=['add'])                   #/add
def add(message):
    try:
        _, date, tail = message.text.split(maxsplit=2)
        task = ' '.join([tail])
        if len(task) < 3:
            bot.send_message(message.chat.id, 'Задачи должны быть больше 3х символов')
        else:
            add_todo(date, task)
            bot.send_message(message.chat.id, f'Задача {task} добавлена на дату {date}')
    except ValueError:
        bot.send_message(message.chat.id, f'Укажи Дату и Задачу после /add')

@bot.message_handler(commands=['print'])                #/print
def print_(message):
    try:
        dates = message.text.split(maxsplit=1)[1].lower().split()
    except IndexError:
        dates = ' '
    response  = ' '
    for date in dates:
        tasks = todos.get(date)
        response += f'{date}: \n'
        if tasks is not None:
            for task in tasks:
                response += f'[ ] {task}\n'
            response += '\n'
        else:
            response = 'Укажи Дату после /print'
    bot.send_message(message.chat.id, response)

@bot.message_handler(content_types=["text"])
def echo(message):
    if message.text.lower() == 'превед':
        bot.send_message(message.chat.id, "превед, медвед!")
    else:
        bot.send_message(message.chat.id, message.text)


@bot.message_handler(commands=['button'])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Кнопка")
    markup.add(item1)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)


#поллинг бота
bot.polling(none_stop=True, interval=2)  