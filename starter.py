from manager.base import *
import manager.templates as templates
from manager.fsm.fsm_class import StatesForCreate, StatesForButtons
from keyboards import keyboardFabric

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram import Router

# Инициализация бота и диспетчера
TOKEN = "7992777592:AAFdMeBsbvwkz4lVAOT1uMPdP9w_MQK4XN4" #manager.get_token()
db_session = Database('src/database.db').Session()
fsm_router = Router()
callback_router = Router()
photo_path = "src/photo"

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(fsm_router)
dp.include_router(callback_router)

# Запуск бота
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    from manager import for_restore