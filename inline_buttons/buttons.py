from aiogram.utils.keyboard import InlineKeyboardBuilder
from starter import *

def categories():
    builder = InlineKeyboardBuilder()
    for categorie in templates.categories:
        builder.add(types.InlineKeyboardButton(
            text=categorie[0],
            callback_data=categorie[1])
        )
    return builder.as_markup()