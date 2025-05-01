from starter import *
from .buttons import *
import keyboards.keyboardFabric as keyboardFabric
from .callbacks import get_pagination_keyboard

@dp.callback_query(F.data == "change_products")
async def change_products(callback: types.CallbackQuery, state: FSMContext):

    product_exist_type_id = [product.type_id for product in CRUD.for_model(Product).all(db_session)]
    types = CRUD.for_model(Type).all(db_session)

    not_sorted = []
    for type in types:
        if type.id in product_exist_type_id:
            print(type.title)
            not_sorted.append(type)

    sorted_array = sorted(not_sorted, key=lambda x: x.rate, reverse=True)
    await state.set_data({
        "isBasket": False,
        "page": 0,
        "type_id": type.id,
        "cd": callback.data,
        "pagination_template": "changeProductWithType__",
    })
    await callback.message.edit_text(
        text="Выберите тип товара (перечислены в соответствии с частотой использования и существующими товарами)",
        reply_markup=keyboardFabric.createKeyboardWithBackButton([
            InlineButton(text=f"{type.title}", callback_data=f"changeProductWithType__{type.id}") for type in sorted_array
        ], "admin_menu_products"))


@dp.callback_query(F.data.startswith('changeProductWithType'))
async def change_product_with_type(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('__')
    type = CRUD.for_model(Type).get(db_session, id=int(data[1]))[0]
    CRUD.for_model(Type).update(db_session, model_id=type.id, rate=type.rate+1)
    keyboard = get_pagination_keyboard(0, type.id, "changeProduct__")
    await callback.message.edit_text(
        text=f"Выберите продукт из категории {type.name}",
        reply_markup=keyboard
    )

@dp.callback_query(F.data.startswith('changeProduct'))
async def change_product(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('__')
    product = CRUD.for_model(Product).get(db_session, id=data[1])[0]

    data = await state.get_data()
    data.update(
        {"current_changed_product_id": product.id}
    )
    await state.set_data(data)

    await callback.message.edit_text(
        text=f"Выберите параметр продукта <code>{product.name}</code>",
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            InlineButton(text="Название", callback_data=f"changeNameProduct__{product.id}"),
            # InlineButton(text="Описание", callback_data=f"changeDescriptionProduct__{product.id}"),
            InlineButton(text="Цена", callback_data=f"changePriceProduct__{product.id}"),
            InlineButton(text="Тип", callback_data=f"changeTypeProduct__{product.id}"),
            InlineButton(text="Фотография", callback_data=f"changePhotoProduct__{product.id}"),
            InlineButton(text="Назад", callback_data="admin_menu_products")
        ]),
        parse_mode="HTML"
    )

# Дописать функцию обработки параметра, который будет изменяться  
@dp.callback_query(F.data.startswith('change'))
async def change_product(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('__')
    print(data)
    if "name" in data[0].lower():
        await state.set_state(StatesForUpdate.product_name)
        await callback.message.answer(
            text="Введите новое название для продукта",
            reply_markup=keyboardFabric.createCustomInlineKeyboard([
                InlineButton(text="Отменить действие", callback_data="cancel_task")
            ]),
        )

    # elif "description" in data[0].lower():
    #     await state.set_state(StatesForUpdate.product_description)
    #     await callback.message.answer(
    #         text="Введите новое описание для продукта",
    #         reply_markup=keyboardFabric.createCustomInlineKeyboard([
    #             InlineButton(text="Отменить действие", callback_data="cancel_task")
    #         ]),
    #     )

    elif "price" in data[0].lower():
        await state.set_state(StatesForUpdate.product_description)
        await callback.message.answer(
            text="Введите новую цену для продукта",
            reply_markup=keyboardFabric.createCustomInlineKeyboard([
                InlineButton(text="Отменить действие", callback_data="cancel_task")
            ]),
        )

    elif "type" in data[0].lower():
        await state.set_state(StatesForUpdate.product_type)
        not_sorted = CRUD.for_model(Type).all(db_session)
        sorted_array = sorted(not_sorted, key=lambda x: x.rate, reverse=True)
        await callback.message.answer(
            text="Введите новый тип для продукта",
            reply_markup=keyboardFabric.createCustomInlineKeyboard(
                keyboardFabric.InlineButton(type.name, f"typeUpdate__{type.id}") for type in sorted_array
            )
        )

    elif "photo" in data[0].lower():
        await state.set_state(StatesForUpdate.product_photo)
        await callback.message.answer(
            text="Отправьте новую фотографию для продукта",
            reply_markup=keyboardFabric.createCustomInlineKeyboard([
                InlineButton(text="Отменить действие", callback_data="cancel_task")
            ]),
        )


@dp.callback_query(F.data == "cancel_task")
async def cancel_task(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer('Действие отменено.')
    data = await state.get_data()
    await data["product_create_progress"].delete()
    await callback.message.delete()
    await state.clear()