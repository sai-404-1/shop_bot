from starter import *

product_create_states = [
    StatesForCreate.product_name,
    StatesForCreate.product_description,
    StatesForCreate.product_price,
    StatesForCreate.product_type,
    StatesForCreate.product_photo,
    # StatesForCreate.product_quantity,
    # StatesForCreate.count ?
]

product_template = [
    ["Название", "product_name"],
    ["Описание", "product_description"],
    ["Цена", "product_price"],
    ["Тип", "product_type"],
    ["Фотография", "product_photo"]
]

async def create_progress_message(data):
    result = ""
    for step in product_template:
        result += f"{step[0]}: {'❌' if data.get(step[1]) == None else data.get(step[1])}\n"
    return result

@fsm_router.message(StatesForCreate.product_name)
async def message_try(message: Message, state: FSMContext):
    data = await state.get_data()
    await data.get('current_message').delete()
    current_message = await message.answer('Теперь описание')
    data.update(
        {'product_name': message.text, 'current_message': current_message}
    )
    await state.set_data(data)
    await state.set_state(StatesForCreate.product_description)
    await data['product_create_progress'].edit_text(await create_progress_message(data))
    await message.delete()

@fsm_router.message(StatesForCreate.product_description)
async def message_try(message: Message, state: FSMContext):
    data = await state.get_data()
    await data.get('current_message').delete()
    current_message = await message.answer('Теперь цена')
    data.update(
        {'product_description': message.text, 'current_message': current_message}
    )
    await state.set_data(data)
    await state.set_state(StatesForCreate.product_price)
    await data['product_create_progress'].edit_text(await create_progress_message(data))
    await message.delete()

@fsm_router.message(StatesForCreate.product_price)
async def message_try(message: Message, state: FSMContext):
    data = await state.get_data()
    await data.get('current_message').delete()
    current_message = await message.answer('Теперь тип товара',
        reply_markup=keyboardFabric.createCustomInlineKeyboard(
            keyboardFabric.InlineButton(type.name, f"{type.name}_create_product") for type in CRUD.for_model(Type).all(db_session)
    ))
    data.update(
        {'product_price': message.text, 'current_message': current_message}
    )
    await state.set_data(data)
    await state.set_state(StatesForCreate.product_type)
    await data['product_create_progress'].edit_text(await create_progress_message(data))
    await message.delete()

@fsm_router.callback_query(F.data.in_([f"{type.name}_create_product" for type in CRUD.for_model(Type).all(db_session)]))
async def message_try(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await data.get('current_message').delete()
    current_message = await callback.message.answer('Теперь отправьте фотографию товара')
    data.update(
        {'product_type': callback.data.replace('_create_product', ''), 'current_message': current_message}
    )
    await state.set_data(data)
    await state.set_state(StatesForCreate.product_photo)
    await data['product_create_progress'].edit_text(await create_progress_message(data))

@fsm_router.message(StatesForCreate.product_photo)
async def message_try(message: Message, state: FSMContext, bot: Bot):
    data = await state.get_data()

    data.update({'product_photo': "Скачиваю..."})
    await data['product_create_progress'].edit_text(await create_progress_message(data))
    await data.get('current_message').delete()
    
    file_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    await bot.download_file(
        file_path=file.file_path,
        destination=f"src/photo/{file_id}.jpg"
    )
    data.update({'product_photo': f"{file_id[:10]}..."})
    await data['product_create_progress'].edit_text(await create_progress_message(data))

    CRUD.for_model(Product).create(
        db_session,
        name=data.get(product_template[0][1]),
        description=data.get(product_template[1][1]),
        photo=f"{file_id}.jpg",
        price=data.get(product_template[2][1]),
        type_id=\
        CRUD.for_model(Type).get(db_session, name=data.get(product_template[3][1]))[0].id
    )
    
    await data['product_create_progress'].edit_text(
        f'Товар с названием "{data.get(product_template[0][1])}" в категории {data.get(product_template[3][1])} создан!'
    )
    await state.clear()
    await message.delete()