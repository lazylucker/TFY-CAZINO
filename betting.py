# Ставки на игроков
def place_bet(user_id, opponent_id, bet_amount, message):
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    user_balance = cursor.fetchone()[0]

    if user_balance < bet_amount:
        bot.send_message(message.chat.id, "Недостаточно средств для ставки!")
        return

    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (opponent_id,))
    opponent_balance = cursor.fetchone()[0]

    if opponent_balance < bet_amount:
        bot.send_message(message.chat.id, "Оппонент не может сделать такую ставку!")
        return

    # Разрешаем ставку
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet_amount, user_id))
    cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet_amount, opponent_id))
    conn.commit()

    # Ставки сделаны, теперь определяем победителя случайным образом
    winner = random.choice([user_id, opponent_id])
    prize = bet_amount * 2  # Победитель забирает всю сумму ставки

    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (prize, winner))
    conn.commit()

    bot.send_message(message.chat.id, f"Ставка прошла! Победитель: {winner}. Он забрал {prize} TFY COINS!")
