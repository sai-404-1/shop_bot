from manager.base import *
import manager.templates as templates

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# Инициализация бота и диспетчера
TOKEN = "8107506318:AAEdGyBoDxqXKMwxDdPezJ3lmv7KS_2ccbY" #manager.get_token()
db_session = Database('database.db').Session()

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Запуск бота
async def main():
    await dp.start_polling(bot)