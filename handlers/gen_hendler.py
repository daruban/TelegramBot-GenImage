from telebot.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from core import bot
import base64
from models.Chat import Chat
from models.Base import session
from datetime import datetime
from handlers.gen_request import request
from models.Progressmonitor import ProgressMonitor
from config.env import STABLE_DIFFUSION_URL
import json
import threading


def gen_hendler(message_chat_id, message_text):
    if Chat.get(message_chat_id):
        command_text = message_text.replace('/gen', '')
        
        status_message = bot.send_message(message_chat_id, "Начало генерации...", parse_mode="html")
        chat = Chat.get(message_chat_id)
        payload = chat.chat_data.copy() if chat.chat_data else {}
        payload['prompt'] = command_text
        
        # Запускаем мониторинг прогресса
        monitor = ProgressMonitor(
            bot, 
            message_chat_id, 
            status_message.message_id,
            payload.get('sd_url', STABLE_DIFFUSION_URL)
        )
        
        monitor_thread = threading.Thread(
            target=monitor.monitor_progress_sync,
            args=(payload.get('steps', 20),),
            daemon=True
        )
        monitor_thread.start()
        
        try:
            otvet = request(payload)
            if otvet and 'images' in otvet:
                markup = InlineKeyboardMarkup()
                Button = InlineKeyboardButton("Повторить", callback_data=f"gen_")
                markup.row(Button)
                bot.send_photo(
                    message_chat_id,
                    base64.b64decode(otvet['images'][0].split(',')[-1]),
                    caption = f"{command_text[:200]}\nSeed: {json.loads(otvet['info'])['seed']}",
                    reply_markup = markup,
                )
                
                bot.edit_message_text(
                    f"Генерация завершена!\n",
                    message_chat_id,
                    status_message.message_id
                )
        except Exception as e:
            bot.edit_message_text(
                f"Ошибка: {str(e)}",
                message_chat_id,
                status_message.message_id
            )
        finally:
            monitor.stop()
