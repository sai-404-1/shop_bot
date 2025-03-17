from manager.base import *
import manager.templates as templates
from manager.fsm.fsm_class import States as FSM_States

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext

# Инициализация бота и диспетчера
TOKEN = "8107506318:AAEdGyBoDxqXKMwxDdPezJ3lmv7KS_2ccbY" #manager.get_token()
db_session = Database('src/database.db').Session()
photo_path = "src/photo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    from manager import for_restore