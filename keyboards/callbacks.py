from starter import *

from aiogram import F
from .buttons import *
import keyboards.keyboardFabric as keyboardFabric
import keyboards.messageGenerator as messageGenerator

from myUtils import Json

@dp.callback_query(F.data == "phones")
async def regenerate_button_callback(callback: types.CallbackQuery):
    products = CRUD.for_model(Product).all(db_session)
    template = ""
    for product in products:
        template += "{} – {}\n".format(product.id, product.name)
    
    await callback.message.edit_text(template)

@dp.callback_query(F.data == "cases")
async def regenerate_button_callback(callback: types.CallbackQuery):
    await callback.message.edit_text("Чехлы (не-а)")

async def send_generated_message(callback):
    data = callback.data
    mg = messageGenerator.MessageGenerator(data)
    await callback.message.edit_text(
        mg.getText(),
        reply_markup = mg.getInlineKeyboard()
    )

@dp.callback_query(F.data.in_([
    "main", "categories", "menu", "new_devices",
    "used_devices", "beauty", "game_consoles",
    "accessories", "smartphones"
]))
async def regenerate_button_callback(callback: types.CallbackQuery):
    await send_generated_message(callback)