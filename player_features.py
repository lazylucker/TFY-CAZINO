import sqlite3
import random

# Подключение к базе данных
conn = sqlite3.connect('TFY_CASINO.db', check_same_thread=False)
cursor = conn.cursor()

# Ранги игроков
def update_rank(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # Ранги основываются на количестве выигранных игр
        rank = 'Новичок'
        if user[3] >= 50:  # 50 побед - промежуточный ранг
            rank = 'Игрок'
        if user[3] >= 100:  # 100 побед - высокий ранг
            rank = 'Профи'
        if user[3] >= 200:  # 200 побед - VIP
            rank = 'VIP'

        cursor.execute('UPDATE users SET rank = ? WHERE user_id = ?', (rank, user_id))
        conn.commit()

        bot.send_message(message.chat.id, f"🔥 Твой новый ранг: {rank}. Продолжай выигрывать, чтобы достичь новых высот!")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Квесты
def complete_quest(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # Простые квесты, например: выиграть определенное количество игр
        quests = [
            {"task": "Выиграй 5 игр", "reward": 100, "completed": user[5] >= 5},
            {"task": "Выиграй 10 игр", "reward": 200, "completed": user[5] >= 10},
            {"task": "Попробуй все игры", "reward": 300, "completed": user[6] == 10},  # 10 разных игр
        ]

        available_quests = [quest for quest in quests if not quest['completed']]
        if available_quests:
            quest = random.choice(available_quests)
            bot.send_message(message.chat.id, f"🔑 Квест: {quest['task']}. Награда: {quest['reward']} TFY COINS.")
            cursor.execute('UPDATE users SET completed_quests = completed_quests + 1 WHERE user_id = ?', (user_id,))
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (quest['reward'], user_id))
            conn.commit()
        else:
            bot.send_message(message.chat.id, "Ты выполнил все доступные квесты. Новый квест будет доступен через некоторое время!")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Турниры
def start_tournament(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        tournament_entries = random.randint(10, 50)  # Случайное количество участников турнира
        tournament_prize = tournament_entries * 100  # Призовой фонд

        # Выбираем победителя турнира
        winner_id = random.randint(1, 1000)  # случайный победитель
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (tournament_prize, winner_id))
        conn.commit()

        bot.send_message(message.chat.id, f"🏆 Турнир завершен! Призовой фонд: {tournament_prize} TFY COINS. Победитель: игрок {winner_id}.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Ставки на игроков
def bet_on_player(user_id, bet_id, amount, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (bet_id,))
    bet_user = cursor.fetchone()

    if user and bet_user:
        if user[2] >= amount:
            outcome = random.choice(['win', 'lose'])
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
            if outcome == 'win':
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount * 2, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"💥 Ты выиграл ставку на игрока {bet_user[1]}! Получаешь {amount * 2} TFY COINS.")
            else:
                conn.commit()
                bot.send_message(message.chat.id, f"💔 Ты проиграл ставку на игрока {bet_user[1]}.")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно средств для ставки.")
    else:
        bot.send_message(message.chat.id, "Ошибка: один из игроков не зарегистрирован в системе.")
