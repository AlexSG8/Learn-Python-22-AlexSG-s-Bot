from random import randint, choice
from emoji import emojize
from telegram import ReplyKeyboardMarkup, KeyboardButton
from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2

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


def is_cat(url):
    """
    Проверка фото на котиков

    :param url: Ссылка на картинку
    :return:
    """

    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
    # This is how you authenticate.
    metadata = (('authorization', f'Key {settings.CLARIFAI_API_KEY}'),)

    request = service_pb2.PostModelOutputsRequest(
        model_id='aaa03c23b3724a16a56b629203edc62c',
        inputs=[
            resources_pb2.Input(data=resources_pb2.Data(image=resources_pb2.Image(url=url)))
        ])
    response = stub.PostModelOutputs(request, metadata=metadata)

    for concept in response.outputs[0].data.concepts:
        if concept.name == 'cat' and concept.value >= 0.7:
            return True

    return False
