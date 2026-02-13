from core import bot
from handlers.gen_hendler import gen_hendler

@bot.callback_query_handler(func=lambda call: call.data.startswith('gen_'))
def ch_gen(call):
    gen_hendler(call.json['message']['chat']['id'], call.message.caption.split('\n')[0])