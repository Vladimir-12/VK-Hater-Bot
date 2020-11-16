import sqlite3


def is_user_hatelisted(user_id: int) -> bool:
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("SELECT count(user_id) FROM users WHERE user_id = %d" % user_id)
        result = c.fetchone()[0]
    c.close()
    conn.close()
    return result > 0


def insert_hatelist(user_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("INSERT INTO users(user_id) VALUES (%d)" % user_id)
        conn.commit()
        print(f"Пользователь {user_id} добавлен в хейтлист")
    c.close()
    conn.close()


def delete_hatelist(user_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE user_id=%d" % user_id)
        conn.commit()
        print(f"Пользователь {user_id} удален из хейтлиста")
    c.close()
    conn.close()


def get_all_users():
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM users")
        result = c.fetchall()
    c.close()
    conn.close()
    return result


def set_cooldown(cooldown: int, type_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("UPDATE settings SET cooldown = %d WHERE id = %d" % (cooldown, type_id))
        conn.commit()
        print(f"Задержка изменена на {cooldown} секунд")
    c.close()
    conn.close()


def get_settings(type_id: int):
    with sqlite3.connect("database/db.db") as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM settings WHERE id = %d" % type_id)
        result = c.fetchone()
    c.close()
    conn.close()
    return result
