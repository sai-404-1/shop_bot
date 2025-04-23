from starter import *

from aiogram.utils.keyboard import InlineKeyboardMarkup

from .buttons import *
import keyboards.keyboardFabric as keyboardFabric
import keyboards.messageGenerator as messageGenerator

from myUtils import Json

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
        dataset = Json.getMainDataset()
        message = callback.message
        await state.clear()

        # We are creating a new user if that not be was before
        user = CRUD.for_model(Users).get(db_session, user_id=message.from_user.id)
        if len(user) == 0:
            user = CRUD.for_model(Users).create(db_session, 
                username=message.from_user.username, 
                user_id=message.from_user.id
            )
        else: user = user[0]
        
        # Creating /start menu
        buttons = []
        for button_data in dataset["main"] if user.role >= 1 else dataset["main"][:2]:
            buttons.append(KeyboardButtonRegular(button_data[0]))

        await message.edit_text(
            text=dataset["message_texts"]["main"],
            reply_markup=keyboardFabric.createCustomReplyKeyboard(buttons)
        )
    except:
        await callback.answer('Ошибка')

@dp.callback_query(F.data.in_(["database_change", "admin_menu_products"]))
async def check_for_admin(callback: types.CallbackQuery, state: FSMContext):
    user = CRUD.for_model(Users).get(db_session, user_id=callback.from_user.id)[0]
    if user.role < 1: await callback.message.delete()
    else: await send_generated_message(callback)

@dp.callback_query(F.data.in_(
    [obj.name for obj in CRUD.for_model(Type).get(db_session)]
))
async def product_type_handler(callback: types.CallbackQuery, state: FSMContext):
    type_id = CRUD.for_model(Type).get(db_session, name=callback.data)[0].id
    products = CRUD.for_model(Product).get(db_session, type_id=type_id)
    buttons = []
    tg = messageGenerator.TextGenerator(callback.data)

    for product in products:
        buttons.append(InlineButton(product.name, f"product__{product.id}"))
    
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

    # print(backAction)

    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(tg.getMessagePart(), reply_markup=keyboardFabric.createKeyboardWithBackButton(buttons, backAction))
    else:
        await callback.message.edit_text(tg.getMessagePart(), reply_markup=keyboardFabric.createKeyboardWithBackButton(buttons, backAction))
    
    await state.clear()
    await state.set_data({
        "isBasket": False
    })

@dp.callback_query(F.data.startswith("product"))
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    #-------------------------------------------UPDATE START----------------------------------------------
    product = CRUD.for_model(Product).get(db_session, id=int(callback.data.split("__")[1]))[0]
    # TODO: add condition (if product is empty())
    # Need updates
    print(product.name)
    print(product.id)
    print(product.description)
    if empty(product): 
        callback.answer("Данная позиция уже выкуплена")
        if data.get("isBasket") == False:
            await cmd_start(callback, state)
        else:
            # TODO: delete all positions from basket with int(callback.data.split("__")[1]) == product.id
            await basket(callback, state)
        return
    #-------------------------------------------UPDATE END----------------------------------------------
    product = product[0]
    photo = types.FSInputFile(f"{photo_path}/{product.photo}")

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
        #-------------------------------------------UPDATE START----------------------------------------------
        basket_position = CRUD.for_model(Basket).get(db_session, user_id=callback.from_user.id, products_id=product.id)
        # TODO: add condition (if basket_position is empty())
        # Need updates
        if empty(basket_position):
            callback.answer("Данная позиция уже выкуплена")
            # TODO: delete all positions from basket with int(callback.data.split("__")[1]) == product.id
            await basket(callback, state)
            return
        basket_position = basket_position[0]
        #-------------------------------------------UPDATE END----------------------------------------------
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
    await callback.message.answer_photo(
        types.FSInputFile(
            f"{photo_path}/{product.photo}"
        ),
        caption="{}\n\n{}\n\n[Ссылка на товар]({})".format(product.name, product.price, await create_start_link(bot, str(product.id))),
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
    chat = CRUD.for_model(Communication).get(db_session, user_id=callback.from_user.id)
    if len(chat) == 0:
        CRUD.for_model(Communication).create(db_session, user_id=callback.from_user.id)
        chat = CRUD.for_model(Communication).get(db_session, user_id=callback.from_user.id)
    chat = chat[0]
    await callback.message.edit_text(
        "Вы перешли в чат с поддержкой.\nПожалуйста, опишите ваш вопрос и ожидайте ответа", 
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            InlineButton(
                "Отменить",
                "delete_message"
    )]))
    await state.set_state(StatesForManager.userCommunicate)

async def sendLastMessages(callback: types.CallbackQuery, messages: list, amount: int = 20) -> None:
    if amount > len(messages):
        amount = len(messages)
    messages = messages[-amount:]
    for message in messages:
        await callback.message.answer(
            "{}:\n{}".format(message[0], message[1])
        )

# for admins
@dp.callback_query(F.data.contains("//support//"))
async def support(callback: types.CallbackQuery, state: FSMContext):
    import json
    user_id = int(callback.data.split("//support//")[1])
    chat = CRUD.for_model(Communication).get(db_session, user_id=user_id)[0]
    CRUD.for_model(Communication).update(db_session, chat.id, readed=True)
    await sendLastMessages(callback, json.loads(chat.messages), amount=1)
    await callback.message.answer(
        "Вы перешли в чат с пользователем {}.\nОтправьте ответ на его вопрос".format(user_id),
        reply_markup=keyboardFabric.createKeyboardWithBackButton(
            [InlineButton("Последние 20 сообщений", "history")], "main"
        )
    )
    await state.set_state(StatesForManager.managerCommunicate)
    await state.set_data({
        "userId": user_id,
    })

# for users
@dp.callback_query(F.data.contains("//help//"))
async def help(callback: types.CallbackQuery,state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "Вы перешли в чат с поддержкой.\nЕсли у вас остались вопросы - задайте их", 
        reply_markup=keyboardFabric.createKeyboardWithBackButton(
            [InlineButton("Последние 20 сообщений", "history")], "main"
        )
    )
    await state.set_data({
        "userId": callback.from_user.id
    })
    await state.set_state(StatesForManager.userCommunicate)
    print(callback.data)

@dp.callback_query(F.data == "history")
async def history(callback: types.CallbackQuery, state: FSMContext):
    import json
    user_id = (await state.get_data())["userId"]
    chat = CRUD.for_model(Communication).get(db_session, user_id=user_id)[0]
    await sendLastMessages(callback, json.loads(chat.messages))

# admin functions
def get_pagination_keyboard(page: int) -> InlineKeyboardMarkup:
    chats = CRUD.for_model(Communication).get(db_session)
    chats = sorted(chats, key=lambda chat: chat.readed)
    buttons = []
    for chat in chats:
        buttons.append(
            InlineButton(
                text="{} - {}".format(chat.user_id, '✅' if chat.readed else '❌'),
                callback_data="//support//{}".format(chat.user_id)
            )
        )
    return keyboardFabric.createPaginationKeyboard(buttons, page)

# admin functions
@dp.callback_query(F.data == "list_of_requests_help") 
async def list_of_requests_help(callback: types.CallbackQuery, state: FSMContext):
    await state.set_data({
        "page": 0,
    })
    keyboard = get_pagination_keyboard(0)
    await callback.message.edit_text("Список чатов", reply_markup=keyboard)

@dp.callback_query(F.data == "pagination_back")
async def pagination_back(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_data({
        "page": data["page"] - 1
    })
    keyboard = get_pagination_keyboard(data["page"] - 1)
    await callback.message.edit_text("Список чатов", reply_markup=keyboard)

@dp.callback_query(F.data == "pagination_forward")
async def pagination_forward(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await state.set_data({
        "page": data["page"] + 1
    })
    keyboard = get_pagination_keyboard(data["page"] + 1)
    await callback.message.edit_text("Список чатов", reply_markup=keyboard)

@dp.callback_query(F.data == "nothing")
async def Noting(callback: types.CallbackQuery, state: FSMContext):
    # just nothing
    pass

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

@callback_router.callback_query()
async def handle_unknown_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        text=f"⚠️ {callback.data.title()}\n Эта кнопка пока не работает.",
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            InlineButton(
                "Удалить сообщение 🗑",
                "delete_message"
    )]))