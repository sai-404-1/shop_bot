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
    # ["Описание", "product_description"],
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
    current_message = await message.answer('Теперь цена',
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            keyboardFabric.InlineButton("Отменить процесс", "cancel_task")
    ]))
    data.update(
        {'product_name': message.text, 'current_message': current_message}
    )
    await state.set_data(data)
    await state.set_state(StatesForCreate.product_price)
    await data['product_create_progress'].edit_text(await create_progress_message(data))
    await message.delete()

@fsm_router.message(StatesForCreate.product_price)
async def message_try(message: Message, state: FSMContext):
    data = await state.get_data()
    await data.get('current_message').delete()
    not_sorted = CRUD.for_model(Type).all(db_session)
    sorted_array = sorted(not_sorted, key=lambda x: x.rate, reverse=True)
    current_message = await message.answer('Теперь тип товара',
        reply_markup=keyboardFabric.createCustomInlineKeyboard(
            keyboardFabric.InlineButton(type.title, f"{type.name}_create_product") for type in sorted_array
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
    current_message = await callback.message.answer('Теперь отправьте фотографию товара',
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            keyboardFabric.InlineButton("Отменить процесс", "cancel_task")
    ]))
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

    product = CRUD.for_model(Product).create(
        db_session,
        name=data.get("product_name"),
        description="",
        photo=f"{file_id}.jpg",
        price=data.get("product_price"),
        type_id=\
        CRUD.for_model(Type).get(db_session, name=data.get("product_type"))[0].id
    )
    
    await data['product_create_progress'].edit_text(
        f'Товар с названием "{data.get("product_name")}" в категории {data.get("product_type")} создан!\nСсылка на товар: {await create_start_link(bot, str(product.id))}',
        reply_markup=keyboardFabric.createCustomInlineKeyboard([
            keyboardFabric.InlineButton(
                "Удалить сообщение 🗑",
                "delete_message"
    )]))
    await state.clear()
    await message.delete()