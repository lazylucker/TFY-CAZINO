import random
import time

# Ежедневный бонус
def daily_bonus(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        last_claim = user[6]
        current_time = time.time()

        # Проверяем, был ли запрос на бонус в течение 24 часов
        if current_time - last_claim >= 86400:  # 86400 секунд = 24 часа
            bonus = random.randint(10, 100)  # Случайный бонус от 10 до 100 TFY COINS
            cursor.execute('UPDATE users SET balance = balance + ?, last_claim = ? WHERE user_id = ?', (bonus, current_time, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Ты получил {bonus} TFY COINS в качестве ежедневного бонуса!")
        else:
            remaining_time = 86400 - (current_time - last_claim)
            bot.send_message(message.chat.id, f"Ты уже получал бонус сегодня. Подожди {int(remaining_time // 3600)} часов и {int((remaining_time % 3600) // 60)} минут.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Ранги игроков
def update_rank(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        play_count = user[7]  # Количество сыгранных игр
        if play_count >= 50:
            new_rank = "VIP"
        elif play_count >= 20:
            new_rank = "Pro"
        else:
            new_rank = "Beginner"

        cursor.execute('UPDATE users SET rank = ? WHERE user_id = ?', (new_rank, user_id))
        conn.commit()

# Квесты
def daily_quest(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        quest_completed = user[8]  # Индикатор выполнения квеста
        if not quest_completed:
            reward = random.randint(50, 150)
            cursor.execute('UPDATE users SET balance = balance + ?, quest_completed = 1 WHERE user_id = ?', (reward, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Ты выполнил квест и получил {reward} TFY COINS!")
        else:
            bot.send_message(message.chat.id, "Ты уже выполнил квест сегодня. Завтра будет новый!")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Турниры
def start_tournament():
    tournament_active = True
    tournament_players = []

    # Запуск турнира
    while tournament_active:
        time.sleep(86400)  # Турнир длится 24 часа

        # Подсчет результатов
        winner = random.choice(tournament_players)
        cursor.execute('UPDATE users SET balance = balance + ?, tournament_wins = tournament_wins + 1 WHERE user_id = ?', (500, winner))
        conn.commit()

        bot.send_message(winner, "Поздравляем! Ты выиграл турнир и получил 500 TFY COINS!")
        tournament_active = False

# Обмен валюты
def exchange_currency(user_id, message, exchange_amount):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        balance = user[2]
        if balance >= exchange_amount:
            bonus = exchange_amount * 0.8  # Обмен с комиссией 20%
            cursor.execute('UPDATE users SET balance = balance - ?, bonus_balance = bonus_balance + ? WHERE user_id = ?', (exchange_amount, bonus, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Ты обменял {exchange_amount} TFY COINS на {bonus} TFY COINS бонуса!")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для обмена.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")
