"""
    Команды бота:
        /start              - начало работы с ботом
        /subscribe          - подписка на ежедневную рассылку
        /unsubscribe        - отписка от ежедневной рассылки
        /help               - помощь и основные команды бота
        /help_me            - форма отправки сообщений разработчику

    Команда только для "админов" (настройки в config.py):
        /send_message       - отправка сообщения от разработчика к пользователю
"""
from random import choice
from time import sleep
from traceback import print_exc

import schedule
from pyowm.commons.exceptions import NotFoundError
from telebot import TeleBot, types
from telebot.apihelper import ApiTelegramException
from telebot.util import async_dec

import config
import helper
from sqlighter import SQLighter
from strings import strings

bot = TeleBot(config.TOKEN_TG)  # Токен Telegram
db = SQLighter(config.name_db)  # Инициализация БД


@bot.message_handler(commands=["start"])
def start_cmd(message): bot.send_message(message.chat.id, strings["start"], reply_markup=helper.keyboard())


@bot.message_handler(commands=["subscribe"])
def sub_weather(message):
    bot.send_message(message.chat.id, strings["subscribe"])
    bot.register_next_step_handler(message, reg_weather)


def reg_weather(message):
    """Подтверждение подписки"""
    if message.text == "/cancel":
        return bot.send_message(message.chat.id, strings["cancel"])
    try:
        helper.get_weather(message.text, "now")
        db.upd_subs(message.chat.id, message.text, True)
        bot.send_message(message.chat.id, strings["success"], reply_markup=helper.keyboard())
    except NotFoundError:
        bot.send_message(message.chat.id, strings["not_found"])
        bot.register_next_step_handler(message, reg_weather)


@bot.message_handler(commands=["unsubscribe"])
def unsubscribe(message: types.Message):
    if not db.check_subs(message.chat.id):
        bot.send_message(message.chat.id, strings["not_active"], reply_markup=helper.keyboard())
    else:
        db.upd_subs(message.chat.id, status=False)
        bot.send_message(message.chat.id, strings["unsubscribe"], reply_markup=helper.keyboard())


@bot.message_handler(commands=["help"])
def helping(message):
    bot.send_message(message.chat.id, strings["help"])


@bot.message_handler(commands=["help_me"])
def help_me(message):
    """Отправка сообщений от пользователей"""
    bot.send_message(message.chat.id, strings["help_me"])
    bot.register_next_step_handler(message, send_help)


def send_help(message):
    if message.text == "/cancel":
        bot.send_message(message.chat.id, strings["not_ask"])
    else:
        bot.send_message(config.admins[0], "НОВОЕ СООБЩЕНИЕ:\n"
                                           f"{message.chat.first_name} {message.chat.last_name}\n"
                                           f"Username: @{message.chat.username}\n"
                                           f"id: '{message.chat.id}'\n\n"
                                           f"Текст: {message.text}")
        bot.send_message(message.chat.id, "Сообщение отправлено!")


@bot.message_handler(commands=["send_message"])
def set_id_text(message):
    """Ответ на сообщение через бота"""
    if helper.is_admin(message.chat.id):
        bot.send_message(message.chat.id, "Введите id и текст через ```##```", parse_mode="Markdown")
        bot.register_next_step_handler(message, sending)
    else:
        text_cmd(message)


def sending(message):
    try:
        msg = message.text.split("##")
        id_user = int(msg[0])
        text = msg[1]
        bot.send_message(id_user, text, parse_mode="Markdown")
        bot.send_message(message.chat.id, "Сообщение отправлено!")
    except ValueError:
        bot.send_message(message.chat.id, "Неправильный id!")
    except ApiTelegramException as e:
        bot.send_message(message.chat.id, f"Код ошибки: {e.error_code}\n"
                                          f"{e.result_json['description']}")


@bot.message_handler(content_types=["text"])
def text_cmd(message):
    """Определение команд с клавиатуры и перехват всех сообщений"""
    if message.text == strings["now"]:
        bot.send_message(message.chat.id, strings["weather"], reply_markup=helper.keyboard())
        bot.register_next_step_handler(message, search_weather, "now")
    elif message.text == strings["daily"]:
        bot.send_message(message.chat.id, strings["weather"], reply_markup=helper.keyboard())
        bot.register_next_step_handler(message, search_weather, "daily")
    elif message.text == strings["mail"]:
        bot.send_message(message.chat.id, strings["mail_send"])
    elif message.text[0] == "/":
        bot.send_message(message.chat.id, strings["not_cmd"], reply_markup=helper.keyboard())
    else:
        default(message)


@bot.message_handler(
    content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"])
def default(message): bot.send_message(message.chat.id, strings["understand"], reply_markup=helper.keyboard())


@async_dec()
def mailing():
    """Автоматическая рассылка погоды"""
    print("Рассылка запущенна!")

    schedule.every().day.at("08:00").do(sending_weather, time_city="now")
    schedule.every().day.at("14:00").do(sending_weather, time_city="now")
    schedule.every().day.at("20:00").do(sending_weather, time_city="daily")

    while True:
        try:
            schedule.run_pending()
            sleep(10)
        except Exception as e:
            print(e)
            print_exc()


def search_weather(message, time_city=None):
    if message.text == "/cancel":
        return bot.send_message(message.chat.id, strings["cancel"])
    try:
        text = "Погода на завтра:\n" if time_city == "daily" else ""
        text1 = helper.get_weather(message.text, time_city)
        text += text1
        bot.reply_to(message, text)
    except NotFoundError:
        bot.send_message(message.chat.id, strings["not_found"])
        bot.register_next_step_handler(message, search_weather, time_city)


def sending_weather(time_city):
    subs_user = db.get_subs()
    for i in range(0, len(subs_user)):
        user_id = subs_user[i][1]
        user_city = subs_user[i][2].capitalize()

        text = helper.get_weather(user_city, time_city)
        text0 = "Погода на завтра" if time_city == "daily" else "Сейчас"
        text = text0 + f" в городе {user_city}:\n" + text

        try:
            bot.send_sticker(user_id, choice(config.bot_stickers))
            bot.send_message(user_id, text)
        except ApiTelegramException:
            print(f"Id: {user_id} не отписался от рассылки!")
        sleep(1)


if __name__ == "__main__":
    mailing()
    while True:
        try:
            print("Бот работает!")
            bot.polling(none_stop=True)
        except Exception as error:
            print(error)
            print_exc()
            print("Бот перезагружается...")
            sleep(15)
