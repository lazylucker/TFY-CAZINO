import telebot
import random
from telebot import types
import sqlite3
from datetime import datetime

# Создание подключения к базе данных
conn = sqlite3.connect('TFY_CASINO.db', check_same_thread=False)
cursor = conn.cursor()

# Создание таблиц в базе данных, если их еще нет
cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    balance INTEGER DEFAULT 100,
                    rank TEXT DEFAULT 'Новичок',
                    daily_bonus_received BOOLEAN DEFAULT FALSE,
                    last_login TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
conn.commit()

# Инициализация бота
API_TOKEN = 'YOUR_API_TOKEN'  # Токен бота
bot = telebot.TeleBot(API_TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def start_game(message):
    user_id = message.from_user.id
    username = message.from_user.username

    # Проверка, есть ли пользователь в базе данных
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user is None:
        # Если пользователя нет, добавляем его в базу
        cursor.execute('INSERT INTO users (user_id, username, balance) VALUES (?, ?, ?)', 
                       (user_id, username, 100,))  # Начальный баланс 100 TFY COINS
        conn.commit()
        bot.send_message(message.chat.id, f"Yo, {username}! Добро пожаловать в TFY CASINO! Ты попал в мир, где каждый день можно подняться на TFY COINS! Твой стартовый баланс: 100 TFY COINS.")
    else:
        bot.send_message(message.chat.id, f"Yo, {username}! Ты снова с нами. Твой баланс: {user[2]} TFY COINS. Готов разжигать этот день?")

    # Кнопки для взаимодействия
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    item1 = types.KeyboardButton("🎰 Играть")
    item2 = types.KeyboardButton("🎁 Ежедневный бонус")
    item3 = types.KeyboardButton("💰 Мой баланс")
    item4 = types.KeyboardButton("🏆 Турниры")
    markup.add(item1, item2, item3, item4)
    bot.send_message(message.chat.id, "Чё будешь делать? Стартуем или разогреваемся?", reply_markup=markup)

# Команда для ежедневного бонуса
@bot.message_handler(func=lambda message: message.text.lower() == 'ежедневный бонус')
def daily_bonus(message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        # Проверка, был ли уже получен бонус
        if user[4] == 0:  # Если бонус еще не был получен
            bonus = random.randint(20, 50)  # Сумма бонуса
            cursor.execute('UPDATE users SET balance = balance + ?, daily_bonus_received = 1 WHERE user_id = ?', (bonus, user_id))
            conn.commit()
            bot.send_message(message.chat.id, f"Чисто бонусом тебе закинуло {bonus} TFY COINS! Ты в деле, братишка! Текущий баланс: {user[2] + bonus} TFY COINS.")
        else:
            bot.send_message(message.chat.id, "Ты уже забрал свой бонус сегодня, парниша! Завтра возвращайся за своим.")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Команда для проверки баланса
@bot.message_handler(func=lambda message: message.text.lower() == 'мой баланс')
def check_balance(message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if user:
        bot.send_message(message.chat.id, f"Твой баланс: {user[2]} TFY COINS. Готов к большому хапку?")
    else:
        bot.send_message(message.chat.id, "Ты не зарегистрирован в системе. Напиши /start, чтобы начать.")

# Команда для отображения турниров
@bot.message_handler(func=lambda message: message.text.lower() == 'турниры')
def show_tournaments(message):
    # Временно простая заглушка для турниров
    bot.send_message(message.chat.id, "Турниры на этой неделе:\n- Турнир по слотам: Победитель получит 1000 TFY COINS!\n- Турнир по блэкджеку: Победитель получит 1500 TFY COINS!\nБудешь с нами или просто наблюдаешь?")

# Запуск бота
if __name__ == '__main__':
    bot.polling(none_stop=True)
