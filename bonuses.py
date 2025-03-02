import random

# Ежедневные бонусы
def claim_daily_bonus(user_id, message):
    cursor.execute('SELECT last_claim FROM users WHERE user_id = ?', (user_id,))
    last_claim = cursor.fetchone()[0]

    if time.time() - last_claim < 86400:
        # Если прошло меньше 24 часов, пользователь уже получал бонус
        bot.send_message(message.chat.id, "Ты уже забирал бонус сегодня. Приходи завтра!")
        return

    bonus = random.randint(50, 200)  # Случайный бонус от 50 до 200 TFY COINS
    cursor.execute('UPDATE users SET balance = balance + ?, last_claim = ? WHERE user_id = ?', (bonus, time.time(), user_id))
    conn.commit()
    
    bot.send_message(message.chat.id, f"Ты получил ежедневный бонус: {bonus} TFY COINS!")

# Тайный спонсор
def secret_sponsor(user_id, message):
    if random.random() < 0.05:  # 5% шанс на выпадение тайного спонсора
        extra_coins = random.randint(50, 150)
        cursor.execute('UPDATE users SET balance = balance + ? WHERE user_id = ?', (extra_coins, user_id))
        conn.commit()
        bot.send_message(message.chat.id, f"Поздравляем! Ты стал обладателем бонуса от Тайного Спонсора и получил {extra_coins} TFY COINS!")
