from core import bot
from models.Chat import Chat
from models.Base import session
from datetime import datetime

@bot.message_handler(commands=["start"], chat_types=["group"])
def start(message):
    if Chat.get(message.chat.id):
        text_mes = f"Группа авторизирована"
    else:
        chat = Chat.create(chat_id = message.chat.id)
        text_mes = f"Группа зарегестрирована"        
    print(Chat.get(message.chat.id).chat_data)
    bot.send_message(
        message.chat.id,
        text_mes,
        parse_mode="html",
    )
    bot.edit_message_text()
