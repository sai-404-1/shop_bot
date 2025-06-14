from starter import *

@fsm_router.message(StatesForUpdate.product_name)
async def name_update_product(message: Message, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
    CRUD.for_model(Product).update(db_session, model_id=product.id, name=message.text)
    await message.answer(await get_message(product), parse_mode="HTML")
    await state.clear()

# @fsm_router.message(StatesForUpdate.product_description)
# async def name_update_product(message: Message, state: FSMContext):
#     data = await state.get_data()
#     product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
#     CRUD.for_model(Product).update(db_session, model_id=product.id, description=message.text)
#     await message.answer(await get_message(product), parse_mode="HTML")
#     await state.clear()

@fsm_router.message(StatesForUpdate.product_price)
async def name_update_product(message: Message, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
    CRUD.for_model(Product).update(db_session, model_id=product.id, price=int(message.text))
    await message.answer(await get_message(product), parse_mode="HTML")
    await state.clear()

@fsm_router.message(StatesForUpdate.product_type)
async def type_update_product(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
    type_id = int(callback.data.split('__')[1])
    CRUD.for_model(Product).update(db_session, model_id=product.id, type_id=type_id)
    type = CRUD.for_model(Type).get(db_session, id=type_id)[0]
    CRUD.for_model(Type).update(db_session, model_id=type.id, rate=type.rate+1)
    await callback.message.answer(await get_message(product), parse_mode="HTML")
    await state.clear()

@dp.callback_query(F.data.startswith('changedPhotoProduct'))
async def photo_update_product(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    data.update({"choice_photo_number": int(callback.data.split("__")[1]) - 1})
    await state.set_data(data)
    await state.set_state(StatesForUpdate.single_photo_handler)
    await callback.message.edit_text("Отправьте новую фотографию для продукта")

@fsm_router.message(StatesForUpdate.single_photo_handler)
async def photo_update_product(message: Message, state: FSMContext):
    data = await state.get_data()

    product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
    current_message = await message.answer('Скачиваю...')
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await bot.download_file(
        file_path=file.file_path,
        destination=f"src/photo/{file_id}.jpg"
    )

    if data.get("choice_photo_number") != None:
        product.photo[data["choice_photo_number"]] = f"{file_id}.jpg"
    else:
        product.photo[0] = f"{file_id}.jpg"

    await current_message.edit_text(f"Файл: {file_id[:10]}...")

    CRUD.for_model(Product).delete(db_session, model_id=product.id)
    CRUD.for_model(Product).create(
        db_session,
        id=product.id,
        name=product.name,
        description=product.description,
        photo=product.photo,
        price=product.price,
        type_id=product.type_id,
        quantity=product.quantity
    )    
    await message.answer(await get_message(product), parse_mode="HTML")
    await current_message.delete()
    await state.clear()



@fsm_router.callback_query(F.data.startswith('typeUpdate'))
async def message_try(callback: types.CallbackQuery, state: FSMContext):
    callback.data = callback.data.split('__')
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=int(data.get('current_changed_product_id')))[0]
    CRUD.for_model(Product).update(db_session, model_id=product.id, type_id=callback.data[1])
    await callback.message.answer(await get_message(product), parse_mode="HTML")
    await state.clear()

async def get_message(product):
    type = CRUD.for_model(Type).get(db_session, id=product.type_id)[0]
    return f'Продукт типа <b>"{type.title}"</b>, <b>"{product.name}"</b> был <a href="{await create_start_link(bot, str(product.id))}">обновлён</a>'