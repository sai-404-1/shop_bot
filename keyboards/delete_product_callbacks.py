from starter import *
from keyboards.keyboardFabric import *
from .callbacks import get_pagination_keyboard

@dp.callback_query(F.data == "delete_product")
async def change_products(callback: types.CallbackQuery, state: FSMContext):

    product_exist_type_id = [product.type_id for product in CRUD.for_model(Product).all(db_session)]
    types = CRUD.for_model(Type).all(db_session)

    not_sorted = []
    for type in types:
        if type.id in product_exist_type_id:
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
            InlineButton(text=f"{type.title}", callback_data=f"deleteProductWithType__{type.id}__{type.name}") for type in sorted_array
        ], "admin_menu_products"))
    
@dp.callback_query(F.data.startswith('deleteProductWithType'))
async def delete_product_with_type(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('__')
    type = CRUD.for_model(Type).get(db_session, id=int(data[1]))[0]
    await state.set_data({
        "isBasket": False,
        "page": 0,
        "type_id": type.id,
        "cd": callback.data,
        "pagination_template": "deleteProduct__",
    })
    keyboard = get_pagination_keyboard(0, type.id, "deleteProduct__")
    CRUD.for_model(Type).update(db_session, model_id=type.id, rate=type.rate+1)
    await callback.message.edit_text(
        text=f"Выберите продукт из категории {type.title} <b>для удаления</b>",
        reply_markup=keyboard,
        parse_mode='HTML'
    )

@dp.callback_query(F.data.startswith('deleteProduct'))
async def change_product(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('__')
    product = CRUD.for_model(Product).get(db_session, id=data[1])[0]

    await callback.message.edit_text(
        text=f'Подтвердите удаление продукта <a href="{await create_start_link(bot, str(product.id))}">{product.name}</a>',
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            InlineButton(text="Удалить", callback_data=f"confirmDeleteProduct__{product.id}"),
        ]),
        parse_mode="HTML"
    )

@dp.callback_query(F.data.startswith('confirmDeleteProduct'))
async def delete_product(callback: types.CallbackQuery, state: FSMContext):
    data = callback.data.split('__')
    product = CRUD.for_model(Product).get(db_session, id = data[1])[0]
    CRUD.for_model(Product).delete(db_session, model_id=data[1])
    await callback.message.edit_text(
        text=f'Продукт "{product.name}" был удалён',
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            InlineButton(text="Вернуться к базе", callback_data=f"database_change"),
        ]),
        parse_mode="HTML"
    )
