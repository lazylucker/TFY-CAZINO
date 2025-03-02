import random
from telebot import types
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('TFY_CASINO.db', check_same_thread=False)
cursor = conn.cursor()

# Монетка
def coin_flip(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= 5:  # Минимальная ставка 5 TFY COINS
            bet = 5
            result = random.choice(['Орел', 'Решка'])
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
            conn.commit()

            if result == 'Орел':
                winnings = bet * 2
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"🪙 Ты выбрал Орел и выиграл! Получаешь {winnings} TFY COINS. Твой баланс: {user[2] + winnings} TFY COINS.")
            else:
                bot.send_message(message.chat.id, f"🪙 Ты выбрал Решку и проиграл! Твой баланс: {user[2] - bet} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств для ставки. Минимальная ставка — 5 TFY COINS.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Колесо фортуны
def fortune_wheel(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= 10:  # Минимальная ставка 10 TFY COINS
            bet = 10
            result = random.choice(['Удача', 'Неудача'])
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
            conn.commit()

            if result == 'Удача':
                winnings = random.randint(20, 100)
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"🎉 Колесо фортуны: Удача! Ты выиграл {winnings} TFY COINS. Твой баланс: {user[2] + winnings} TFY COINS.")
            else:
                bot.send_message(message.chat.id, f"🎉 Колесо фортуны: Неудача. Ты проиграл {bet} TFY COINS. Твой баланс: {user[2] - bet} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств для ставки. Минимальная ставка — 10 TFY COINS.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Кости (Craps)
def dice_game(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= 10:  # Минимальная ставка 10 TFY COINS
            bet = 10
            roll = random.randint(2, 12)
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
            conn.commit()

            if roll == 7 or roll == 11:
                winnings = bet * 2
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"🎲 Ты кинул {roll}! Победа! Ты выиграл {winnings} TFY COINS. Твой баланс: {user[2] + winnings} TFY COINS.")
            else:
                bot.send_message(message.chat.id, f"🎲 Ты кинул {roll}. Проиграл {bet} TFY COINS. Твой баланс: {user[2] - bet} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств для ставки. Минимальная ставка — 10 TFY COINS.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Джекпот-лотерея
def jackpot_lottery(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= 10:  # Минимальная ставка 10 TFY COINS
            bet = 10
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
            conn.commit()

            jackpot = random.choice([True, False])
            if jackpot:
                winnings = random.randint(200, 1000)
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"💰 Джекпот! Ты выиграл {winnings} TFY COINS! Твой баланс: {user[2] + winnings} TFY COINS.")
            else:
                bot.send_message(message.chat.id, f"💰 Ты не выиграл джекпот, но не переживай! Проиграл {bet} TFY COINS. Твой баланс: {user[2] - bet} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств для ставки. Минимальная ставка — 10 TFY COINS.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

