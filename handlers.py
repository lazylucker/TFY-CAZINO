from game_features import daily_bonus, daily_quest, update_rank, start_tournament, exchange_currency
from game_bonuses import player_bets, combo_wins, secret_sponsor, all_in

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()

    if not user:
        cursor.execute('INSERT INTO users (user_id, balance, rank, last_claim, quest_completed, tournament_wins, play_count, combo_count) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                       (user_id, 100, 'Beginner', time.time(), 0, 0, 0, 0))
        conn.commit()
        bot.send_message(message.chat.id, "Добро пожаловать в TFY CASINO! Тебе начислено 100 TFY COINS. Приятной игры!")
    else:
        bot.send_message(message.chat.id, "Ты уже зарегистрирован в системе. Готов играть?")

@bot.message_handler(commands=['bonus'])
def claim_bonus(message):
    user_id = message.from_user.id
    daily_bonus(user_id, message)

@bot.message_handler(commands=['quest'])
def claim_quest(message):
    user_id = message.from_user.id
    daily_quest(user_id, message)

@bot.message_handler(commands=['rank'])
def show_rank(message):
    user_id = message.from_user.id
    update_rank(user_id)
    cursor.execute('SELECT rank FROM users WHERE user_id = ?', (user_id,))
    user_rank = cursor.fetchone()[0]
    bot.send_message(message.chat.id, f"Твой текущий ранг: {user_rank}")

@bot.message_handler(commands=['tournament'])
def start_game_tournament(message):
    start_tournament()

@bot.message_handler(commands=['exchange'])
def exchange(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Напиши количество TFY COINS, которое хочешь обменять.")
    bot.register_next_step_handler(message, exchange_amount, user_id)

def exchange_amount(message, user_id):
    try:
        amount = int(message.text)
        exchange_currency(user_id, message, amount)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")

@bot.message_handler(commands=['bet'])
def bet_on_player(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "На какого игрока ставишь? Напиши его ID.")
    bot.register_next_step_handler(message, process_bet, user_id)

def process_bet(message, user_id):
    try:
        target_player_id = int(message.text)
        bot.send_message(message.chat.id, "Напиши сумму ставки.")
        bot.register_next_step_handler(message, process_bet_amount, user_id, target_player_id)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите ID игрока.")

def process_bet_amount(message, user_id, target_player_id):
    try:
        bet_amount = int(message.text)
        player_bets(user_id, message, bet_amount, target_player_id)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную сумму ставки.")

@bot.message_handler(commands=['combo'])
def combo(message):
    user_id = message.from_user.id
    combo_wins(user_id, message)

@bot.message_handler(commands=['sponsor'])
def sponsor(message):
    user_id = message.from_user.id
    secret_sponsor(user_id, message)

@bot.message_handler(commands=['allin'])
def all_in_mode(message):
    user_id = message.from_user.id
    bot.send_message(message.chat.id, "Напиши количество монет, которое хочешь поставить в режиме 'ALL IN'.")
    bot.register_next_step_handler(message, all_in_bet, user_id)

def all_in_bet(message, user_id):
    try:
        bet_amount = int(message.text)
        all_in(user_id, message, bet_amount)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите корректную сумму ставки.")
