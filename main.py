import keyboards.keyboardFabric as keyboardFabric
import keyboards.callbacks as inline_callbacks
import keyboards.keyboardCallbacks as keyboard_callbacks
import manager.fsm.fsm_handler as fsm_handler
import keyboards.buttons as button_types
import keyboards.change_product_callbacks as product_changer
import keyboards.delete_product_callbacks as product_deleter

import myUtils.fastFunctions.buttons as fastFunctions_buttons
import myUtils.fastFunctions as fastFunctions

from aiogram.types import CallbackQuery
from starter import *

@dp.message(CommandStart(deep_link=True))
async def cmd_start_arguments(message: Message, command: CommandObject, state: FSMContext):
    # await state.clear()
    product = CRUD.for_model(Product).get(db_session, id=int(command.args))[0]
    maxQuantity = product.quantity
    # await state.set_data({
    #     "productId": product.id,
    #     "currQuantity": 1,
    #     "maxQuantity": maxQuantity
    # })

    media = []
    for photo in product.photo:
        media.append(
            InputMediaPhoto(media=FSInputFile(f"{photo_path}/{photo}"))  # Используем FSInputFile для локальных файлов
        )

    sent_messages = await message.answer_media_group(media=media)
    data = await state.get_data()
    data.update({
        "for_delete": [[msg.chat.id, msg.message_id] for msg in sent_messages], 
        "productId": product.id,
        "currQuantity": 1,
        "maxQuantity": maxQuantity})
    await state.set_data(data)

    keyboard = await keyboardFabric.createBeforeBasketKeyboard(state)
    await message.delete()

    await message.answer(
        "{}\n\n[Ссылка на товар]({})".format(
            # fastFunctions.text.insert_after_first_line(product.name, f"Цена: {product.price}₽"), 
            product.name,
            await create_start_link(bot, str(product.id))),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
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

    await message.answer(
        text=dataset["message_texts"]["main"],
        reply_markup=keyboardFabric.createCustomReplyKeyboard(buttons)
    )

@dp.message(Command("admin"))
async def cmd_basket(message: Message, state: FSMContext):
    await state.clear()
    user = CRUD.for_model(Users).get(db_session, user_id=message.from_user.id)[0]
    print(user, user.role, user.username)
    if user.role >= 1: 
        mes = await message.answer('.')
        callback_query = CallbackQuery(
            id="callback_query_id",
            from_user=message.from_user,
            chat_instance=str(mes.chat.id),
            data="database_change",
            message=mes
        )
        await fastFunctions_buttons.send_generated_message(callback_query)

@dp.message(Command("test"))
async def test(message: Message, state: FSMContext):
    await state.set_state(StatesForCreate.product_photo)
    await message.answer("Now send me many different photo")

@dp.message(Command("basket"))
async def cmd_basket(message: Message, state: FSMContext):
    await fastFunctions_buttons.show_basket(user_id=message.from_user.id, state=state, message=message)

if __name__ == "__main__":
    import asyncio
    # function main is declared in starter.py
    asyncio.run(main())
