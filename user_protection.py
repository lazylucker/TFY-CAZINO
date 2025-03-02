import time

# Защита от злоупотреблений
def anti_abuse(user_id, message):
    cursor.execute('SELECT last_action_time FROM users WHERE user_id = ?', (user_id,))
    last_action_time = cursor.fetchone()[0]

    if time.time() - last_action_time < 5:
        # Если между действиями игрока прошло меньше 5 секунд, это может быть бот
        bot.send_message(message.chat.id, "Ты слишком быстро делаешь действия! Пожалуйста, подожди немного.")
        return True
    else:
        # Обновляем время последнего действия
        cursor.execute('UPDATE users SET last_action_time = ? WHERE user_id = ?', (time.time(), user_id))
        conn.commit()
        return False

# Ограничение ставок
def check_bet_limit(user_id, bet_amount, message):
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()

    if balance and balance[0] < bet_amount:
        bot.send_message(message.chat.id, "У тебя недостаточно средств для этой ставки!")
        return False

    max_bet = balance[0] * 0.5  # Ограничение ставки до 50% от баланса
    if bet_amount > max_bet:
        bot.send_message(message.chat.id, f"Максимальная ставка — {max_bet} TFY COINS.")
        return False

    return True
