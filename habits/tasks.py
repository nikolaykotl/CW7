import datetime

# import requests
import telebot
from celery import shared_task
from django.utils import timezone

from config.settings import TG_TOKEN, TG_ID
from habits.models import Habit

# from users.models import User

token = TG_TOKEN
user = TG_ID
base_url = 'https://api.telegram.org/bot'


def send_tg_message(user, message):
    '''функция для отправки сообщений'''
    #  url = f'{base_url}{token}/sendMessage'
    # data = {'chat_id': user,
    #        'text': message}
    #  url = f"{base_url}{token}/sendMessage?chat_id={user}&text={message}"
    # requests.get(url, data=data)
    # print(requests.get(url).json())

    bot = telebot.TeleBot(token)
    chat_id = user
    text = message
    bot.send_message(chat_id, text)


def habit_message(obj):

    '''Функция для создания сообщения'''

    action = obj.action
    time_to_complete = obj.time_to_complete
    award = obj.award
    related_habit = obj.related_habit
    if award:
        if time_to_complete:
            return f'Приготовся {action} в течении {time_to_complete}'
        else:
            return f'Приготовся {action}, после можешь {award}'
    elif related_habit:
        if time_to_complete:
            return f'Приготовся {action} в течении {time_to_complete},' \
                   f' после можешь {related_habit.name}'
        else:
            return f'Приготовся {action},' \
                   f' после можешь {related_habit.name}'
    else:
        return f'Приготовся {action}'


@shared_task
def mailing_telegram():
    habits = Habit.objects.all()

    for habit in habits:
        if habit.is_pleasant is False:
            start_time_habit = habit.start_time
            time_up = timezone.now() - datetime.timedelta(minutes=5)
            time_after = timezone.now() + datetime.timedelta(minutes=5)

            if time_up <= start_time_habit <= time_after:
                user = habit.user.tg_id
                message = habit_message(habit)
                send_tg_message(user, message)

            elif start_time_habit < time_up:
                days = habit.periodicity
                if days:
                    while habit.start_time < time_up:
                        habit.start_time = habit.start_time + \
                                           datetime.timedelta(hours=24 * days)
                        habit.save()
