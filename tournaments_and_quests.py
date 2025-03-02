import sqlite3
import random
from datetime import datetime, timedelta

# Подключение к базе данных
conn = sqlite3.connect('TFY_CASINO.db', check_same_thread=False)
cursor = conn.cursor()

# Турниры
def start_tournament(message):
    cursor.execute('SELECT * FROM users ORDER BY balance DESC LIMIT 10')  # ТОП-10 игроков
    top_players = cursor.fetchall()

    if top_players:
        tournament_id = random.randint(1000, 9999)  # Генерируем ID турнира
        cursor.execute('INSERT INTO tournaments (tournament_id, start_time) VALUES (?, ?)', 
                       (tournament_id, datetime.now()))
        conn.commit()

        bot.send_message(message.chat.id, f"🏆 Новый турнир стартует! Прими участие и выиграй супер-приз! ID турнира: {tournament_id}")
        for player in top_players:
            # Добавляем игроков в турнир
            cursor.execute('INSERT INTO tournament_players (tournament_id, user_id) VALUES (?, ?)', 
                           (tournament_id, player[0]))
        conn.commit()

    else:
        bot.send_message(message.chat.id, "Турнир не может начаться, так как нет игроков.")

# Подсчет результатов турнира
def end_tournament(tournament_id, message):
    cursor.execute('SELECT * FROM tournament_players WHERE tournament_id = ?', (tournament_id,))
    players_in_tournament = cursor.fetchall()

    if players_in_tournament:
        # Выбираем победителя случайным образом для простоты
        winner = random.choice(players_in_tournament)
        cursor.execute('SELECT * FROM users WHERE user_id = ?', (winner[1],))
        winner_data = cursor.fetchone()

        winnings = random.randint(1000, 5000)
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, winner[1]))
        conn.commit()

        bot.send_message(message.chat.id, f"🏆 Турнир завершен! Победитель: {winner_data[1]} — {winnings} TFY COINS!")
        cursor.execute('DELETE FROM tournament_players WHERE tournament_id = ?', (tournament_id,))
        conn.commit()
    else:
        bot.send_message(message.chat.id, "Нет участников для завершения турнира.")

# Квесты
def start_quest(user_id, message):
    quests = ['Сыграй 3 игры', 'Потрать 50 TFY COINS', 'Заработай 100 TFY COINS за день', 'Участвуй в турнире']
    selected_quest = random.choice(quests)

    cursor.execute('INSERT INTO quests (user_id, quest_name, status) VALUES (?, ?, ?)', 
                   (user_id, selected_quest, 'Ожидает'))
    conn.commit()

    bot.send_message(message.chat.id, f"🎯 Новый квест: {selected_quest}! Выполни его, чтобы получить награду!")

# Завершение квеста
def complete_quest(user_id, message):
    cursor.execute('SELECT * FROM quests WHERE user_id = ? AND status = ?', (user_id, 'Ожидает'))
    quest = cursor.fetchone()

    if quest:
        rewards = random.randint(100, 500)  # Награда за квест
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (rewards, user_id))
        cursor.execute('UPDATE quests SET status = ? WHERE user_id = ?', ('Завершен', user_id))
        conn.commit()

        bot.send_message(message.chat.id, f"🎯 Ты выполнил квест и получил {rewards} TFY COINS! Поздравляем!")
    else:
        bot.send_message(message.chat.id, "У тебя нет активных квестов.")

# Ранги игроков
def check_player_rank(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        balance = user[2]
        if balance >= 1000:
            rank = 'VIP'
        elif balance >= 500:
            rank = 'Мастер'
        elif balance >= 100:
            rank = 'Продвинутый'
        else:
            rank = 'Новичок'

        bot.send_message(message.chat.id, f"👑 Твой текущий ранг: {rank}. Твой баланс: {balance} TFY COINS.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")
