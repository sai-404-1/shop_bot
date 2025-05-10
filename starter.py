from manager.base import *
import manager.templates as templates
from manager.fsm.fsm_class import StatesForCreate, StatesForUpdate, StatesForButtons, StatesForManager, StatesForRegBasket
from keyboards import keyboardFabric

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, InputMediaPhoto, FSInputFile
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram import Router
from aiogram.utils.deep_linking import create_start_link
import myUtils.Json as Json
from myUtils.fastFunctions.photo_service import MediaGroupMiddleware

# Инициализация бота и диспетчера
# TOKEN = "8189724684:AAFEEBUKaYrGwqoCBsWH5qE_HsdaTwygT1U" 
TOKEN = "8192189600:AAGBp3jHPZnykrMTQAikHFTxA57QOAmnGNg"
# TOKEN = "7816677166:AAF_ppIzs1oPRV3-agwb5Xeb8sVGX-3fm1o"
# TOKEN = "7543943279:AAG20NNnPm-SIOjVB43rbdHM_w4Gx8usEFM" #manager.get_token()
db_session = Database('src/database.db').Session()
photo_path = "src/photo"

bot = Bot(token=TOKEN)
dp = Dispatcher()

fsm_router = Router()
callback_router = Router()
phone_number = Router()
dp.include_router(phone_number)
dp.include_router(fsm_router)
dp.include_router(callback_router)

# Запуск бота
async def main():
    dp.message.middleware(MediaGroupMiddleware())
    await dp.start_polling(bot)

if __name__ == "__main__":
    # from manager import for_restore
    from manager import change_type
