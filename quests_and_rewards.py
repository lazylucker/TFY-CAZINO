import sqlite3
from datetime import datetime
import random

# Подключение к базе данных
conn = sqlite3.connect('TFY_CASINO.db', check_same_thread=False)
cursor = conn.cursor()

# Ежедневные бонусы
def daily_bonus(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        last_claim = user[3]  # Дата последнего получения бонуса
        current_time = datetime.now()

        # Проверка, прошли ли 24 часа с последнего бонуса
        if (current_time - datetime.strptime(last_claim, "%Y-%m-%d %H:%M:%S")).days >= 1:
            bonus_amount = random.randint(50, 200)  # Сумма бонуса от 50 до 200 TFY COINS
            cursor.execute('UPDATE users SET balance = balance + ?, last_bonus = ? WHERE user_id = ?',
                           (bonus_amount, current_time.strftime("%Y-%m-%d %H:%M:%S"), user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"🎉 Ты получил ежедневный бонус: {bonus_amount} TFY COINS!")
        else:
            bot.send_message(message.chat.id, "Ты уже получил бонус сегодня. Приходи завтра!")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Ранги игроков
def update_rank(user_id):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # Вычисление ранга игрока на основе баланса
        balance = user[2]
        if balance < 1000:
            rank = 'Новичок'
        elif balance < 5000:
            rank = 'Игрок'
        elif balance < 10000:
            rank = 'Продвинутый'
        else:
            rank = 'VIP'

        cursor.execute('UPDATE users SET rank = ? WHERE user_id = ?', (rank, user_id))
        conn.commit()

# Квесты
def daily_quests(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        current_time = datetime.now()

        # Проверка выполнения квеста (например, за день нужно сделать определенные действия)
        quest_completed = user[4]  # Статус выполнения квеста
        if not quest_completed:
            quest_reward = random.randint(100, 500)  # Награда за выполнение квеста
            cursor.execute('UPDATE users SET balance = balance + ?, quest_completed = ? WHERE user_id = ?',
                           (quest_reward, True, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"🎯 Ты выполнил квест и получил {quest_reward} TFY COINS!")
        else:
            bot.send_message(message.chat.id, "Ты уже выполнил квест сегодня. Удачи в следующем!")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Турниры
def start_tournament(message):
    # Запуск турнира (например, каждый день или каждую неделю)
    tournament_id = random.randint(1, 1000)  # Уникальный ID турнира
    bot.send_message(message.chat.id, f"🏆 Начался новый турнир! Участвуй и выигрывай призы! Турнир ID: {tournament_id}")

# Обмен валюты
def exchange_coins(user_id, amount, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= amount:
            bonus = amount * 1.2  # Обмен по курсу 1.2
            cursor.execute('UPDATE users SET balance = balance - ?, balance_bonus = balance_bonus + ? WHERE user_id = ?',
                           (amount, bonus, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Ты обменял {amount} TFY COINS и получил бонус {bonus} TFY COINS!")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для обмена.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Передача монет
def transfer_coins(sender_id, receiver_id, amount, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (sender_id,))
    sender = cursor.fetchone()
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (receiver_id,))
    receiver = cursor.fetchone()

    if sender and receiver:
        if sender[2] >= amount:
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, sender_id))
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount, receiver_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Ты передал {amount} TFY COINS игроку {receiver_id}.")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для передачи.")
    else:
        bot.send_message(message.chat.id, "Один из игроков не найден в системе.")
