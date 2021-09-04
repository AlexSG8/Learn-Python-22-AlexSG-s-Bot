from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
from random import randint

logging.basicConfig(filename='bot.log',
                    level=logging.INFO)
PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
                                  'password': settings.PROXY_PASSWORD}}


def greet_user(update, context):
    """
    Ответ бота на вызов '/start'

    :param update:
    :param context:
    :return:
    """
    print("Вызван /start")

    update.message.reply_text('Привет, пользователь! Ты вызвал команду /start')


def talk_to_me(update, context):
    """
    Эхо

    :param update:
    :param context:
    :return:
    """
    user_text = update.message.text
    print(user_text)
    update.message.reply_text(user_text)


def play_random_numbers(user_number):
    bot_number = randint(user_number - 10, user_number + 10)

    if bot_number == user_number:
        message = f'{bot_number} = {user_number}. Ничья.'
    elif bot_number > user_number:
        message = f'{bot_number} > {user_number}. Ты проиграл!'
    else:
        message = f'{bot_number} < {user_number}. Ты выиграл!'

    return message


def guess_number(update, context):

    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"

    update.message.reply_text(message)


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
