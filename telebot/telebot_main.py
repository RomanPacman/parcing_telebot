import telebot
import schedule
import time
from datetime import datetime
from parcer_api.parcer import get_flats
from parcer_api.settings import Realt_by
from threading import Thread

now = datetime.now()
current_time = now.strftime("%H:%M")

bot_tg_chanel = 't.me/ParcerRealtBot'
token = '6262247707:AAFaqjCJd4m3V8LdxTUaFxCw4KZNhBTHcio'

bot = telebot.TeleBot(token)
id_chat = 412271538


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Привет {message.from_user.full_name}\n')


@bot.message_handler(commands=['parcing'])
def parcing(message):
    first_page = 0
    last_page = 3
    amount = get_flats(Realt_by.urls, first_page=first_page, last_page=last_page, only_new=False)[0]
    bot.send_message(message.chat.id,
                     f'{message.from_user.full_name}\n Парсинг {amount} квартир с {first_page} страницы по {last_page} произведен')
    return print('parce')


@bot.message_handler(commands=['check_new'])
def check_new(message):
    bot.send_message(message.chat.id, 'Это может занять какое-то время, подождите пожалуйста')
    flats = get_flats(Realt_by.urls, last_page=3)
    if flats[0] == 0:
        bot.send_message(message.chat.id, 'Нет новых квартир')
    else:
        bot.send_message(message.chat.id, f'{str(flats[0])} Новых квартир')
        for flat in flats[1]:
            bot.send_message(message.chat.id, str(flat.link))
    return print('message sent')


def check_new_await():
    flats = get_flats(Realt_by.urls, last_page=3)
    if flats[0] == 0:
        bot.send_message(id_chat, 'Нет новых квартир')
    else:
        bot.send_message(id_chat, f'{str(flats[0])} Новых квартир')
        for flat in flats[1]:
            bot.send_message(id_chat, str(flat.link))
    return print('message sent')


def do_schedule():
    schedule.every(60).minutes.do(check_new_await)

    while True:
        schedule.run_pending()
        time.sleep(600)


def main_loop():
    thread = Thread(target=do_schedule)

    thread.start()
    thread_1 = Thread(target=bot.polling(True))
    thread_1.start()


if __name__ == '__main__':
    main_loop()
