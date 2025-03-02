# Ставки на игроков
def player_bets(user_id, message, bet_amount, target_player_id):
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    user_balance = cursor.fetchone()

    if user_balance and user_balance[0] >= bet_amount:
        cursor.execute('SELECT balance FROM users WHERE user_id = ?', (target_player_id,))
        target_balance = cursor.fetchone()

        if target_balance:
            # Уменьшаем баланс игрока, увеличиваем баланс на целевую ставку
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet_amount, user_id))
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bet_amount, target_player_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Ты поставил {bet_amount} TFY COINS на игрока {target_player_id}.")
            bot.send_message(target_player_id, f"Игрок {user_id} поставил на тебя {bet_amount} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Целевой игрок не найден.")
    else:
        bot.send_message(message.chat.id, "У тебя недостаточно средств для ставки.")

# Комбо-выигрыши
def combo_wins(user_id, message):
    cursor.execute('SELECT combo_count FROM users WHERE user_id = ?', (user_id,))
    combo_count = cursor.fetchone()

    if combo_count:
        if combo_count[0] >= 3:  # Пример: 3 победы подряд дают бонус
            bonus = random.randint(100, 500)  # Сумма бонуса
            cursor.execute('UPDATE users SET balance = balance + ?, combo_count = 0 WHERE user_id = ?', (bonus, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Поздравляем! Ты выиграл серию и получил {bonus} TFY COINS.")
        else:
            bot.send_message(message.chat.id, f"Для бонуса нужно выиграть {3 - combo_count[0]} побед подряд.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Секретный спонсор
def secret_sponsor(user_id, message):
    secret_chance = random.randint(1, 100)
    if secret_chance <= 10:  # 10% шанс на бонус
        bonus = random.randint(50, 200)  # Бонус от секретного спонсора
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bonus, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"Секретный спонсор дарует тебе {bonus} TFY COINS!")
    else:
        bot.send_message(message.chat.id, "Сегодня секретный спонсор не активен.")

# Супер-режим "ALL IN"
def all_in(user_id, message, bet_amount):
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    user_balance = cursor.fetchone()

    if user_balance and user_balance[0] >= bet_amount:
        cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet_amount, user_id))
        conn.commit()

        # Риск по принципу "все или ничего"
        win = random.choice([True, False])
        if win:
            # Победа: удваиваем ставку
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bet_amount * 2, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Ты выиграл в режиме ALL IN! Твой баланс увеличен на {bet_amount * 2} TFY COINS.")
        else:
            # Проигрыш: теряем ставку
            bot.send_message(message.chat.id, f"Ты проиграл в режиме ALL IN и потерял {bet_amount} TFY COINS.")
    else:
        bot.send_message(message.chat.id, "У тебя недостаточно средств для режима 'ALL IN'.")
