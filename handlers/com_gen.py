from core import bot
import base64
from models.Chat import Chat
from models.Base import session
from datetime import datetime
from handlers.gen_request import request
from models.Progressmonitor import ProgressMonitor
from config.env import STABLE_DIFFUSION_URL
import threading



@bot.message_handler(commands=["gen"], chat_types=["group"])
def start_simple(message):
    if Chat.get(message.chat.id):
        command_text = message.text.replace('/gen', '')
        
        status_message = bot.reply_to(message, "Начало генерации...")
        
        chat = Chat.get(message.chat.id)
        payload = chat.chat_data.copy() if chat.chat_data else {}
        payload['prompt'] = command_text
        
        # Запускаем мониторинг прогресса
        monitor = ProgressMonitor(
            bot, 
            message.chat.id, 
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
                bot.send_photo(
                    message.chat.id,
                    base64.b64decode(otvet['images'][0].split(',')[-1]),
                    caption=f"{command_text[:200]}"
                )
                
                bot.edit_message_text(
                    f"Генерация завершена!\n{otvet['info']}",
                    message.chat.id,
                    status_message.message_id
                )
        except Exception as e:
            bot.edit_message_text(
                f"Ошибка: {str(e)}",
                message.chat.id,
                status_message.message_id
            )
        finally:
            monitor.stop()
