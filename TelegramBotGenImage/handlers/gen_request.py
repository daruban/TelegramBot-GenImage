import requests
import json
from TelegramBotGenImage.config.env import STABLE_DIFFUSION_URL

def gen_request(payload):
    """Запрос к сервису для генерации"""
    url = STABLE_DIFFUSION_URL
    headers = {
        'Content-Type': 'application/json'
        }
    response = requests.request("POST", url + '/sdapi/v1/txt2img', headers=headers, data=json.dumps(payload))

    return response.json()