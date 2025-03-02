import random
import time

# Запуск турнира
def start_tournament():
    cursor.execute('SELECT * FROM users ORDER BY balance DESC LIMIT 10')
    top_players = cursor.fetchall()

    if len(top_players) < 2:
        return "Недостаточно игроков для турнира."

    tournament_pot = sum(player[2] for player in top_players)  # Сумма всех монет в банке турнира
    winner = random.choice(top_players)  # Случайный выбор победителя из ТОП-10
    winner_id = winner[0]
    prize = tournament_pot * 0.8  # 80% банка идет победителю

    cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (prize, winner_id))
    conn.commit()

    return f"Турнир завершен! Победитель: {winner[1]}, он забирает {prize} TFY COINS."

# Квесты
def daily_quest(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        quest_completed = user[4]
        if quest_completed < 1:
            reward = random.randint(50, 150)  # Сумма за выполнение квеста
            cursor.execute('UPDATE users SET balance = balance + ?, quest_completed = quest_completed + 1 WHERE user_id = ?',
                           (reward, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Поздравляем! Ты выполнил квест и получил {reward} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Ты уже выполнил этот квест сегодня.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Обновление рангов
def update_rank(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        play_count = user[7]  # Счётчик игр
        if play_count >= 50:
            new_rank = "Pro"
        elif play_count >= 30:
            new_rank = "Intermediate"
        else:
            new_rank = "Beginner"

        cursor.execute('UPDATE users SET rank = ? WHERE user_id = ?', (new_rank, user_id))
        conn.commit()
