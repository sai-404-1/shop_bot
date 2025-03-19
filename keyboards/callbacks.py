from starter import *

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
    "main", "categories", "menu", "new_devices",
    "used_devices", "beauty", "game_consoles",
    "accessories", "new_smartphones", "used_smartphones", 
    "database_change", "admin_menu_products"
]))
async def regenerate_button_callback(callback: types.CallbackQuery, state: FSMContext):
    await send_generated_message(callback)

@dp.callback_query(F.data.in_(
    [obj.name for obj in CRUD.for_model(Type).get(db_session)]
))
async def product_type_handler(callback: types.CallbackQuery, state: FSMContext):
    type_id = CRUD.for_model(Type).get(db_session, name=callback.data)[0].id
    phones = CRUD.for_model(Product).get(db_session, type_id=type_id)
    buttons = []
    tg = messageGenerator.TextGenerator(callback.data)

    for phone in phones:
        buttons.append(InlineButton(phone.name, str(phone.id)))
    
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

    print(backAction)

    if callback.message.photo:
        await callback.message.delete()
        await callback.message.answer(tg.getMessagePart(), reply_markup=keyboardFabric.createKeyboardWithBackButton(buttons, backAction))
    else:
        await callback.message.edit_text(tg.getMessagePart(), reply_markup=keyboardFabric.createKeyboardWithBackButton(buttons, backAction))
    
    await state.clear()
    await state.set_data({
        "isBasket": False
    })

@dp.callback_query(F.data.in_([
    str(product.id) for product in CRUD.for_model(Product).all(db_session)
]))
async def process_callback(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(callback.data))[0]
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
        basket_position = CRUD.for_model(Basket).get(db_session, user_id=callback.from_user.id, products_id=product.id)[0]
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
        caption="{}\n\n{}\n\n{}\n\n[Ссылка на товар]({})".format(product.name, product.description, product.price, await create_start_link(bot, str(product.id))),
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

# TODO: change message + keyboard to show that like in /idk
@dp.callback_query(
    F.data == "basket"
)
async def basket(callback: types.CallbackQuery, state: FSMContext):
    basket = CRUD.for_model(Basket).get(db_session, user_id=callback.from_user.id)
    buttons = []
    text = ""
    for basket_position in basket:
        product = CRUD.for_model(Product).get(db_session, id=basket_position.products_id)[0]
        quantity = basket_position.quantity
        buttons.append(
            InlineButton(
                product.name, 
                str(product.id)
            )
        )
        text += f"Товар: {product.name} \nКол-во: {quantity}\n\n"
    await state.set_data({
        "isBasket": True,
    })
    keyboard = keyboardFabric.createKeyboardWithBackButton(buttons, "menu")
    await callback.message.delete()
    await callback.message.answer("Ваша корзина:\n\n"+text, reply_markup=keyboard)
    
@dp.message(Command("idk"))
async def handler_idk(message: Message):
    text = "Ваша корзина\n<code>(товар / кол-во)</code>"
    await message.answer(
        text=text,
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            InlineButton(text=f"Назание – {i+1}", callback_data="123") for i in range(5)
        ]),
        parse_mode='HTML'
    )

@dp.callback_query(F.data == "remove_from_basket")
async def remove_from_basket(callback: types.CallbackQuery, state: FSMContext):
    basket_position = CRUD.for_model(Basket).get(db_session, user_id=callback.from_user.id, products_id=(await state.get_data())["productId"])[0]
    CRUD.for_model(Basket).delete(db_session, basket_position.id)
    await basket(callback, state)

# admin functions
@dp.callback_query(F.data == "create_product")
async def create_product(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(StatesForCreate.product_name)
    await callback.answer("Идёт процесс создния товара...")
    current_message = await callback.message.answer("Введите название")
    progress_message = await callback.message.answer("...")
    data = await state.get_data()
    data.update({
        'product_create_progress': progress_message, 'current_message': current_message
    })
    await state.set_data(data)

@dp.callback_query(F.data == "delete_message")
async def delete_message(callback: types.CallbackQuery):
    await callback.message.delete()

@callback_router.callback_query()
async def handle_unknown_callback(callback: types.CallbackQuery):
    await callback.message.answer(
        text=f"⚠️ {callback.data.title()}\n Эта кнопка пока не работает.",
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            InlineButton(
                "Удалить сообщение 🗑",
                "delete_message"
    )]))