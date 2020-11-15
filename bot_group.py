import vk_api
import random
import config
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import sqlite3

admins = []
group_id = 
token = ''

conn = sqlite3.connect("db.db")
c = conn.cursor()

vk = vk_api.VkApi(token=token)
vk._auth_token()
vk.get_api()
longpoll = VkBotLongPoll(vk, group_id)


def is_user_hatelisted(user_id: int) -> bool:
    c.execute("SELECT count(user_id) FROM users WHERE user_id = %d" % user_id)
    result = c.fetchone()[0]
    return result > 0


def insert_hatelist(user_id: int):
    c.execute("INSERT INTO users(user_id) VALUES (%d)" % user_id)
    conn.commit()
    print(f"Пользователь {user_id} добавлен в хейтлист")


def delete_hatelist(user_id: int):
    c.execute("DELETE FROM users WHERE user_id=%d" % user_id)
    conn.commit()
    print(f"Пользователь {user_id} удален из хейтлиста")


def get_all_users():
    c.execute("SELECT * FROM users")
    result = c.fetchall()
    return result


def send_msg(peer_id: int, message: str, attachment: str = ""):
    return vk.method("messages.send", {**locals(), "random_id": 0})


user_ids = []

users = get_all_users()
for user in users:
    user_ids.append(user[0])

random.shuffle(config.VARIANTS)

index = 0

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:

                if event.obj.from_id in user_ids:
                    if index < len(config.VARIANTS):
                        send_msg(event.obj.peer_id, f'{config.VARIANTS[index]}')
                        index += 1
                    else:
                        index = 0
                        random.shuffle(config.VARIANTS)
                        send_msg(event.obj.peer_id, f'{config.VARIANTS[index]}')
                        index += 1

                if event.object.text == "+хейт":
                    if event.obj.from_id in admins:
                        if 'reply_message' in event.object:
                            user = event.obj.reply_message['from_id']
                            if user != -group_id:
                                if not is_user_hatelisted(user):
                                    user_ids.append(user)
                                    insert_hatelist(user)
                                    send_msg(event.obj.peer_id, '✅ Пользователь добавлен в хейт лист')
                                else:
                                    send_msg(event.obj.peer_id, '❎ Пользователь уже находится в хейт листе')
                            else:
                                send_msg(event.obj.peer_id, '❎ Невозможно добавить бота в хейт лист')
                        else:
                            send_msg(event.obj.peer_id, '❎ Пользователь не указан')
                    else:
                        choice = random.choice(config.ERRORS)
                        send_msg(event.obj.peer_id, f'{choice}')

                if event.object.text == "-хейт":
                    if event.obj.from_id in admins:
                        if 'reply_message' in event.object:
                            user = event.obj.reply_message['from_id']
                            if is_user_hatelisted(user):
                                user_ids.remove(user)
                                delete_hatelist(user)
                                send_msg(event.obj.peer_id, '✅ Пользователь удален из хейт листа')
                            else:
                                send_msg(event.obj.peer_id, '❎ Пользователя отсутствует в хейт листе')
                        else:
                            send_msg(event.obj.peer_id, '❎ Пользователь не указан')
                    else:
                        choice = random.choice(config.ERRORS)
                        send_msg(event.obj.peer_id, f'{choice}')
    except Exception as e:
        print(repr(e))
