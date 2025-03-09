from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton, KeyboardButton

from .buttons import *
from starter import *

def categories():
    builder = InlineKeyboardBuilder()
    for categorie in templates.categories:
        builder.add(types.InlineKeyboardButton(
            text=categorie[0],
            callback_data=categorie[1])
        )
    return builder.as_markup()

def createCustomKeyboard(buttons: list[Button]) -> InlineKeyboardMarkup|InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder() if inline else ReplyKeyboardBuilder()

    for buttonData in buttons:
        button = buttonData.create()
        keyboard.add(button)
    
    return keyboard.as_markup()