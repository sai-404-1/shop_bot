from starter import *

import re
from aiogram import F
import os
from .buttons import *
import keyboards.keyboardFabric as keyboardFabric
import keyboards.messageGenerator as messageGenerator

from myUtils import Json

async def send_generated_message(callback):
    data = callback.data
    mg = messageGenerator.MessageGenerator(data)
    await callback.message.edit_text(
        mg.getText(),
        reply_markup = mg.getInlineKeyboard()
    )

# you change start to main in templates.json 
# "домой" have action "main"
@dp.callback_query(F.data.in_([
    "main", "categories", "menu", "new_devices",
    "used_devices", "beauty", "game_consoles",
    "accessories", "smartphones"
]))
async def regenerate_button_callback(callback: types.CallbackQuery):
    await send_generated_message(callback)

@dp.callback_query(F.data == "apple")
async def apple(callback: types.CallbackQuery):
    phones = CRUD.for_model(Product).get(db_session, type_id=1)
    buttons = []
    for phone in phones:
        buttons.append(InlineButton(phone.name, "iphone" + str(phone.id)))
    await callback.message.edit_text("Смартфоны Apple", reply_markup=keyboardFabric.createCustomInlineKeyboard(buttons))


# TODO Надо переписать код так, чтобы он обрабатывал любые значения, а не только iphone
@dp.callback_query(lambda c: re.match(r'^iphone', c.data))
async def process_callback(callback: types.CallbackQuery):
    iphone = CRUD.for_model(Product).get(db_session, id=int(callback.data.replace("iphone", "")))[0]
    await callback.message.answer_photo(
        types.FSInputFile(
            f"{photo_path}/{iphone.photo}"
        ),
        caption="{}\n\n{}\n\n{}".format(iphone.name, iphone.description, iphone.price)
    )