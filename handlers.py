import os
from glob import glob
from random import choice
import utils
from utils import get_smile, main_keyboard, play_random_numbers


def greet_user(update, context):
    """
    Ответ бота на вызов '/start'

    :param update:
    :param context:
    :return:
    """
    print("Вызван /start")
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Привет, пользователь {context.user_data['emoji']}!", reply_markup=main_keyboard())


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
    update.message.reply_text(f"Здравствуй, {username} {context.user_data['emoji']}! Ты написал: {user_text}",
                              reply_markup=main_keyboard())


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

    update.message.reply_text(message, reply_markup=main_keyboard())


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
    context.bot.send_photo(chat_id=chat_id, photo=open(cat_pic_filename, "rb"), reply_markup=main_keyboard())


def user_coordinates(update, context):
    """
    Возврат координат геопозиции

    :param update:
    :param context:
    :return:
    """
    coords = update.message.location
    context.user_data['emoji'] = get_smile(context.user_data)
    update.message.reply_text(f"Ваши координаты:\n широта: {coords['latitude']},"
                              f"\n долгота: {coords['longitude']} \n{context.user_data['emoji']}",
                              reply_markup=main_keyboard())


def check_user_photo(update, context):
    """
    Загрузка файла пользователя

    :param update:
    :param context:
    :return:
    """

    update.message.reply_text("Обрабатываю фото")
    os.makedirs('downloads', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    filename = os.path.join('downloads', f'cat_{photo_file.file_id}.jpg')
    photo_file.download(filename)

    if utils.is_cat(photo_file['file_path']):
        update.message.reply_text("Обнаружен котик, добавляю в библиотеку.")
        new_filename = os.path.join('images', f'cat_{photo_file.file_id}.jpg')
        os.rename(filename, new_filename)
    else:
        os.remove(filename)
        update.message.reply_text("Котик не обнаружен!")
