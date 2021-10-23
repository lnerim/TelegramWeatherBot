from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from telebot import types

import config
from strings import strings

config_dict = get_default_config()        # Конфиг по умолчанию
config_dict["language"] = "ru"            # Русский язык в pyowm
owm = OWM(config.TOKEN_OWM, config_dict)  # Токен погоды


def is_admin(id_adm) -> bool: return id_adm in config.admins


def deg_weather(deg) -> str:
    if (337.5 <= deg < 360) or (0 <= deg < 22.5):
        return "Сев."
    elif 22.5 <= deg < 67.5:
        return "СВ"
    elif 67.5 <= deg < 112.5:
        return "Вост."
    elif 112.5 <= deg < 157.5:
        return "ЮВ"
    elif 157.5 <= deg < 202.5:
        return "Юж."
    elif 202.5 <= deg < 247.5:
        return "ЮЗ"
    elif 247.5 <= deg < 292.5:
        return "Зап."
    elif 292.5 <= deg < 337.5:
        return "СЗ"


def wind_warning(speed) -> str:
    if speed >= 30:
        return "\n**Ураган!!!**"
    elif speed >= 18:
        return "\n**На улице шторм!**"
    elif speed >= 10:
        return "\n**Сильный ветер, будьте аккуратны на улице.**"
    else:  # Пустота, т.к. она будет отображаться, когда ветра "нет"
        return ""


def get_weather(city, times) -> str:
    if times == "daily":
        mgr = owm.weather_manager()
        daily_forecast = mgr.forecast_at_place(city, "daily")
        tomorrow = timestamps.tomorrow(14, 0)
        city_weather = daily_forecast.get_weather_at(tomorrow)
    else:
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        city_weather = observation.weather

    temp = city_weather.temperature("celsius")[
        "day" if times == "daily" else "temp"]           # Температура
    speed = city_weather.wind()["speed"]                 # Скорость ветра
    dict_wind = deg_weather(city_weather.wind()["deg"])  # Направление ветра
    hum = city_weather.humidity                          # Влажность воздуха

    return f"Температура воздуха: {temp}°C\n"\
           f"Скорость ветра: {speed} м/с, {dict_wind}{wind_warning(speed)}\n"\
           f"Отн. влажность воздуха: {hum}%\n"\
           f"{city_weather.detailed_status.capitalize()}"


def keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    # Кнопки для клавиатуры
    button1 = types.KeyboardButton(strings["now"])
    button2 = types.KeyboardButton(strings["daily"])
    button3 = types.KeyboardButton(strings["mail"])

    # Добавление кнопок в клавиатуру
    markup.row(button1, button2)
    markup.row(button3)
    return markup
