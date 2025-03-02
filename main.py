import logging
import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from bot.handlers import register_handlers

# Логирование
logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    register_handlers(dp)  # Регистрация обработчиков команд
    await dp.start_polling(bot)  # Запуск бота

if __name__ == "__main__":
    asyncio.run(main())
