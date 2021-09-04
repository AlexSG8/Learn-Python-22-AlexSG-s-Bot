from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
from random import randint, choice
from glob import glob
from emoji import emojize

logging.basicConfig(filename='bot.log',
                    level=logging.INFO)
PROXY = {'proxy_url': settings.PROXY_URL,
         'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME,
                                  'password': settings.PROXY_PASSWORD}}


def get_smile(user_data):
    if 'emoji' not in user_data:
        smile = choice(settings.USER_EMOJI)
        return emojize(smile, use_aliases=True)
    return user_data['emoji']


def greet_user(update, context):
    """
    Ответ бота на вызов '/start'

    :param update:
    :param context:
    :return:
    """
    print("Вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Привет, пользователь {context.user_data['emoji']}!")


def talk_to_me(update, context):
    """
    Эхо

    :param update:
    :param context:
    :return:
    """

    user_text = update.message.text
    username = update.effective_user.first_name
    print(user_text)
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {user_text}")


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


def guess_number(update, context):
    """
    Обработка /guess для игры в числа

    :param update:
    :param context:
    :return:
    """
    if context.args:
        try:
            user_number = int(context.args[0])
            message = play_random_numbers(user_number)
        except (TypeError, ValueError):
            message = "Введите целое число"
    else:
        message = "Введите целое число"

    update.message.reply_text(message)


def send_cat_picture(update, context):
    """
    Отправка случайной картинки по команде /cat

    :param update:
    :param context:
    :return:
    """
    cat_photos_list = glob("images/*cat*.jp*g")
    cat_pic_filename = choice(cat_photos_list)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, "rb"))


def main():
    mybot = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("guess", guess_number))
    dp.add_handler(CommandHandler("cat", send_cat_picture))

    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    logging.info('Бот стартовал')
    mybot.start_polling()
    mybot.idle()


if __name__ == '__main__':
    main()
