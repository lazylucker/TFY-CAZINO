# Профиль игрока
def view_profile(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        rank = user[3]
        play_count = user[4]
        combo_count = user[6]
        bot.send_message(message.chat.id, f"Твой профиль:\nРанг: {rank}\nКоличество игр: {play_count}\nСерия побед: {combo_count}")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")
