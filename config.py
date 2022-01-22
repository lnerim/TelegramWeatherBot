import os
from dotenv import load_dotenv

load_dotenv()

# Токен бота Telrgram
TOKEN_TG = os.getenv("TG")

# Токен OWM, поддерживающий погоду на завтра
TOKEN_OWM = os.getenv("OWM")

# Имя БД, любое
name_db = "bot.sqlite3"

# Минимум один админ должен быть, чтобы не нарушать некоторые функции бота.
# Кортеж из числового идентификатора аккаунта админа
admins = (int(os.getenv("adm0")), int(os.getenv("adm1")))

# Идентификаторы стикеров, можно добавлять/удалять
bot_stickers = (
    "CAACAgIAAxkBAAINuWBrn9JiVKMTSepQhXyfZkNuxnCcAAJoAwACY4tGDHdH19XAzMD2HgQ",
    "CAACAgIAAxkBAAINu2BroBJml26Ab6TCLzRtzjI17QJ_AAJjAwACY4tGDFHvJYA2j_i8HgQ",
    "CAACAgIAAxkBAAINvWBroBrxdzHQQVNp92eRhxjhNlfpAAJkAwACY4tGDNHVOZJmnnCpHgQ",
    "CAACAgIAAxkBAAINv2BroBy42DrwcGiqZsXPGxV-OjjaAAJlAwACY4tGDBdNJzrs2bkEHgQ",
    "CAACAgIAAxkBAAINwWBroCF9BJyClBP8MpKc9G7HXqMPAAJqAwACY4tGDAl_1e-6dDtgHgQ",
    "CAACAgIAAxkBAAINw2BroCUMnv16cbIjKpdOSK2QE2RKAAJsAwACY4tGDHI0_pE916yVHgQ",
    "CAACAgIAAxkBAAINxWBroCbI2C1gKZNMqBmr4aX-jhH-AAJtAwACY4tGDPHRtLKN_YjtHgQ",
    "CAACAgIAAxkBAAINx2BroCdn26Jspn0R645jp8f86fjVAAJuAwACY4tGDLD1j7A1OSIbHgQ",
    "CAACAgIAAxkBAAINyWBroCm7tifdsI6mBapaTjHDnrhzAAJyAwACY4tGDJQZpBeWKkmaHgQ",
    "CAACAgIAAxkBAAINy2BroCsORuO4SfgtLAcBqqysolveAAJvAwACY4tGDEzd-H3zLxZ1HgQ",
    "CAACAgIAAxkBAAINzWBroDHYba_j0ng0UjjyofYwZQABAwACdQMAAmOLRgzyyWy2Er_T4B4E",
    "CAACAgIAAxkBAAINz2BroD1kQE_WfAsKODnf8F0oKOupAAJ0AwACY4tGDO0GMo_VU74aHgQ"
)
