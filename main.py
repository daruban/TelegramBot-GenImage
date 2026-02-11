from telebot.types import *
from core import bot

if __name__ == "__main__":
    from handlers import *
    from models import *

    bot.polling(
        none_stop=True,
        interval=0,
        timeout=25,
        long_polling_timeout=30,
        skip_pending=False,
    )
