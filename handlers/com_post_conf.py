from core import bot
from models.Chat import Chat
import json

@bot.message_handler(commands=["post_conf"], chat_types=["group"])
def post_conf(message):
    try:
        chat = Chat.get(message.chat.id)
        command_text = json.loads(message.text.replace('/post_conf ', '').replace("'", '"'))
        if chat:
            chat.update_chat_data(message.chat.id, command_text)
            text_mes = f"{command_text}"
        else:
            text_mes = f"Группа не авторизирована"        
        bot.send_message(
            message.chat.id,
            text_mes,
            parse_mode="html",
        )
    except Exception as e:
        bot.send_message(
            message.chat.id,
            e,
            parse_mode="html",
        )
