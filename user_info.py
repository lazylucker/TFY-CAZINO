@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = message.from_user.id
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (user_id,))
    balance = cursor.fetchone()
    if balance:
        bot.send_message(message.chat.id, f"Твой текущий баланс: {balance[0]} TFY COINS.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

@bot.message_handler(commands=['status'])
def status(message):
    user_id = message.from_user.id
    cursor.execute('SELECT rank, play_count FROM users WHERE user_id = ?', (user_id,))
    user_status = cursor.fetchone()

    if user_status:
        bot.send_message(message.chat.id, f"Твой текущий ранг: {user_status[0]}\nКоличество игр: {user_status[1]}")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")
