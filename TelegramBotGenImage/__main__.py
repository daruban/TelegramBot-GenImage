from TelegramBotGenImage import bot
from TelegramBotGenImage.logging import LOGGER

LOGGER(__name__).info("client successfully initiated....")
if __name__ == "__main__":
    from TelegramBotGenImage.handlers import *
    from TelegramBotGenImage.models import *

    bot.infinity_polling(
        none_stop=True,
        interval=0,
        timeout=25,
        long_polling_timeout=30,
        skip_pending=False,
    )
