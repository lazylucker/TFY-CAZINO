import random

# Квесты
def generate_quest(user_id, message):
    cursor.execute('SELECT quest_count FROM users WHERE user_id = ?', (user_id,))
    quest_count = cursor.fetchone()[0]

    if quest_count >= 3:
        bot.send_message(message.chat.id, "Ты уже выполнил все квесты на сегодня.")
        return

    # Генерируем случайный квест
    quests = [
        "Выиграй 5 слотов.",
        "Сделай ставку на 100 TFY COINS.",
        "Поиграй в рулетку 3 раза.",
        "Сыграй в покер и выиграй.",
        "Выполни квест и получи 50 TFY COINS."
    ]
    quest = random.choice(quests)

    # Присваиваем квест игроку
    cursor.execute('UPDATE users SET current_quest = ? WHERE user_id = ?', (quest, user_id))
    cursor.execute('UPDATE users SET quest_count = quest_count + 1 WHERE user_id = ?', (user_id,))
    conn.commit()

    bot.send_message(message.chat.id, f"Твой квест: {quest}")
    
def complete_quest(user_id, message):
    cursor.execute('SELECT current_quest FROM users WHERE user_id = ?', (user_id,))
    current_quest = cursor.fetchone()[0]

    if not current_quest:
        bot.send_message(message.chat.id, "Ты не принял квест. Напиши /quests, чтобы начать.")
        return

    reward = random.randint(50, 200)  # Награда за выполнение
    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (reward, user_id))
    cursor.execute('UPDATE users SET current_quest = NULL WHERE user_id = ?', (user_id,))
    conn.commit()

    bot.send_message(message.chat.id, f"Поздравляем! Ты завершил квест и получил {reward} TFY COINS.")
