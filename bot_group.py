import time
import vk_api
import random
import config as c
from threading import Thread
from modules import sqlite_methods as m
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

vk = vk_api.VkApi(token=c.g_token)
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, c.group_id)


def send_msg(peer_id: int, message: str, attachment: str = ""):
    return vk.method("messages.send", {**locals(), "random_id": 0})


user_ids = []

users = m.get_all_users()
for user in users:
    user_ids.append(user[0])

settings_result = []

settings = m.get_settings(2)
for value in settings:
    settings_result.append(value)

random.shuffle(c.VARIANTS)


def hate():
    index = 0
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:

                    if event.obj.from_id in user_ids:
                        if index < len(c.VARIANTS):
                            time.sleep(settings_result[1])
                            send_msg(event.obj.peer_id, f'{c.VARIANTS[index]}')
                            index += 1
                        else:
                            index = 0
                            random.shuffle(c.VARIANTS)
                            time.sleep(settings_result[1])
                            send_msg(event.obj.peer_id, f'{c.VARIANTS[index]}')
                            index += 1
        except Exception as e:
            print(repr(e))


def commands():
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkBotEventType.MESSAGE_NEW:

                    text = event.object.text
                    split_text = event.object.text.split(' ')

                    if text == "+хейт":
                        if event.obj.from_id in c.g_admins:
                            if 'reply_message' in event.object:
                                user = event.obj.reply_message['from_id']
                                if user != -c.group_id:
                                    if not m.is_user_hatelisted(user):
                                        user_ids.append(user)
                                        m.insert_hatelist(user)
                                        send_msg(event.obj.peer_id, '✅ Пользователь добавлен в хейт лист')
                                    else:
                                        send_msg(event.obj.peer_id, '❎ Пользователь уже находится в хейт листе')
                                else:
                                    send_msg(event.obj.peer_id, '❎ Невозможно добавить бота в хейт лист')
                            else:
                                send_msg(event.obj.peer_id, '❎ Пользователь не указан')
                        else:
                            choice = random.choice(c.ERRORS)
                            send_msg(event.obj.peer_id, f'{choice}')

                    if text == "-хейт":
                        if event.obj.from_id in c.g_admins:
                            if 'reply_message' in event.object:
                                user = event.obj.reply_message['from_id']
                                if m.is_user_hatelisted(user):
                                    user_ids.remove(user)
                                    m.delete_hatelist(user)
                                    send_msg(event.obj.peer_id, '✅ Пользователь удален из хейт листа')
                                else:
                                    send_msg(event.obj.peer_id, '❎ Пользователь отсутствует в хейт листе')
                            else:
                                send_msg(event.obj.peer_id, '❎ Пользователь не указан')
                        else:
                            choice = random.choice(c.ERRORS)
                            send_msg(event.obj.peer_id, f'{choice}')

                    if split_text[0] in c.cooldown:
                        if len(split_text) == 2 and split_text[1].isnumeric():
                            settings_result.pop(1)
                            settings_result.insert(1, int(split_text[1]))
                            m.set_cooldown(int(split_text[1]), 2)
                            send_msg(event.obj.peer_id, f'✅ Задержка изменена на {split_text[1]} секунд')
                        else:
                            send_msg(event.obj.peer_id, '❎ Неверный формат команды')
        except Exception as e:
            print(repr(e))


if __name__ == '__main__':
    Thread(target=hate, args=[]).start()
    Thread(target=commands, args=[]).start()
