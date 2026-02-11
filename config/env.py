import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

BOT_TOKEN = os.environ["BOT_TOKEN"]
STABLE_DIFFUSION_URL = os.environ["STABLE_DIFFUSION_URL"]
DB_URI = os.environ["DB_URI"]
