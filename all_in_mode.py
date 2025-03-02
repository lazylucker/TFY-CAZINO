# Супер-режим "ALL IN"
def all_in_mode(user_id, message):
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()[0]

    if balance <= 0:
        bot.send_message(message.chat.id, "У тебя недостаточно средств для участия в ALL IN режиме.")
        return

    # Включаем режим ALL IN — все средства на кон
    bot.send_message(message.chat.id, "Ты в режиме ALL IN! Все твои средства на кону.")

    # Выигрыш или проигрыш
    result = random.choice(["win", "lose"])

    if result == "win":
        multiplier = random.uniform(2, 5)  # Выигрыш в 2-5 раз больше
        prize = int(balance * multiplier)
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (prize, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"Ты выиграл! Твой выигрыш: {prize} TFY COINS.")
    else:
        cursor.execute('UPDATE users SET balance = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
        bot.send_message(message.chat.id, "Ты проиграл! Все твои средства ушли.")
