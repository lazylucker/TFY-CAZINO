import random
from telebot import types
import sqlite3

# Подключение к базе данных
conn = sqlite3.connect('TFY_CASINO.db', check_same_thread=False)
cursor = conn.cursor()

# Игровые механики

# Слоты
def slots_game(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= 10:  # Минимальная ставка 10 TFY COINS
            bet = 10
            result = random.choice(['7', '7', '7', 'X', 'X', 'X', 'BAR', 'BAR', '777', 'JACKPOT'])
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
            conn.commit()

            if result == 'JACKPOT':
                winnings = random.randint(100, 500)
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"🎰 Ты поймал JACKPOT! Получаешь {winnings} TFY COINS! Твой баланс: {user[2] + winnings} TFY COINS.")
            else:
                bot.send_message(message.chat.id, f"🎰 Результат: {result}! Ты проиграл {bet} TFY COINS. Твой баланс: {user[2] - bet} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств для ставки. Минимальная ставка — 10 TFY COINS.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Блэкджек
def blackjack_game(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= 20:  # Минимальная ставка 20 TFY COINS
            bet = 20
            player_hand = random.sample(range(1, 12), 2)
            dealer_hand = random.sample(range(1, 12), 2)
            player_sum = sum(player_hand)
            dealer_sum = sum(dealer_hand)

            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
            conn.commit()

            if player_sum == 21:
                winnings = bet * 2
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"💥 Ты набрал 21! Победа! Получаешь {winnings} TFY COINS. Твой баланс: {user[2] + winnings} TFY COINS.")
            elif player_sum > 21:
                bot.send_message(message.chat.id, f"❌ Перебор! Ты проиграл {bet} TFY COINS. Твой баланс: {user[2] - bet} TFY COINS.")
            else:
                if dealer_sum == 21:
                    bot.send_message(message.chat.id, f"😱 Дилер набрал 21! Ты проиграл {bet} TFY COINS. Твой баланс: {user[2] - bet} TFY COINS.")
                else:
                    bot.send_message(message.chat.id, f"🤔 У тебя: {player_sum}, у дилера: {dealer_sum}. Играй дальше или бросай ставки!")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств для ставки. Минимальная ставка — 20 TFY COINS.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Рулетка
def roulette_game(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        if user[2] >= 10:  # Минимальная ставка 10 TFY COINS
            bet = 10
            result = random.choice(['Красное', 'Черное', 'Зеро'])
            cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
            conn.commit()

            if result == 'Красное':
                winnings = bet * 2
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"🔴 Рулетка: ты выбрал красное и выиграл! Получаешь {winnings} TFY COINS. Твой баланс: {user[2] + winnings} TFY COINS.")
            elif result == 'Черное':
                winnings = bet * 2
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"⚫️ Рулетка: ты выбрал черное и выиграл! Получаешь {winnings} TFY COINS. Твой баланс: {user[2] + winnings} TFY COINS.")
            else:
                bot.send_message(message.chat.id, f"🟢 Рулетка: зеро. Ты проиграл {bet} TFY COINS. Твой баланс: {user[2] - bet} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Недостаточно средств для ставки. Минимальная ставка — 10 TFY COINS.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

