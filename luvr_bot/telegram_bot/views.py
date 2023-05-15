import os

from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from django.http import HttpResponse


load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=token)

updater = Updater(token)


def say_hi(update, context):
    # if chat_id not in employees - send keyboard with request contact button and exit
    print(update)
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text='Привет, я Bot!')
    return HttpResponse()


def wake_up(update, context):
    chat = update.effective_chat
    print(update)
    name = update.message.chat.first_name
    print(update.message)
    phone_button = KeyboardButton(text='Присоединиться', request_contact=True)
    start_shift_button = KeyboardButton(text='Начать смену')
    end_shift_button = KeyboardButton(text='Закончить смену')
    send_location_button = KeyboardButton(text='Отправить координаты', request_location=True)
    context.bot.send_message(chat_id=chat.id,
                             text=f'Спасибо, что включили меня, {name}', reply_markup=ReplyKeyboardMarkup(
            [
                [phone_button],
                [start_shift_button, end_shift_button],
                [send_location_button]
            ]
        )
                             )





updater.dispatcher.add_handler(CommandHandler('start', wake_up))

updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
updater.dispatcher.add_handler(MessageHandler(Filters.contact, say_hi))
updater.dispatcher.add_handler(MessageHandler(Filters.location, say_hi))
updater.start_polling()
# updater.idle()

