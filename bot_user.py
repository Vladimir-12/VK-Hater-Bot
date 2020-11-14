import vk_api
import random
import config
from vk_api.longpoll import VkLongPoll, VkEventType
import sqlite3

admins = []
bot_id =
token = ''

conn = sqlite3.connect("db.db")
c = conn.cursor()

vk_session = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk_session)
vk = vk_session.get_api()


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


def send_msg_reply(reply_to: int, peer_id: int, message: str, attachment: str = ""):
    return vk.messages.send(**locals(), random_id=0)


def send_msg(peer_id: int, message: str, attachment: str = ""):
    return vk.messages.send(**locals(), random_id=0)


user_ids = []

users = get_all_users()
for user in users:
    user_ids.append(user[0])

while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:

                if event.user_id in user_ids:
                    if not event.from_me:
                        who = random.choice(config.VARIANTS)
                        send_msg_reply(event.message_id, event.peer_id, f'{who}')

                if event.text == "+хейт":
                    if event.user_id in admins or event.user_id == bot_id:
                        msg = vk.messages.getById(message_ids=event.message_id)['items'][0]
                        if 'reply_message' in msg:
                            user = msg['reply_message']['from_id']
                            if user != bot_id:
                                if not is_user_hatelisted(user):
                                    user_ids.append(user)
                                    insert_hatelist(user)
                                    send_msg(event.peer_id, '✅ Пользователь добавлен в хейт лист')
                                else:
                                    send_msg(event.peer_id, '❎ Пользователь уже находится в хейт листе')
                            else:
                                send_msg(event.peer_id, '❎ Невозможно добавить бота в хейт лист')
                        else:
                            send_msg(event.peer_id, '❎ Пользователь не указан')
                    else:
                        choice = random.choice(config.ERRORS)
                        send_msg(event.peer_id, f'{choice}')

                if event.text == "-хейт":
                    if event.user_id in admins or event.user_id == bot_id:
                        msg = vk.messages.getById(message_ids=event.message_id)['items'][0]
                        if 'reply_message' in msg:
                            user = msg['reply_message']['from_id']
                            if is_user_hatelisted(user):
                                user_ids.remove(user)
                                delete_hatelist(user)
                                send_msg(event.peer_id, '✅ Пользователь удален из хейт листа')
                            else:
                                send_msg(event.peer_id, '❎ Пользователя отсутствует в хейт листе')
                        else:
                            send_msg(event.peer_id, '❎ Пользователь не указан')
                    else:
                        choice = random.choice(config.ERRORS)
                        send_msg(event.peer_id, f'{choice}')
    except Exception as e:
        print(repr(e))
