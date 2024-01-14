import telebot
import datetime
import configparser
import json
import os
import time

def save_data():
    with open(f'{dir_path}/data.json', 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_data():
    global data
    if not os.path.exists(f'{dir_path}/data.json'):
        data = {"w": []}
        save_data()
    else:
        with open(f'{dir_path}/data.json', 'r') as f:
            data = json.load(f)

def find_coming_date(day_of_week):
    today = datetime.datetime.now()
    days_ahead = day_of_week - today.isoweekday()
    if days_ahead < 0:
        days_ahead += 7
    return today + datetime.timedelta(days_ahead)

def check_past_date(date):
    date = date + " 23:59:59"
    date = datetime.datetime.strptime(date, '%d.%m.%Y %H:%M:%S')    
    today = datetime.datetime.now()
    
    if date < today:
        return False
    else:
        return True

dir_path = (os.path.dirname(__file__))
print("Started at: ", dir_path)
config = configparser.ConfigParser()
config.read(f'{dir_path}/settings.ini')

allowed_users = list(map(int, config['General']['allowed_users'].split(',')))
bot = telebot.TeleBot(config['General']['token'])

load_data()

@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.id in allowed_users:
        bot.send_message(message.chat.id, 'Привет, создатель!')

@bot.message_handler(commands=['add'])
def add_once(message):
    if message.from_user.id in allowed_users:
        comm = message.text.split()
        if len(comm) >= 3 and comm[1] == "w":
            data[comm[1]].append(" ".join(comm[2:]))
            bot.send_message(message.chat.id, 'Добавлено!')
            save_data()
        elif len(comm) >= 3:
            if comm[1] in data:
                data[comm[1]].append(" ".join(comm[2:]))
            else:
                data[comm[1]] = [" ".join(comm[2:])]
            bot.send_message(message.chat.id, 'Добавлено!')
            save_data()
        else:
            bot.send_message(message.chat.id, 'Введите команду в формате /add ДД.ММ.ГГГГ Событие')

@bot.message_handler(commands=['show'])
def show_once(message):
    if message.from_user.id in allowed_users:
        bot.send_message(message.chat.id, 'Все события:')
        msglist = []
        for key in data:
            if key[0].isdigit() and check_past_date(key[:10]):
                mess = f'{key} - {", ".join(data[key])}'
                msglist.append(mess)
            elif key[0] == 'w':
                for weekday in data[key]:
                    mess = find_coming_date(int(weekday[0])).strftime('%d.%m.%Y') + " - " + weekday[2:]
                    msglist.append(mess)
        msglist.sort()
        bot.send_message (message.chat.id, "\n".join(msglist))


@bot.message_handler(commands=['start_everyday'])
def start_everyday(message):
    if message.from_user.id in allowed_users:
        bot.send_message(message.chat.id, 'Напоминание включено')
        while True:
            now = datetime.datetime.now()
            print (now.hour, now.minute)
            if now.hour == 4:
                show_once(message)
            time.sleep(3600)


bot.polling(none_stop=True)