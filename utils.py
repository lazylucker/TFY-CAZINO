import time

# Обработка ошибок
def handle_error(message, error):
    bot.send_message(message.chat.id, f"Произошла ошибка: {error}")
    print(f"Error: {error}")

# Проверка статуса игрока
def check_player_status(user_id, message):
    cursor.execute('SELECT balance, quest_count, current_quest, rank FROM users WHERE user_id = ?', (user_id,))
    player_data = cursor.fetchone()

    if player_data:
        balance, quest_count, current_quest, rank = player_data
        bot.send_message(message.chat.id, f"Твой баланс: {balance} TFY COINS\n"
                                          f"Текущий квест: {current_quest}\n"
                                          f"Квестов выполнено: {quest_count}/3\n"
                                          f"Твой ранг: {rank}")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Начни игру!")
        cursor.execute('INSERT INTO users (user_id, balance, quest_count, current_quest, rank) VALUES (?, ?, ?, ?, ?)', 
                       (user_id, 100, 0, None, "Новичок"))
        conn.commit()

# Команда /help для получения информации
def send_help(message):
    help_text = """
    Привет, это TFY CASINO! Вот что ты можешь делать:

    🎰 Слоты, ♠️ Блэкджек, 🔴⚫️ Рулетка, 🎲 Кости (Craps), 🎴 Покер, 🎯 Колесо фортуны, 🎩 Монетка, 🏇 Ставки на гонки, 💎 Минное поле, 💰 Джекпот-лотерея

    🔥 Команды:
    /play - Начни игру
    /quests - Посмотреть доступные квесты
    /balance - Узнать баланс
    /bet - Сделать ставку на игрока
    /rank - Узнать свой ранг
    /help - Получить помощь
    """
    bot.send_message(message.chat.id, help_text)

# Запуск игры
def start_game(message):
    bot.send_message(message.chat.id, "Привет! Готов ли ты испытать удачу в TFY CASINO? Для начала игры выбери одну из игр или воспользуйся командой /help!")
