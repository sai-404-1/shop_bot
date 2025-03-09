from starter import *

from aiogram import F
from .buttons import *

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