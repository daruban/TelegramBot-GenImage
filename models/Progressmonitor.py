import asyncio
import aiohttp
import threading
import time
import requests

class ProgressMonitor:
    def __init__(self, bot, chat_id, message_id, sd_url):
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = message_id
        self.sd_url = sd_url
        self.start_time = time.time()
        self.is_active = True
    
    def stop(self):
        self.is_active = False

    def monitor_progress_sync(self, total_steps=20):
        
        
        last_step = 0
        while self.is_active:
            try:
                response = requests.get(f"{self.sd_url}/sdapi/v1/progress", timeout=2)
                
                if response.status_code == 200:
                    data = response.json()
                    progress = data.get('progress', 0) * 100
                    current_step = data['state'].get('sampling_step', 0)
                    if current_step > last_step:
                        elapsed = time.time() - self.start_time
                        it_per_sec = current_step / elapsed if elapsed > 0 else 0
                        
                        filled = int(current_step / total_steps * 20)
                        bar = '█' * filled + '░' * (20 - filled)
                        
                        status_text = (
                            f"Генерация... {progress:.1f}%\n"
                            f"┗ {bar}\n"
                            f"   {current_step}/{total_steps} шагов | {it_per_sec:.1f} шаг/с"
                        )
                        
                        try:
                            self.bot.edit_message_text(
                                status_text,
                                self.chat_id,
                                self.message_id
                            )
                        except:
                            print('ERROR')
                        
                        last_step = current_step
                    
                    if progress >= 99.9 or current_step >= total_steps:
                        break
                        
            except Exception as e:
                print('ERROR')
            time.sleep(0.5)