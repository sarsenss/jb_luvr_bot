import os

from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from django.http import HttpResponse

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=token)

updater = Updater(token)


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я Bot!')
    return HttpResponse()


def wake_up(update, context):
    chat = update.effective_chat
    print(update)
    name = update.message.chat.first_name
    context.bot.send_message(chat_id=chat.id,
                             text=f'Спасибо, что включили меня, {name}')


updater.dispatcher.add_handler(CommandHandler('start', wake_up))

updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
updater.start_polling()
# updater.idle()

