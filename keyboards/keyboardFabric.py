from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from manager.fsm.fsm_class import StatesForButtons

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

async def createBeforeBasketKeyboard(state: FSMContext) -> InlineKeyboardMarkup:
    data = await state.get_data()
    print(data)
    buttons = []
    buttons.append(InlineButton("Добавить в корзину", "add_to_basket"))
    # типа обработка fsm (какое-то значение поставить в id товара)
    if(data["maxQuantity"] > 1):
        #     # типа fsm с кол-вом
        currQuantity = data['currQuantity']
        print(f"CURRENT QUANTITY: {currQuantity}")
        buttons.append(InlineButton(f"Количество: {currQuantity}", "changeQuantity"))
    
    product = CRUD.for_model(Product).get(db_session, id=int(data["productId"]))[0]
    typeId = product.type_id
    productType = CRUD.for_model(Type).get(db_session, id=typeId)[0]
    backAction = productType.name
    print(f"BACK ACTION: {backAction}")

    return createKeyboardWithBackButton(buttons, backAction)

async def createAfterBasketKeyboard(state: FSMContext) -> InlineKeyboardMarkup:
    data = await state.get_data()
    buttons = []
    buttons.append(InlineButton("В корзину", "basket"))
    buttons.append(InlineButton("В меню", "menu"))

    # еще немного копипасты
    product = CRUD.for_model(Product).get(db_session, id=int(data["productId"]))[0]
    typeId = product.type_id
    productType = CRUD.for_model(Type).get(db_session, id=typeId)[0]
    backAction = productType.name
    
    return createKeyboardWithBackButton(buttons, backAction)