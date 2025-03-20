from starter import *

@fsm_router.message(StatesForUpdate.product_name)
async def name_update_product(message: Message, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
    CRUD.for_model(Product).update(db_session, model_id=product.id, name=message.text)
    await message.answer(get_message(product), parse_mode="HTML")
    await state.clear()

@fsm_router.message(StatesForUpdate.product_description)
async def name_update_product(message: Message, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
    CRUD.for_model(Product).update(db_session, model_id=product.id, description=message.text)
    await message.answer(get_message(product), parse_mode="HTML")
    await state.clear()

@fsm_router.message(StatesForUpdate.product_price)
async def name_update_product(message: Message, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
    CRUD.for_model(Product).update(db_session, model_id=product.id, price=int(message.text))
    await message.answer(get_message(product), parse_mode="HTML")
    await state.clear()

@fsm_router.callback_query(F.data.startswith('typeUpdate'))
async def message_try(callback: types.CallbackQuery, state: FSMContext):
    callback.data = callback.data.split('__')
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
    CRUD.for_model(Product).update(db_session, model_id=product.id, type_id=callback.data[1])
    await callback.message.answer(get_message(product), parse_mode="HTML")
    await state.clear()

async def get_message(product):
    type = CRUD.for_model(Type).get(db_session, id=product.type_id)[0]
    return f'Продукт типа <b>"{type.title}"</b>, <b>"{product.name}"</b> был <a href="{await create_start_link(bot, str(product.id))}">обновлён</a>'