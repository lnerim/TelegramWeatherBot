from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from telebot import types

import config
from strings import strings

config_dict = get_default_config()        # Config pyowm по умолчанию
config_dict["language"] = "ru"            # Русский язык в pyowm
owm = OWM(config.TOKEN_OWM, config_dict)  # Токен погоды


def is_admin(id_adm) -> bool: return id_adm in config.admins


def deg_weather(deg) -> str:
    return {
        (337.5 <= deg < 360) or (0 <= deg < 22.5): "Сев.",
        22.5 <= deg < 67.5: "СВ",
        67.5 <= deg < 112.5: "Вост.",
        112.5 <= deg < 157.5: "ЮВ",
        157.5 <= deg < 202.5: "Юж.",
        202.5 <= deg < 247.5: "ЮЗ",
        247.5 <= deg < 292.5: "Зап.",
        292.5 <= deg < 337.5: "СЗ"
    }[True]


def wind_warning(speed) -> str:
    return {
        speed >= 30: "\n🌪 Ураган!!!",
        30 > speed >= 18: "\n💨 На улице шторм!",
        18 > speed >= 10: "\n🌬 Сильный ветер, будьте аккуратны на улице.",
        speed < 10: ""  # Отсутствие предупреждения
    }[True]


def get_weather(city, times) -> str:
    mgr = owm.weather_manager()
    if times == "daily":
        daily_forecast = mgr.forecast_at_place(city, "daily")
        tomorrow = timestamps.tomorrow(14, 0)
        city_weather = daily_forecast.get_weather_at(tomorrow)
    else:
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
