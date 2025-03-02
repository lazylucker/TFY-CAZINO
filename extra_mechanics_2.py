import sqlite3
import random

# Подключение к базе данных
conn = sqlite3.connect('TFY_CASINO.db', check_same_thread=False)
cursor = conn.cursor()

# Обмен валюты
def exchange_currency(user_id, message, amount, bonus_type):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= amount:  # Проверяем, хватает ли средств на обмен
            if bonus_type == 'Бонус на ставку':
                bonus = random.randint(20, 50)
                cursor.execute('UPDATE users SET balance = balance + ?, special_bonus = special_bonus + ? WHERE user_id = ?', 
                               (bonus, bonus, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"💸 Ты обменял {amount} TFY COINS и получил бонус на ставку в размере {bonus} TFY COINS.")
            elif bonus_type == 'Бонус на баланс':
                bonus = random.randint(100, 300)
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bonus, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"💸 Ты обменял {amount} TFY COINS и получил бонус на баланс в размере {bonus} TFY COINS.")
            else:
                bot.send_message(message.chat.id, "Неизвестный тип бонуса.")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств для обмена.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Передача монет между игроками
def transfer_coins(sender_id, receiver_id, amount, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (sender_id,))
    sender = cursor.fetchone()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (receiver_id,))
    receiver = cursor.fetchone()

    if sender and receiver:
        if sender[2] >= amount:
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, sender_id))
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, receiver_id))
            conn.commit()
            bot.send_message(message.chat.id, f"🤝 Ты передал {amount} TFY COINS игроку {receiver[1]}. Твой баланс: {sender[2] - amount} TFY COINS.")
            bot.send_message(receiver_id, f"🎁 Ты получил {amount} TFY COINS от игрока {sender[1]}. Твой баланс: {receiver[2] + amount} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств для передачи.")
    else:
        bot.send_message(message.chat.id, "Ошибка в передаче. Проверь ID игроков.")

# Супер-режим "ALL IN"
def all_in(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        bet = user[2]  # Ставим весь баланс
        if bet > 0:
            roll = random.choice(['Удача', 'Неудача'])
            cursor.execute('UPDATE users SET balance = 0 WHERE user_id = ?', (user_id,))
            conn.commit()

            if roll == 'Удача':
                winnings = bet * 2
                cursor.execute('UPDATE users SET balance = ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"🔥 Супер-режим 'ALL IN': Ты рискнул всем! Удача! Получаешь {winnings} TFY COINS. Твой новый баланс: {winnings} TFY COINS.")
            else:
                bot.send_message(message.chat.id, f"🔥 Супер-режим 'ALL IN': Ты рискнул всем! Неудача! Проиграл все. Твой новый баланс: 0 TFY COINS.")
        else:
            bot.send_message(message.chat.id, "У тебя нет средств для игры в 'ALL IN'.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Комбо-выигрыши
def combo_bonus(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # Проверяем, не был ли игрок в серии побед
        if user[4] >= 3:  # Если у игрока есть 3 или больше побед подряд
            combo_bonus = random.randint(50, 200)
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (combo_bonus, user_id))
            cursor.execute('UPDATE users SET win_streak = 0 WHERE user_id = ?', (user_id))  # Обнуляем серию побед
            conn.commit()

            bot.send_message(message.chat.id, f"🔥 Ты в серии побед! Комбо-выигрыш! Получаешь {combo_bonus} TFY COINS. Твой новый баланс: {user[2] + combo_bonus} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Ты не в серии побед, но продолжай играть!")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Шанс на Тайного спонсора
def secret_sponsor(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        chance = random.randint(1, 100)
        if chance <= 5:  # 5% шанс на Тайного спонсора
            sponsor_bonus = random.randint(50, 300)
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (sponsor_bonus, user_id))
            conn.commit()

            bot.send_message(message.chat.id, f"🎉 Ты получил бонус от Тайного спонсора! Получаешь {sponsor_bonus} TFY COINS. Твой новый баланс: {user[2] + sponsor_bonus} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Тайный спонсор не пришел сегодня. Продолжай играть!")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")
