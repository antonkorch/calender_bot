# Description: This is the main file that will be used 
from sqlalchemy import create_engine
from db_commands import add_event, list_events_from
import telebot
import configparser
import os
from datetime import datetime

dir_path = (os.path.dirname(__file__))
print("Started at: ", dir_path)

config = configparser.ConfigParser()
config.read(f'{dir_path}/settings.ini')

engine = create_engine(f'sqlite:///{dir_path}/calender.db')

allowed_users = list(map(int, config['General']['allowed_users'].split(',')))
bot = telebot.TeleBot(config['General']['token'])


@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in allowed_users:
        bot.send_message(message.chat.id, 'Привет, создатель!')


@bot.message_handler(commands=['show'])
def show_once(message):
    if message.from_user.id in allowed_users:
        msglist = []
        events = list_events_from(engine, '2024-04-04')
        for event in events:
            date = datetime.strptime(event[0], '%Y-%m-%d')
            time = event[1]
            text = event[2]
            day_of_week = date.strftime('%A')
            date = date.strftime('%d.%m')
            mess = f'{day_of_week}, {date}, {time}, {text}'
            msglist.append(mess)
        bot.send_message(message.chat.id, "\n".join(msglist))


@bot.message_handler(commands=['add'])
def add_once(message):
    if message.from_user.id in allowed_users:
        comm = message.text.split()
        errormsg = 'Введите команду в формате /add ДД.ММ ЧЧ:ММ Событие'
        if len(comm) >= 3:
            try:
                date = datetime.strptime(comm[1], '%d.%m')
                current_year = datetime.now().year
                date = date.strftime(f'{current_year}-%m-%d')
                time = datetime.strptime(comm[2], '%H:%M')
                time = time.strftime('%H:%M')
                text = " ".join(comm[3:])
                add_event(engine, None, date, time, text)
                bot.send_message(message.chat.id, 'Добавлено!')
            except ValueError:
                bot.send_message(message.chat.id, errormsg)
        else:
            bot.send_message(message.chat.id, errormsg)


@bot.message_handler(commands=['add_regular'])
def add_regular(message):
    if message.from_user.id in allowed_users:
        comm = message.text.split()
        errormsg = 'Введите команду в формате /add_regular День_недели ЧЧ:ММ Событие'
        if len(comm) >= 3:
            try:
                dow = comm[1]
                time = datetime.strptime(comm[2], '%H:%M')
                time = time.strftime('%H:%M')
                text = " ".join(comm[3:])
                add_event(engine, dow, None, time, text)
                bot.send_message(message.chat.id, 'Добавлено!')
            except ValueError:
                bot.send_message(message.chat.id, errormsg)
        else:
            bot.send_message(message.chat.id, errormsg)
    


bot.polling(none_stop=True)

