# Регистрация нового пользователя
def register_user(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        bot.send_message(message.chat.id, "Ты уже зарегистрирован в системе!")
    else:
        cursor.execute('INSERT INTO users (user_id, username, balance, rank, play_count, last_claim, combo_count, last_action_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, message.from_user.username, 100, "Beginner", 0, time.time(), 0, time.time()))
        conn.commit()
        bot.send_message(message.chat.id, "Ты успешно зарегистрирован! Начинай играть и выигрывать TFY COINS!")

# Команды для пользователя
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    register_user(user_id, message)

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "Команды:\n/start - Начать игру\n/balance - Посмотреть баланс\n/status - Посмотреть свой статус\n/quests - Посмотреть квесты")
