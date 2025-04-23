from starter import *
from keyboards import keyboardFabric
from keyboards.buttons import InlineButton
import json

# Копипаста, но да
async def copy1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=data["productId"])[0]
    if data.get("isBasket"):
        keyboard = await keyboardFabric.createProductFromBasketKeyboard(state)
    else:
        keyboard = await keyboardFabric.createBeforeBasketKeyboard(state)
    await message.delete()
    await message.answer_photo(
        types.FSInputFile(
            f"{photo_path}/{product.photo}"
        ),
        caption="{}\n\nЦена: {}₽ \n\n{}".format(product.name, int(product.price), product.description),
        reply_markup=keyboard
    )

@fsm_router.message(StatesForButtons.ready_to_enter_new_quantity)
async def enter_new_quantity(message: types.Message, state:FSMContext):
    data = await state.get_data()
    isBasket = data.get("isBasket")
    try:
        newQuantity = int(message.text.strip())
        if newQuantity <= 0:
            await message.reply("Quantity can't be negative or 0")
        elif newQuantity > data["maxQuantity"]:
            await message.reply("Quantity is too big")
        elif isBasket:
            await state.update_data(currQuantity=newQuantity)
            basket_position = CRUD.for_model(Basket).get(db_session, user_id = message.from_user.id, products_id=data["productId"])[0]
            CRUD.for_model(Basket).update(db_session, basket_position.id, quantity=newQuantity)
            await copy1(message, state)
        else:
            await state.update_data(currQuantity=newQuantity)
            await copy1(message, state)
    except Exception as e:
        await message.reply("Wrong input")
        print(e)

# for communocation with manager
async def sendToManagers(state: FSMContext, chat_id: int):
    data = await state.get_data()
    
    managers = CRUD.for_model(Users).get(db_session, role = 1)
    managers += CRUD.for_model(Users).get(db_session, role = 2)

    for manager in managers:
        manager_id = manager.user_id
        await bot.send_message(
            chat_id=manager_id,
            text=f"New message in support chat number {chat_id}",
            reply_markup=keyboardFabric.createCustomInlineKeyboard(buttons=[
                InlineButton(
                    "Open chat",
                    "//support//{}".format(chat_id)
                )
            ])
        )

def messagesAppend(chat: str, user_id: int, message: str) -> str:
    messages = json.loads(chat)
    messages.append([user_id, message])
    chat = json.dumps(messages)
    return chat

@fsm_router.message(StatesForManager.userCommunicate)
async def messageByUser(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user = CRUD.for_model(Users).get(db_session, user_id=message.from_user.id)[0]
    chat = CRUD.for_model(Communication).get(db_session, user_id=user.user_id)
    chat = chat[0]
    chat.messages = messagesAppend(chat.messages, user.user_id, message.text)
    print(chat.messages)
    print(chat.id)
    CRUD.for_model(Communication).update(db_session, chat.id, messages=chat.messages)
    chat = CRUD.for_model(Communication).get(db_session, user_id=user.user_id)[0]
    print(chat.messages)
    if chat.readed == True:
        await sendToManagers(state, chat.user_id)
        chat.readed = False

@fsm_router.message(StatesForManager.managerCommunicate)
async def messageByManager(message: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = int(data["userId"])
    print(user_id)
    user = CRUD.for_model(Users).get(db_session, user_id=user_id)[0]
    chat = CRUD.for_model(Communication).get(db_session, user_id=user.user_id)[0]    
    chat.messages = messagesAppend(chat.messages, message.from_user.id, message.text)
    await bot.send_message(
        chat_id=user_id,
        text=f"Answer from manager: {message.text}",
        reply_markup=keyboardFabric.createCustomInlineKeyboard(buttons=[
            InlineButton(
                "Open chat",
                "//help//{}".format(user_id)
            )
        ])
    )
    await message.answer(
        "Message has been sent to user, you can send more messages or go back to main menu",
        reply_markup=keyboardFabric.createKeyboardWithBackButton([], "main")
    )