import random

# Слоты
def slots(user_id, message):
    result = random.choice(['🍒', '🍊', '🍉', '🍇', '🍓', '7️⃣'])
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        bet = user[5]  # Ставка пользователя
        if user[2] >= bet:
            outcome = [result, result, result]
            if result == '7️⃣':  # Джекпот
                winnings = bet * 10
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"🎰 Ты выиграл джекпот! Получил {winnings} TFY COINS! Результат: {outcome}")
            else:
                cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
                conn.commit()
                bot.send_message(message.chat.id, f"Ты проиграл {bet} TFY COINS. Результат: {outcome}")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для этой ставки.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Блэкджек
def blackjack(user_id, message):
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)

    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        bet = user[5]  # Ставка
        if user[2] >= bet:
            player_hand = [deck.pop(), deck.pop()]
            dealer_hand = [deck.pop(), deck.pop()]

            def calc_hand(hand):
                total = 0
                aces = hand.count('A')
                for card in hand:
                    if card in ['J', 'Q', 'K']:
                        total += 10
                    elif card == 'A':
                        total += 11
                    else:
                        total += int(card)
                while total > 21 and aces:
                    total -= 10
                    aces -= 1
                return total

            player_total = calc_hand(player_hand)
            dealer_total = calc_hand(dealer_hand)

            # Игровая логика
            if player_total > 21:
                result = f"Перебрал! Ты проиграл {bet} TFY COINS."
                cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))
            elif dealer_total > 21 or player_total > dealer_total:
                winnings = bet * 2
                result = f"Ты победил! Получил {winnings} TFY COINS."
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
            elif player_total == dealer_total:
                result = f"Ничья. Твой баланс не изменился."
            else:
                result = f"Ты проиграл. Ставка {bet} TFY COINS ушла в банк."
                cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))

            conn.commit()
            bot.send_message(message.chat.id, f"Твои карты: {player_hand} ({player_total})\nКарты дилера: {dealer_hand} ({dealer_total})\n{result}")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для этой ставки.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Рулетка
def roulette(user_id, message):
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        bet = user[5]  # Ставка
        if user[2] >= bet:
            bet_choice = random.choice(['красное', 'черное', 'зеро', 'число'])
            winning_number = random.randint(0, 36)
            color = 'красное' if winning_number % 2 == 0 else 'черное'

            if bet_choice == 'красное' and color == 'красное':
                winnings = bet * 2
                result = f"Поздравляем! Выиграл цвет! Получил {winnings} TFY COINS."
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
            elif bet_choice == 'черное' and color == 'черное':
                winnings = bet * 2
                result = f"Поздравляем! Выиграл цвет! Получил {winnings} TFY COINS."
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
            elif bet_choice == 'зеро' and winning_number == 0:
                winnings = bet * 10
                result = f"Поздравляем! Ты угадал зеро! Выиграл {winnings} TFY COINS."
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
            elif bet_choice == 'число' and winning_number == bet:
                winnings = bet * 35
                result = f"Поздравляем! Ты угадал число! Выиграл {winnings} TFY COINS."
                cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (winnings, user_id))
            else:
                result = f"Ты проиграл {bet} TFY COINS. Число: {winning_number}, Цвет: {color}."
                cursor.execute('UPDATE users SET balance = balance - ? WHERE user_id = ?', (bet, user_id))

            conn.commit()
            bot.send_message(message.chat.id, f"Рулетка: {result}")
        else:
            bot.send_message(message.chat.id, "У тебя недостаточно монет для этой ставки.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")
