from starter import *

product_create_states = [
    StatesForRegBasket.name,
    StatesForRegBasket.phone_number,
]

product_template = [
    ["Имя", "name"],
    ["Номер телефона", "phone_number"]
]

@fsm_router.message(StatesForRegBasket.name)
async def message_try(message: Message, state: FSMContext):
    data = await state.get_data()
    await data.get('current_message').delete()
    # current_message = await message.answer('Теперь, введите ваш <b>номер телефона</b>. Он поможет нам связаться с вами',
    #     reply_markup=keyboardFabric.createCustomInlineKeyboard([
    #         keyboardFabric.InlineButton("Отменить процесс", "cancel_task")
    # ]),
    # parse_mode='HTML')
    current_message = await message.answer('Теперь, отправьте ваш <b>номер телефона</b>. Он поможет нам связаться с вами',
        reply_markup = keyboardFabric.ReplyKeyboardMarkup(
            keyboard=[[keyboardFabric.KeyboardButton(
                text="Отправить номер телефона ☎️", 
                request_contact=True
            )]],
            resize_keyboard=True
        ),
        parse_mode='HTML'
    )
    # await current_message.edit_reply_markup(
    #     inline_message_id=current_message.message_id,
    #     reply_markup=keyboardFabric.createCustomInlineKeyboard([
    #         keyboardFabric.InlineButton("Отменить процесс", "cancel_task")
    #     ])
    # )
    data.update(
        {'name': message.text, 'current_message': current_message}
    )
    await state.set_data(data)
    await state.set_state(StatesForRegBasket.phone_number)
    await message.delete()

@fsm_router.message(StatesForRegBasket.phone_number)
async def message_try(message: Message, state: FSMContext):
    data = await state.get_data()
    await data.get('current_message').delete()
    basket = CRUD.for_model(Basket).get(db_session, user_id=message.from_user.id)
    await message.delete()
    
    import keyboards.buttons as button_types
    import myUtils.Json as Json
    buttons = [[]]
    dataset = Json.getMainDataset()
    for button_data in dataset["menu"]:
        if button_data[0] not in ['Корзина']:
            if len(buttons[-1]) < 2:
                buttons[-1].append(button_types.KeyboardButtonRegular(button_data[0]))
            else:
                buttons.append([button_types.KeyboardButtonRegular(button_data[0])])
    
    text = ""
    for basket_position in basket:
        product = CRUD.for_model(Product).get(db_session, id=basket_position.products_id)[0]
        quantity = basket_position.quantity
        text += f'<a href="{await create_start_link(bot, str(product.id))}">{product.name}</a> \nКол-во: {quantity}\n\n'

    await bot.send_message(
        # chat_id=7594389667,
        # chat_id=5139311660,
        chat_id=5014598015, #@Multiphone_stav1
        text=f" Новый заказ!\nИмя пользователя: {data.get('name')}\nНомер телефона: {message.contact.phone_number}\n\nТовары: \n" + text,
        parse_mode="HTML"
    )

    await message.answer(
        text=f"Благодарим вас за заказ, ваша корзина была отправлена! Ожидайте звонка!",
        reply_markup=keyboardFabric.createCustomReplyKeyboard(buttons)
    )