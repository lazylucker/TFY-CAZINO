import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота
TOKEN = os.getenv("BOT_TOKEN")

# Настройки базы данных
DB_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///database.db")

# Валюта
CURRENCY_NAME = "TFY COINS"

# Игровые настройки
DAILY_BONUS = 100  # Ежедневный бонус в TFY COINS
MIN_BET = 10       # Минимальная ставка
MAX_BET = 1000     # Максимальная ставка

# Настройки ограничений
RATE_LIMIT = 1  # Ограничение по времени (в секундах) на выполнение команд
