# Обработка всех команд и событий
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id

    if anti_abuse(user_id, message):
        return

    if message.text.lower() == "/balance":
        balance(message)
    elif message.text.lower() == "/status":
        status(message)
    elif message.text.lower() == "/quests":
        daily_quest(user_id, message)
    elif message.text.lower().startswith("/bet"):
        bet_amount = int(message.text.split()[1])  # Получаем ставку из сообщения
        if check_bet_limit(user_id, bet_amount, message):
            # Логика для ставок
            pass
    elif message.text.lower() == "/profile":
        view_profile(user_id, message)
