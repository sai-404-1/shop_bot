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

@dp.callback_query(F.data.in_([
    "apple", "android", 
    "chargers", "cases","glasses", "speakers", "etc",
    "ps", "xbox",
    "dyson_styler", "dyson_straightener", "dyson_hair_dryer",
    "tablets", "notebooks", "watches", "headphones",
]))
async def apple(callback: types.CallbackQuery):
    # TODO: add state machine for new_devices/used_devices
    type_id = CRUD.for_model(Type).get(db_session, name=callback.data)[0].id
    phones = CRUD.for_model(Product).get(db_session, type_id=type_id)
    buttons = []

    tg = messageGenerator.TextGenerator(callback.data)

    for phone in phones:
        buttons.append(InlineButton(phone.name, "\pupupu/" + tg.getButtonPart() + str(phone.id)))
    await callback.message.edit_text(tg.getMessagePart(), reply_markup=keyboardFabric.createCustomInlineKeyboard(buttons))


# TODO Надо переписать код так, чтобы он обрабатывал любые значения, а не только iphone
# @dp.callback_query(lambda c: re.match(r'^iphone', c.data))
@dp.callback_query(lambda c: "\pupupu/" in c.data) # меточки для обработки
async def process_callback(callback: types.CallbackQuery):
    iphone = CRUD.for_model(Product).get(db_session, id=int(callback.data.replace("iphone", "")))[0]
    await callback.message.answer_photo(
        types.FSInputFile(
            f"{photo_path}/{iphone.photo}"
        ),
        caption="{}\n\n{}\n\n{}".format(iphone.name, iphone.description, iphone.price)
    )