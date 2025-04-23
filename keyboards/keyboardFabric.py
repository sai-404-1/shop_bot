from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, InlineKeyboardMarkup
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardMarkup
from manager.fsm.fsm_class import StatesForButtons

from .buttons import *
from starter import *

# NEED TO CHECK, MAYBE THIS FUNCTION IS NOT USED
# i think, about that's realy doesn't used anywhere
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
    # print(keyboard)
    return keyboard.as_markup()

def createCustomReplyKeyboard(buttons: list[list[Button]]) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    for row in buttons:
        for button_data in row:
            button = button_data.create()
            keyboard.add(button)
        keyboard.adjust(2)  # По 2 кнопки в ряду
    
    return keyboard.as_markup(resize_keyboard=True)

# Special cases
def createKeyboardWithBackButton(buttons: list[Button], backAction: str) -> InlineKeyboardMarkup:
    buttons.append(
        InlineButton('Назад', backAction)
    )
    return createCustomInlineKeyboard(buttons)

async def createBeforeBasketKeyboard(state: FSMContext) -> InlineKeyboardMarkup:
    data = await state.get_data()
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

async def createProductFromBasketKeyboard(state: FSMContext) -> InlineKeyboardMarkup:
    data = await state.get_data()
    buttons = []
    buttons.append(InlineButton("Удалить из корзины", "remove_from_basket"))
    currQuantity = data['currQuantity']
    print(f"CURRENT QUANTITY: {currQuantity}")
    buttons.append(InlineButton(f"Количество: {currQuantity}", "changeQuantity"))
    return createKeyboardWithBackButton(buttons, "basket")    

def get_page(arr: list, page: int, page_size: int) -> list:
    if len(arr) < page * page_size: return []
    if len(arr) < (page + 1) * page_size: return arr[page * page_size:]
    return arr[page * page_size: (page + 1) * page_size]

def createPaginationKeyboard(items: list[InlineButton], page: int, page_size: int = 10) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    items_size = len(items)
    items = get_page(items, page, page_size)
    for item in items:
        keyboard.row(item.create())
    last_row = []
    if page != 0: last_row.append(InlineButton("<-", "pagination_back").create())
    last_row.append(InlineButton(f"{page + 1}", "nothing").create())
    if items_size > page_size * (page + 1): last_row.append(InlineButton("->", "pagination_forward").create())
    keyboard.row(*last_row)
    keyboard.row(InlineButton("Меню", "main").create())
    return keyboard.as_markup()
