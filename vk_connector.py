from random import randint

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import song_generator

# Файл привязки к вк

token = "23460cf20ab5d2b001c99ce020bf71f47a9d5118716b543e8495f5a4024c2438793193ed830dec83f8ca5"
vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, "random_id": randint(0, 10 ** 10)})


def main():
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me:
                request = event.text
                print(request, 'https://vk.com/id' + str(event.user_id))
                answer = song_generator.manipulate(request)
                write_msg(event.user_id, answer)


main()
