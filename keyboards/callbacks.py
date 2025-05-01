from starter import *

from aiogram.utils.keyboard import InlineKeyboardMarkup, ReplyKeyboardBuilder, InlineKeyboardBuilder

from .buttons import *
import keyboards.buttons as button_types
import keyboards.keyboardFabric as keyboardFabric
import keyboards.messageGenerator as messageGenerator

from myUtils import Json
from myUtils.fastFunctions import text

# user functions
async def send_generated_message(callback):
    data = callback.data
    mg = messageGenerator.MessageGenerator(data)
    await callback.message.edit_text(
        mg.getText(),
        reply_markup = mg.getInlineKeyboard()
    )

# TODO: add generator like in 
# @dp.callback_query(F.data.in_(
#     [obj.name for obj in CRUD.for_model(Type).get(db_session)]
# ))
# but before - add all jsons to db
@dp.callback_query(F.data.in_([
    "categories", "new_devices",
    "used_devices", "beauty", "game_consoles",
    "accessories", "new_smartphones", "used_smartphones", 
]))
async def regenerate_button_callback(callback: types.CallbackQuery, state: FSMContext):
    await send_generated_message(callback)
    await state.clear()

@dp.callback_query(F.data == "main")
async def cmd_start(callback: types.CallbackQuery, state: FSMContext):
    try:
        message = callback.message
        dataset = Json.getMainDataset()

        # We are creating a new user if that not be was before
        user = CRUD.for_model(Users).get(db_session, user_id=message.from_user.id)
        if len(user) == 0:
            user = CRUD.for_model(Users).create(db_session, 
                username=message.from_user.username if message.from_user.username != None else " ", 
                user_id=message.from_user.id
            )
        else: user = user[0]
        
        # Creating /start menu
        buttons = [[]]
        for button_data in dataset["menu"]:
            if button_data[0] not in ['Корзина']:
                if len(buttons[-1]) < 2:
                    buttons[-1].append(button_types.KeyboardButtonRegular(button_data[0]))
                else:
                    buttons.append([button_types.KeyboardButtonRegular(button_data[0])])

        await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id    
        )
        await message.answer(
            text=dataset["message_texts"]["main"],
            reply_markup=keyboardFabric.createCustomReplyKeyboard(buttons)
        )
    except Exception as e:
        print(e)
        await callback.answer('Ошибка')

@dp.callback_query(F.data.in_(["database_change", "admin_menu_products"]))
async def check_for_admin(callback: types.CallbackQuery, state: FSMContext):
    user = CRUD.for_model(Users).get(db_session, user_id=callback.from_user.id)[0]
    if user.role < 1: await callback.message.delete()
    else: await send_generated_message(callback)

# TODO: 
def get_pagination_keyboard(page: int, type_id: int) -> InlineKeyboardMarkup:
    products = CRUD.for_model(Product).get(db_session, type_id=type_id)
    buttons = []
    for product in products:
        buttons.append(
            InlineButton(
                product.name, f"product__{product.id}"
            )
        )

    return keyboardFabric.createPaginationKeyboard(buttons, page)

# TODO
@dp.callback_query(F.data == "pagination_back")
async def pagination_back(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_data({
        "page": data["page"] - 1,
        "type_id": data["type_id"],
        "cd": data["cd"]
    })
    keyboard = get_pagination_keyboard(data["page"] - 1, data["type_id"])
    tg = messageGenerator.TextGenerator(data["cd"])
    await callback.message.edit_text(tg.getMessagePart(), reply_markup=keyboard)

# TODO
@dp.callback_query(F.data == "pagination_forward")
async def pagination_forward(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_data({
        "page": data["page"] + 1,
        "type_id": data["type_id"],
        "cd": data["cd"]
    })
    keyboard = get_pagination_keyboard(data["page"] + 1, data["type_id"])
    tg = messageGenerator.TextGenerator(data["cd"])
    await callback.message.edit_text(tg.getMessagePart(), reply_markup=keyboard)

# TODO
@dp.callback_query(F.data == "nothing")
async def Noting(callback: types.CallbackQuery, state: FSMContext):
    # just nothing
    pass

@dp.callback_query(F.data.in_(
    [obj.name for obj in CRUD.for_model(Type).get(db_session)]
))
async def product_type_handler(callback: types.CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        data = data.get("for_delete")
        for msg in data:
            await bot.delete_message(chat_id=msg[0], message_id=msg[1])
    except Exception as e:
        print(f"Error until atempt try delete: {e}")

    tg = messageGenerator.TextGenerator(callback.data)
    
    backAction = "pupupu"
    dataset = Json.getMainDataset()
    
    for key in dataset:
        try:
            value = dataset[key]
            actions = [v[1] for v in value]
            if callback.data in actions:
                backAction = key
                break
        except:
            pass

    # TODO: Change
    type_id = CRUD.for_model(Type).get(db_session, name=callback.data)[0].id
    keyboard = get_pagination_keyboard(0, type_id)

    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(tg.getMessagePart(), reply_markup=keyboard)
    else:
        await callback.message.edit_text(tg.getMessagePart(), reply_markup=keyboard)
    
    await state.clear()
    await state.set_data({
        "isBasket": False,
        "page": 0,
        "type_id": type_id,
        "cd": callback.data
    })

@dp.callback_query(F.data.startswith("product"))
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(callback.data.split("__")[1]))
    if product is None or (len(product) == 0): 
        callback.answer("Данная позиция уже выкуплена")
        if data.get("isBasket") == False:
            await cmd_start(callback, state)
        else:
            # TODO: delete all positions from basket with int(callback.data.split("__")[1]) == product.id
            await basket(callback, state)
        return
    product = product[0]
    # Список фотографий для отправки
    media = []
    for photo in product.photo:
        media.append(
            InputMediaPhoto(media=FSInputFile(f"{photo_path}/{photo}"))  # Используем FSInputFile для локальных файлов
        )

    if data.get("isBasket") == False:
        buttons = []
        maxQuantity = product.quantity
        await state.set_data({
            "productId": product.id,
            "currQuantity": 1,
            "maxQuantity": maxQuantity
        })
        keyboard = await keyboardFabric.createBeforeBasketKeyboard(state)
    else:
        basket_position = CRUD.for_model(Basket).get(db_session, user_id=callback.from_user.id, products_id=product.id)
        if basket_position is None  or (len(basket_position) == 0):
            callback.answer("Данная позиция уже выкуплена")
            # TODO: delete all positions from basket with int(callback.data.split("__")[1]) == product.id
            await basket(callback, state)
            return
        basket_position = basket_position[0]
        await state.set_data({
            "isBasket": True,
            "productId": product.id,
            "currQuantity": basket_position.quantity,
            "maxQuantity": product.quantity
        })
        keyboard = await keyboardFabric.createProductFromBasketKeyboard(state)
        # TODO: add this
        pass

    await callback.message.delete()
    sent_messages = await callback.message.answer_media_group(media=media)
    data = await state.get_data()
    data.update({"for_delete": [[msg.chat.id, msg.message_id] for msg in sent_messages]})
    await state.set_data(data)

    await callback.message.answer(
        "{}\n\n[Ссылка на товар]({})".format(text.insert_after_first_line(product.name, f"Цена: {product.price}₽"), await create_start_link(bot, str(product.id))),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.callback_query(
    F.data == "changeQuantity"
)
async def change_quantity(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    data = await state.get_data()
    await callback.message.answer("Введите новое кол-во товара\nМаксимум: {}".format(data["maxQuantity"]))
    await state.set_state(StatesForButtons.ready_to_enter_new_quantity)

@dp.callback_query(
    F.data == "add_to_basket"
)
async def add_to_basket(callback: types.CallbackQuery, state: FSMContext):
    user_id = callback.from_user.id
    try:
        data = await state.get_data()
        data = data.get("for_delete")
        for msg in data:
            await bot.delete_message(chat_id=msg[0], message_id=msg[1])
    except Exception as e:
        print(f"Error until atempt try delete: {e}")
    product_id = (await state.get_data())["productId"]
    quantity = (await state.get_data())["currQuantity"]
    basket = CRUD.for_model(Basket).get(db_session, user_id=user_id, products_id=product_id)
    if basket:
        basket = basket[0]
        CRUD.for_model(Basket).update(db_session, basket.id, quantity=quantity)
    else:
        CRUD.for_model(Basket).create(db_session, user_id=user_id, products_id=product_id, quantity=quantity)
    
    await callback.message.delete()
    await callback.message.answer("Товар успешно добавлен в корзину", reply_markup=await keyboardFabric.createAfterBasketKeyboard(state))

    await state.clear()


@dp.callback_query(
    F.data == "basket"
)
async def basket(callback: types.CallbackQuery, state: FSMContext):
    from myUtils.fastFunctions.buttons import show_basket
    await show_basket(user_id=callback.from_user.id, state=state, message=callback)

@dp.callback_query(F.data == "remove_from_basket")
async def remove_from_basket(callback: types.CallbackQuery, state: FSMContext):
    basket_position = CRUD.for_model(Basket).get(db_session, user_id=callback.from_user.id, products_id=(await state.get_data())["productId"])[0]
    CRUD.for_model(Basket).delete(db_session, basket_position.id)
    await basket(callback, state)

@dp.callback_query(F.data == "manager")
async def manager(callback: types.CallbackQuery, state: FSMContext):
    keyboard = InlineKeyboardBuilder()
    keyboard.row(InlineKeyboardButton(text="WhatsApp", url="https://wa.me/79887485869"))
    keyboard.row(InlineKeyboardButton(text="Telegram", url="https://t.me/jxc_kmp"))
    keyboard.row(InlineKeyboardButton(text="Связаться по номеру", callback_data="send_contact"))
    keyboard.row(InlineKeyboardButton(text="Назад", callback_data="main"))
    await bot.delete_message(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id    
        )
    await callback.message.answer(text="Выберете средство связи", reply_markup=keyboard.as_markup())

# admin functions
@dp.callback_query(F.data == "create_product")
async def create_product(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(StatesForCreate.product_name)
    await callback.answer("Идёт процесс создния товара...")
    progress_message = await callback.message.answer("...")
    current_message = await callback.message.answer("Введите название",
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            InlineButton("Отменить процесс", "cancel_task")
        ])
    )
    data = await state.get_data()
    data.update({
        'product_create_progress': progress_message, 'current_message': current_message
    })
    await state.set_data(data)

@dp.callback_query(F.data == "delete_message")
async def delete_message(callback: types.CallbackQuery):
    await callback.message.delete()

@dp.callback_query(F.data == "menu")
async def fucking_plug(callback: types.CallbackQuery):
    await callback.answer("Вы в самом начале")

@dp.callback_query(F.data == "register_basket")
async def register_basket(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.delete()
    current_message = await callback.message.answer("Введите ваше имя: как к вам обращаться?")
    data = await state.get_data()
    data.update({
        'current_message': current_message
    })
    await state.set_data(data)
    await state.set_state(StatesForRegBasket.name)

@dp.callback_query(F.data == "send_contact")
async def send_contact(callback: types.CallbackQuery):
    await callback.message.bot.send_contact(
        chat_id= callback.from_user.id,
        phone_number="+79887485869",
        first_name="Ilya",
        last_name="Nikitin"
    )

@callback_router.callback_query()
async def handle_unknown_callback(callback: types.CallbackQuery, state: FSMContext):

    try:
        data = await state.get_data()
        data = data.get("for_delete")
        for msg in data:
            await bot.delete_message(chat_id=msg[0], message_id=msg[1])
    except Exception as e:
        print(f"Error until atempt try delete: {e}")

    await callback.message.answer(
        text=f"⚠️ {callback.data.title()}\n Эта кнопка пока не работает.",
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            InlineButton(
                "Удалить сообщение 🗑",
                "delete_message"
    )]))
