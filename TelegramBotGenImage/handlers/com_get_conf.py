from TelegramBotGenImage import bot
from TelegramBotGenImage.models.Chat import Chat

@bot.message_handler(commands=["get_conf"], chat_types=["group"])
def get_conf(message):
    chat = Chat.get(message.chat.id)
    if chat is not None:
        text_mes = f"{chat.chat_data}"
    else:
        text_mes = f"Группа не авторизирована"        
    bot.send_message(
        message.chat.id,
        text_mes,
        parse_mode="html",
    )
