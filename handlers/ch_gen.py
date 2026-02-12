from core import bot
import base64
from models.Chat import Chat
from models.Base import session
from datetime import datetime
from handlers.gen_request import request
from handlers.gen_hendler import gen_hendler
from models.Progressmonitor import ProgressMonitor
from config.env import STABLE_DIFFUSION_URL
import json
import threading



@bot.callback_query_handler(func=lambda call: call.data.startswith('gen_'))
def ch_gen(call):
    gen_hendler(call.json['message']['chat']['id'], call.message.caption.split('\n')[0])