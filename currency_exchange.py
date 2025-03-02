# Обмен валюты на спец-бонусы
def exchange_currency(user_id, amount, message):
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()[0]

    if balance < amount:
        bot.send_message(message.chat.id, "Недостаточно средств для обмена.")
        return

    # Конвертация TFY COINS в бонусы (например, 1 TFY COIN = 2 бонуса)
    bonus = amount * 2
    cursor.execute('UPDATE users SET balance = balance - ?, bonus_points = bonus_points + ? WHERE user_id = ?', (amount, bonus, user_id))
    conn.commit()

    bot.send_message(message.chat.id, f"Ты обменял {amount} TFY COINS на {bonus} бонусных очков!")
