from core import bot
from models.Chats import Chat
from models.Base import session


@bot.message_handler(commands=["start"], chat_types=["group"])
def start(message):
    chat = session.get(Chat, 1)
    bot.send_message(
        message.chat.id,
        f"Группа зарегестрирована {chat}",
        parse_mode="html",
    )
