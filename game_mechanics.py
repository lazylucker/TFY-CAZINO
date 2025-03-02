import random
import sqlite3
from time import time

# Подключение к базе данных
conn = sqlite3.connect('TFY_CASINO.db', check_same_thread=False)
cursor = conn.cursor()

# Обмен валюты
def exchange_coins(user_id, amount, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= amount:  # Если достаточно монет
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
            cursor.execute('UPDATE users SET special_bonus = special_bonus + ? WHERE user_id = ?', (amount, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"✅ Ты обменял {amount} TFY COINS на бонусы! Теперь у тебя {user[2] - amount} TFY COINS и {user[7] + amount} бонусных монет.")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для обмена.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Тайный спонсор
def secret_sponsor(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # С вероятностью 10% пользователю выдается подарок от тайного спонсора
        if random.random() < 0.1:
            bonus = random.randint(50, 200)  # Случайный бонус
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bonus, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"🎉 Тайный спонсор подарил тебе {bonus} TFY COINS! Везет!")
        else:
            bot.send_message(message.chat.id, "Тайный спонсор сегодня молчит. Попробуй позже.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Режим "ALL IN" (все ставки на кон)
def all_in(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] > 0:  # Если есть хотя бы 1 монета для ставки
            bet_amount = user[2]  # Ставим все монеты
            outcome = random.choice(['win', 'lose'])

            if outcome == 'win':
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bet_amount * 2, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"🔥 Ты выиграл ставку ALL IN! Баланс удвоен! У тебя теперь {user[2] * 2} TFY COINS.")
            else:
                cursor.execute('UPDATE users SET balance = 0 WHERE user_id = ?', (user_id,))
                conn.commit()
                bot.send_message(message.chat.id, f"💔 Ты проиграл ставку ALL IN. Все монеты потеряны.")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для ставки ALL IN.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Система комбо-выигрышей
def combo_bonus(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # Проверка на серию побед
        if user[4] >= 3:  # Если игрок выиграл 3 раза подряд
            bonus = random.randint(100, 500)
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bonus, user_id))
            cursor.execute('UPDATE users SET streak = 0 WHERE user_id = ?', (user_id))  # Сбросить серию
            conn.commit()
            bot.send_message(message.chat.id, f"🔥 Ты в комбо-выигрыше! Получаешь {bonus} TFY COINS за серию побед!")
        else:
            bot.send_message(message.chat.id, "Ты еще не в серии побед. Попробуй выиграть несколько раз подряд.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")
