from starter import *

from aiogram import F
from .buttons import *

@dp.callback_query(F.data == "phones")
async def regenerate_button_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("Телефоны (ага)")

@dp.callback_query(F.data == "cases")
async def regenerate_button_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("Чехлы (не-а)")