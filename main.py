import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from bot.handlers import register_handlers

# Логирование
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Инициализация бота
bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

async def main():
    register_handlers(dp)  # Регистрация обработчиков команд
    logging.info("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Бот остановлен!")
