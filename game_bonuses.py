import random
import time

# Ставки на игроков
def player_bets(user_id, message, bet_amount, target_player_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (target_player_id,))
    target_player = cursor.fetchone()

    if user and target_player:
        if user[2] >= bet_amount:  # Проверяем, есть ли у игрока достаточно монет
            winner = random.choice([user_id, target_player_id])  # Рандомный выбор победителя
            if winner == user_id:
                winnings = bet_amount * 2
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet_amount, user_id))
                cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet_amount, target_player_id))
                conn.commit()
                bot.send_message(message.chat.id, f"Ты выиграл ставку! Получил {winnings} TFY COINS.")
            else:
                cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet_amount, user_id))
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bet_amount, target_player_id))
                conn.commit()
                bot.send_message(message.chat.id, f"Ты проиграл ставку. {target_player[1]} выиграл и забрал {bet_amount} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для этой ставки.")
    else:
        bot.send_message(message.chat.id, "Ошибка. Не удалось найти игроков.")

# Система комбо-выигрышей
def combo_wins(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        combo_count = user[9]  # Счётчик комбо-побед
        if combo_count >= 3:  # Если есть 3 победы подряд
            bonus = random.randint(50, 200)  # Бонус за комбо
            cursor.execute('UPDATE users SET balance = balance + ?, combo_count = 0 WHERE user_id = ?', (bonus, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Поздравляем! Ты получаешь бонус за комбо-выигрыш: {bonus} TFY COINS.")
        else:
            cursor.execute('UPDATE users SET combo_count = combo_count + 1 WHERE user_id = ?', (user_id,))
            conn.commit()
            bot.send_message(message.chat.id, "Ты на пути к комбо-выигрышу! Побеждай еще раз, чтобы получить бонус!")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Тайный спонсор
def secret_sponsor(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        chance = random.random()
        if chance < 0.05:  # 5% шанс на получение тайного спонсора
            bonus = random.randint(50, 500)  # Сумма бонуса от тайного спонсора
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bonus, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"🎁 Тайный спонсор щедро поддержал тебя! Ты получил {bonus} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Тайный спонсор не выбрал тебя в этот раз.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Супер-режим "ALL IN"
def all_in(user_id, message, bet_amount):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= bet_amount:
            all_in_choice = random.choice(["win", "lose"])  # Рандомный выбор: выиграл или проиграл
            if all_in_choice == "win":
                winnings = bet_amount * 2
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet_amount, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"Ты поставил все на кон и выиграл! Получил {winnings} TFY COINS.")
            else:
                cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet_amount, user_id))
                conn.commit()
                bot.send_message(message.chat.id, "Ты проиграл в режиме 'ALL IN'. Все монеты ушли в банк.")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для супер-ставки.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")
