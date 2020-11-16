import time
import vk_api
import random
import config as c
from modules import sqlite_methods as m
from threading import Thread
from vk_api.longpoll import VkLongPoll, VkEventType

vk_session = vk_api.VkApi(token=c.u_token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


def send_msg_reply(reply_to: int, peer_id: int, message: str, attachment: str = ""):
    return vk.messages.send(**locals(), random_id=0)


def send_msg(peer_id: int, message: str, attachment: str = ""):
    return vk.messages.send(**locals(), random_id=0)


user_ids = []

users = m.get_all_users()
for user in users:
    user_ids.append(user[0])

settings_result = []

settings = m.get_settings(1)
for value in settings:
    settings_result.append(value)

random.shuffle(c.VARIANTS)


def hate():
    index = 0
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:

                    if event.user_id in user_ids:
                        if not event.from_me:
                            if index < len(c.VARIANTS):
                                time.sleep(settings_result[1])
                                send_msg_reply(event.message_id, event.peer_id, f'{c.VARIANTS[index]}')
                                index += 1
                            else:
                                index = 0
                                random.shuffle(c.VARIANTS)
                                time.sleep(settings_result[1])
                                send_msg_reply(event.message_id, event.peer_id, f'{c.VARIANTS[index]}')
                                index += 1
        except Exception as e:
            print(repr(e))


def commands():
    while True:
        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW:

                    text = event.text
                    split_text = event.text.split(' ')

                    if text in c.hate:
                        if event.user_id in c.u_admins:
                            msg = vk.messages.getById(message_ids=event.message_id)['items'][0]
                            if 'reply_message' in msg:
                                user = msg['reply_message']['from_id']
                                if user != c.bot_id:
                                    if not m.is_user_hatelisted(user):
                                        user_ids.append(user)
                                        m.insert_hatelist(user)
                                        send_msg(event.peer_id, '✅ Пользователь добавлен в хейт лист')
                                    else:
                                        send_msg(event.peer_id, '❎ Пользователь уже находится в хейт листе')
                                else:
                                    send_msg(event.peer_id, '❎ Невозможно добавить бота в хейт лист')
                            else:
                                send_msg(event.peer_id, '❎ Пользователь не указан')
                        else:
                            choice = random.choice(c.ERRORS)
                            send_msg(event.peer_id, f'{choice}')

                    if text in c.unhate:
                        if event.user_id in c.u_admins:
                            msg = vk.messages.getById(message_ids=event.message_id)['items'][0]
                            if 'reply_message' in msg:
                                user = msg['reply_message']['from_id']
                                if m.is_user_hatelisted(user):
                                    user_ids.remove(user)
                                    m.delete_hatelist(user)
                                    send_msg(event.peer_id, '✅ Пользователь удален из хейт листа')
                                else:
                                    send_msg(event.peer_id, '❎ Пользователь отсутствует в хейт листе')
                            else:
                                send_msg(event.peer_id, '❎ Пользователь не указан')
                        else:
                            choice = random.choice(c.ERRORS)
                            send_msg(event.peer_id, f'{choice}')

                    if split_text[0] in c.cooldown:
                        if len(split_text) == 2 and split_text[1].isnumeric():
                            settings_result.pop(1)
                            settings_result.insert(1, int(split_text[1]))
                            m.set_cooldown(int(split_text[1]), 1)
                            send_msg(event.peer_id, f'✅ Задержка изменена на {split_text[1]} секунд')
                        else:
                            send_msg(event.peer_id, '❎ Неверный формат команды')
        except Exception as e:
            print(repr(e))


if __name__ == '__main__':
    Thread(target=hate, args=[]).start()
    Thread(target=commands, args=[]).start()
