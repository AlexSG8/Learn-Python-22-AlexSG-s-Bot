from random import randint, choice
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
import settings


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def play_random_numbers(user_number):
    """
    Игра в числа

    :param user_number:
    :return:
    """
    bot_number = randint(user_number - 10, user_number + 10)

    if bot_number == user_number:
        message = f'{bot_number} = {user_number}. Ничья.'
    elif bot_number > user_number:
        message = f'{bot_number} > {user_number}. Ты проиграл!'
    else:
        message = f'{bot_number} < {user_number}. Ты выиграл!'

    return message


def main_keyboard():
    """
    Формирование основной клавиатуры бота

    :return:
    """
    return ReplyKeyboardMarkup([['Прислать котика', KeyboardButton('Мои координаты', request_location=True)]])
