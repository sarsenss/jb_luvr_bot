import os

from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv
from django.http import HttpResponse

from .models import Employee

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=token)

updater = Updater(token)


def main_func(update, context):
    chat = update.effective_chat
    if not Employee.objects.filter(chat_id=chat.id):
        phone_button = KeyboardButton(text='Отправить номер телефона', request_contact=True)
        context.bot.send_message(chat_id=chat.id,
                                 text=f'Пожалуйста, отправьте мне свой номер телефона для регистрации '
                                      f'(кнопка "Отправить номер телефона")',
                                 reply_markup=ReplyKeyboardMarkup([[phone_button]]))

    context.bot.send_message(chat_id=chat.id, text='Спасибо, что поделились номером телефона!\n'
                                                   'Для начала смены нажмите кнопку "Начать смену"')
    phone_number = update.message.contact.phone_number
    employee = Employee.objects.filter(chat_id=chat.id)
    employee.phone_number = phone_number
    location_button = KeyboardButton(text='Отправить координаты', request_location=True)
    context.bot.send_message(chat_id=chat.id,
                             text=f'Спасибо, мы записали ваши данные о начале смены.\n'
                                  f'Не забудьте завершить смену, нажав на кнопку "Закончить смену"',
                             reply_markup=ReplyKeyboardMarkup([[location_button]]))

    return HttpResponse()


def start(update, context):
    chat = update.effective_chat
    if not Employee.objects.filter(chat_id=chat.id):
        Employee.objects.create(chat_id=chat.id)
    name = update.message.chat.first_name
    phone_button = KeyboardButton(text='Отправить номер телефона', request_contact=True)
    # start_shift_button = KeyboardButton(text='Начать смену')
    # end_shift_button = KeyboardButton(text='Закончить смену')
    # send_location_button = KeyboardButton(text='Отправить координаты', request_location=True)
    context.bot.send_message(chat_id=chat.id,
                             text=f'Спасибо, что включили меня, {name}!\n'
                                  f'Пожалуйста, отправьте мне свой номер телефона для регистрации '
                                  f'(кнопка "Отправить номер телефона")', reply_markup=ReplyKeyboardMarkup([[phone_button]]))


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, main_func))
updater.dispatcher.add_handler(MessageHandler(Filters.contact, main_func))
updater.dispatcher.add_handler(MessageHandler(Filters.location, main_func))
updater.start_polling()
# updater.idle()

