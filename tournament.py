import random
import time

# Турниры
def start_tournament(message):
    cursor.execute('SELECT COUNT(*) FROM users')
    total_players = cursor.fetchone()[0]

    if total_players < 2:
        bot.send_message(message.chat.id, "Нужно как минимум 2 игрока для начала турнира.")
        return

    tournament_prize_pool = 1000  # Призовой фонд турнира
    bot.send_message(message.chat.id, f"Турнир начался! Призовой фонд: {tournament_prize_pool} TFY COINS.")

    # Выбираем случайных игроков для участия в турнире
    cursor.execute('SELECT user_id FROM users')
    players = cursor.fetchall()
    random.shuffle(players)
    tournament_players = players[:min(10, len(players))]  # Ограничиваем 10 игроками

    # Распределение призового фонда
    prize_distribution = [int(tournament_prize_pool * 0.5), int(tournament_prize_pool * 0.3), int(tournament_prize_pool * 0.2)]

    # Отправляем сообщение игрокам
    for player in tournament_players:
        bot.send_message(player[0], f"Ты участвуешь в турнире! Призовой фонд — {tournament_prize_pool} TFY COINS.")
    
    # Определяем победителей случайным образом
    winners = random.sample(tournament_players, 3)
    
    # Раздаем призы
    for i, winner in enumerate(winners):
        prize = prize_distribution[i]
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (prize, winner[0]))
        conn.commit()
        bot.send_message(winner[0], f"Ты выиграл турнир и получил {prize} TFY COINS!")

# Проверка турнира
def check_tournament(message):
    cursor.execute('SELECT * FROM tournaments WHERE status = "active"')
    active_tournament = cursor.fetchone()

    if active_tournament:
        bot.send_message(message.chat.id, "Турнир уже активен!")
    else:
        start_tournament(message)
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
