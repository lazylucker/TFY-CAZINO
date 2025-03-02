# Мульти-игровые режимы
def choose_game_mode(user_id, message, game_mode):
    if game_mode == "slots":
        bot.send_message(message.chat.id, "Ты выбрал слоты! Желаем удачи!")
        # Логика игры в слоты
    elif game_mode == "blackjack":
        bot.send_message(message.chat.id, "Ты выбрал Блэкджек! Делай ставку.")
        # Логика игры в блэкджек
    elif game_mode == "roulette":
        bot.send_message(message.chat.id, "Ты выбрал Рулетку! Рискни всем!")
        # Логика игры в рулетку
    elif game_mode == "poker":
        bot.send_message(message.chat.id, "Ты выбрал Покер! Пора блефовать!")
        # Логика игры в покер
    else:
        bot.send_message(message.chat.id, "Неверный режим игры. Попробуй снова.")
