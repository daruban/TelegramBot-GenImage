from TelegramBotGenImage import bot
from TelegramBotGenImage.handlers.gen_hendler import gen_hendler

@bot.message_handler(commands=["gen"], chat_types=["group"])
def gen(message):
    gen_hendler(message.chat.id ,message.text)