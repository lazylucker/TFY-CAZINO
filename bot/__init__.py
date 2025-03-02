from aiogram import Dispatcher

from .handlers import register_handlers


def setup_bot(dp: Dispatcher):
    """Функция для настройки бота и регистрации обработчиков."""
    register_handlers(dp)
