import time
import logging
from telebot import TeleBot
from database import conn, cursor
from utils import handle_error, check_player_status, send_help, start_game
from game_mechanics import slots, blackjack, roulette, poker, coin_flip, wheel_of_fortune, minefield, jackpot
from quests import generate_quest, complete_quest
from bonuses import claim_daily_bonus, secret_sponsor
from betting import place_bet
from currency_exchange import exchange_currency
from tournaments import start_tournament, check_tournament
from game_modes import choose_game_mode
from all_in_mode import all_in_mode

API_TOKEN = '7884246690:AAHdoMN0p_T3ZW0WJYfL1ZhBLTlx-KSOdo4'
bot = TeleBot(API_TOKEN)

# Логирование
logging.basicConfig(level=logging.INFO)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    check_player_status(message.from_user.id, message)
    bot.send_message(message.chat.id, "Добро пожаловать в TFY CASINO! Напиши /help для получения списка команд.")

# Обработчик команды /help
@bot.message_handler(commands=['help'])
def handle_help(message):
    send_help(message)

# Обработчик команды /balance
@bot.message_handler(commands=['balance'])
def handle_balance(message):
    cursor.execute('SELECT balance FROM users WHERE user_id = ?', (message.from_user.id,))
    balance = cursor.fetchone()[0]
    bot.send_message(message.chat.id, f"Твой баланс: {balance} TFY COINS")

# Обработчик команды /quests
@bot.message_handler(commands=['quests'])
def handle_quests(message):
    generate_quest(message.from_user.id, message)

# Обработчик команды /claim_bonus
@bot.message_handler(commands=['claim_bonus'])
def handle_claim_bonus(message):
    claim_daily_bonus(message.from_user.id, message)

# Обработчик игры
@bot.message_handler(commands=['play'])
def handle_play(message):
    game_mode_keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    game_mode_keyboard.row('Слоты', 'Блэкджек', 'Рулетка', 'Покер')
    game_mode_keyboard.row('Колесо фортуны', 'Монетка', 'Минное поле', 'Джекпот-лотерея')
    game_mode_keyboard.row('Ставки на гонки', 'Кости (Craps)')

    bot.send_message(message.chat.id, "Выбери игру:", reply_markup=game_mode_keyboard)

# Обработчик выбора игры
@bot.message_handler(func=lambda message: message.text in ['Слоты', 'Блэкджек', 'Рулетка', 'Покер', 'Колесо фортуны', 'Монетка', 'Минное поле', 'Джекпот-лотерея', 'Ставки на гонки', 'Кости (Craps)'])
def handle_game_choice(message):
    game_mode = message.text
    choose_game_mode(message.from_user.id, message, game_mode)

# Обработчик команды /bet для ставок
@bot.message_handler(commands=['bet'])
def handle_bet(message):
    opponent_id = int(message.text.split()[1])
    bet_amount = int(message.text.split()[2])
    place_bet(message.from_user.id, opponent_id, bet_amount, message)

# Обработчик команды /all_in для ALL IN
@bot.message_handler(commands=['all_in'])
def handle_all_in(message):
    all_in_mode(message.from_user.id, message)

# Запуск бота
bot.polling(none_stop=True)
