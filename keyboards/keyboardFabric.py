from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup

from .buttons import *
from starter import *

# NEED TO CHECK, MAYBE THIS FUNCTION IS NOT USED
def categories():
    builder = InlineKeyboardBuilder()
    for categorie in templates.categories:
        builder.add(types.InlineKeyboardButton(
            text=categorie[0],
            callback_data=categorie[1])
        )
    return builder.as_markup()

def createCustomInlineKeyboard(buttons: list[Button]) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for buttonData in buttons:
        button = buttonData.create()
        keyboard.row(button)
    
    return keyboard.as_markup()

def createCustomReplyKeyboard(buttons: list[Button]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    for buttonData in buttons:
        button = buttonData.create()
        keyboard.add(button)
    
    return keyboard.as_markup(resize_keyboard=True)

# Special cases
def createKeyboardWithBackButton(buttons: list[Button], backAction: str) -> InlineKeyboardMarkup:
    buttons.append(
        InlineButton('Назад', backAction)
    )
    return createCustomInlineKeyboard(buttons)

# def CreateBasketKeyboard
