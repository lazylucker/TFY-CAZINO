import random
import sqlite3
from time import time

# Подключение к базе данных
conn = sqlite3.connect('TFY_CASINO.db', check_same_thread=False)
cursor = conn.cursor()

# Ставки на гонки
def race_bet(user_id, horse_number, amount, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= amount:  # Если достаточно средств для ставки
            # Определяем победителя (рандомная лошадка)
            winning_horse = random.randint(1, 5)
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
            conn.commit()

            if horse_number == winning_horse:
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (amount * 2, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"🏇 Ты выиграл ставку на гонки! Твоя лошадка №{horse_number} победила и ты получил {amount * 2} TFY COINS!")
            else:
                bot.send_message(message.chat.id, f"💔 Ты проиграл ставку на гонки. Лошадка №{winning_horse} выиграла.")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для ставки.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Минное поле
def minefield(user_id, amount, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= amount:  # Проверяем наличие средств
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
            conn.commit()

            # Играем в минное поле (рандомно определяем, есть ли мина)
            outcome = random.choice(['safe', 'mine'])
            if outcome == 'safe':
                bonus = random.randint(100, 500)
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (bonus, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"💎 Ты выиграл в минное поле! Найдено {bonus} TFY COINS.")
            else:
                bot.send_message(message.chat.id, "💣 Ты попал на мину! Все монеты потеряны.")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для игры.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Колесо фортуны
def spin_wheel(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # Колесо фортуны с случайными результатами
        wheel_outcome = random.choice(['jackpot', 'small_win', 'lose', 'big_win'])
        cursor.execute('UPDATE users SET balance = balance - 10 WHERE user_id = ?', (user_id))  # Ставка 10 монет на колесо
        conn.commit()

        if wheel_outcome == 'jackpot':
            jackpot = random.randint(500, 1000)
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (jackpot, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"🎉 Джекпот! Ты выиграл {jackpot} TFY COINS на колесе фортуны!")
        elif wheel_outcome == 'big_win':
            big_win = random.randint(100, 500)
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (big_win, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"🎉 Ты выиграл {big_win} TFY COINS на колесе фортуны!")
        elif wheel_outcome == 'small_win':
            small_win = random.randint(10, 50)
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (small_win, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Ты выиграл {small_win} TFY COINS на колесе фортуны!")
        else:
            bot.send_message(message.chat.id, "Колесо фортуны сегодня не в твою пользу. Попробуй еще раз!")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Лотерея с джекпотом
def jackpot_lottery(user_id, amount, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= amount:  # Если достаточно монет для участия
            jackpot_pool = random.randint(1000, 5000)  # Размер джекпота
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (amount, user_id))
            conn.commit()

            # Рандомный выбор победителя
            winner_id = random.randint(1, 1000)
            cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (jackpot_pool, winner_id))
            conn.commit()

            bot.send_message(message.chat.id, f"🎰 Ты принял участие в лотерее с джекпотом {jackpot_pool} TFY COINS. Победитель — игрок {winner_id}!")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для участия в лотерее.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")
