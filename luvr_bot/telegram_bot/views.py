import datetime
import os

from telegram import Bot, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from dotenv import load_dotenv

from .models import Employee, JobRequestAssignment, EmployeeGeoPosition
from geopy.distance import geodesic as GD
from django.db.models import Q

load_dotenv()

token = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=token)

updater = Updater(token)


def main_func(update, context):
    chat = update.effective_chat
    has_contact_in_message = hasattr(update, 'message') and hasattr(update.message, 'contact') and hasattr(update.message.contact, 'phone_number')
    if not Employee.objects.filter(chat_id=chat.id).exists() and not has_contact_in_message:
        phone_button = KeyboardButton(text='Отправить номер телефона', request_contact=True)
        context.bot.send_message(chat_id=chat.id,
                                 text=f'Пожалуйста, отправьте мне свой номер телефона для регистрации '
                                      f'(кнопка "Отправить номер телефона")',
                                 reply_markup=ReplyKeyboardMarkup([[phone_button]]))
        return

    if has_contact_in_message:
        # TODO find employee by phone number. If exists - set chat_id and save. If not exists - create with chat_id and phone number
        phone_number = update.message.contact.phone_number
        if Employee.objects.filter(phone_number=phone_number).exists():
            employee = Employee.objects.get(phone_number=phone_number)
            employee.chat_id = chat.id
            employee.save()
        else:
            Employee.objects.create(chat_id=chat.id, phone_number=phone_number)
        location_button = KeyboardButton(text='Начать смену', request_location=True)
        context.bot.send_message(chat_id=chat.id, text='Спасибо, что поделились номером телефона!\n'
                                                       'Для начала смены нажмите кнопку "Начать смену"',
                                 reply_markup=ReplyKeyboardMarkup([[location_button]], one_time_keyboard=True))
        return

    if hasattr(update, 'message') and hasattr(update.message, 'location'):
        employee = Employee.objects.get(chat_id=chat.id)
        #TODO to handle assignment not exist error
        if not JobRequestAssignment.objects.filter(Q(employee=employee) & Q(assignment_date=datetime.datetime.today())).exists():
            context.bot.send_message(chat_id=chat.id, text='Для вас не была назначена заявка на смену.'
                                                           '\nОбратитесь к менеджеру.')
            return

        # TODO ensure its today's assignment
        assignment = JobRequestAssignment.objects.get(employee=employee, assignment_date=datetime.datetime.today())

        if assignment.start_position is None:
            geo_position = update.message.location
            employee_geo_position = EmployeeGeoPosition.objects.create(
                employee=employee, latitude=geo_position['latitude'],
                longitude=geo_position['longitude'])
            assignment.start_position = employee_geo_position
            assignment.save()
            branch = assignment.job_request.branch
            distance = GD((branch.latitude, branch.longitude), (geo_position['latitude'], geo_position['longitude'])).meters

            if distance > 500:
                location_button = KeyboardButton(text='Начать смену', request_location=True)
                context.bot.send_message(chat_id=chat.id, text='Вы находитесь не на территории филиала.'
                                                               '\nПожалуйста, вернитесь в офис и отправьте геоданные еще раз',
                                         reply_markup=ReplyKeyboardMarkup([[location_button]], one_time_keyboard=True))
                return

            location_button = KeyboardButton(text='Закончить смену', request_location=True)
            context.bot.send_message(chat_id=chat.id,
                                     text=f'Спасибо, мы записали ваши данные о начале смены.\n'
                                          f'Не забудьте завершить смену, нажав на кнопку "Закончить смену"',
                                     reply_markup=ReplyKeyboardMarkup([[location_button]], one_time_keyboard=True))
        elif assignment.end_position is None:
            geo_position = update.message.location
            employee_geo_position = EmployeeGeoPosition.objects.create(
                employee=employee, latitude=geo_position['latitude'],
                longitude=geo_position['longitude'])
            assignment.end_position = employee_geo_position
            assignment.save()
            branch = assignment.job_request.branch
            distance = GD((branch.latitude, branch.longitude),
                          (geo_position['latitude'], geo_position['longitude'])).meters

            if distance > 500:
                location_button = KeyboardButton(text='Закончить смену', request_location=True)
                context.bot.send_message(chat_id=chat.id, text='Вы находитесь не на территории филиала.'
                                                               '\nПожалуйста, вернитесь в офис и отправьте геоданные еще раз',
                                         reply_markup=ReplyKeyboardMarkup([[location_button]], one_time_keyboard=True))
                return

            context.bot.send_message(chat_id=chat.id, text='Спасибо за отметку, ваши данные записаны и отправлены работодателю.')
        else:
            context.bot.send_message(chat_id=chat.id, text='Все уже заполнено, спасибо!')

        return


def start(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    phone_button = KeyboardButton(text='Отправить номер телефона', request_contact=True)
    context.bot.send_message(chat_id=chat.id,
                             text=f'Спасибо, что включили меня, {name}!\n'
                                  f'Пожалуйста, отправьте мне свой номер телефона для регистрации '
                                  f'(кнопка "Отправить номер телефона")', reply_markup=ReplyKeyboardMarkup([[phone_button]], one_time_keyboard=True))


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(MessageHandler(Filters.text, main_func))
updater.dispatcher.add_handler(MessageHandler(Filters.contact, main_func))
updater.dispatcher.add_handler(MessageHandler(Filters.location, main_func))
updater.start_polling()
# updater.idle()

