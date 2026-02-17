from TelegramBotGenImage import bot
from TelegramBotGenImage.models.Chat import Chat
from TelegramBotGenImage.logging import LOGGER

@bot.message_handler(commands=["start"], chat_types=["group"])
def start(message):
    try:
        if Chat.get(message.chat.id):
            text_mes = f"Группа авторизирована"
        else:
            chat = Chat.create(chat_id=message.chat.id)
            text_mes = f"Группа зарегестрирована"
        
        bot.send_message(
            message.chat.id,
            text_mes,
            parse_mode="html",
        )
    except Exception as e:
        # Логируем ошибку
        LOGGER(__name__).error(f"Error in start handler for chat {message.chat.id}: {e}")

        # Отправляем пользователю понятное сообщение
        bot.send_message(
            message.chat.id,
            "Произошла ошибка. Попробуйте позже.",
            parse_mode="html",
        )