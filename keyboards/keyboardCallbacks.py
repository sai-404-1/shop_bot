from starter import *

from aiogram.utils.keyboard import InlineKeyboardMarkup

from .buttons import *
import keyboards.keyboardFabric as keyboardFabric
import keyboards.messageGenerator as messageGenerator
import myUtils.Json as Json
from myUtils.fastFunctions.buttons import show_basket

@dp.message(F.text.in_(
    [button[0] for button in Json.getMainDataset()["menu"]]
    # ['Новые устройства', 'Б/у устройства', 'Красота', 'Игровые приставки', 'Аксессуары', 'Корзина', 'Связь с менеджером', 'Доставка / оплата']
))
async def buttons_header(message: Message, state: FSMContext):
    await message.delete()

    if message.text == "Корзина":
        await show_basket(user_id=message.from_user.id, state=state, message=message)
    
    elif message.text == "Связь с менеджером":
        chat = CRUD.for_model(Communication).get(db_session, user_id=message.from_user.id)
        if len(chat) == 0:
            CRUD.for_model(Communication).create(db_session, user_id=message.from_user.id)
            chat = CRUD.for_model(Communication).get(db_session, user_id=message.from_user.id)
        chat = chat[0]
        await message.answer(
            "Вы перешли в чат с поддержкой.\nПожалуйста, опишите ваш вопрос и ожидайте ответа", 
            reply_markup=keyboardFabric.createCustomInlineKeyboard([
                InlineButton(
                    "Отменить",
                    "delete_message"
        )]))
        await state.set_state(StatesForManager.userCommunicate)
    
    elif message.text == "Доставка / оплата":
        # TODO добавить возможность выбора товара для оформления и последующую его обработку
        # basket = CRUD.for_model(Basket).get(db_session, user_id=message.from_user.id)
        # text = 'Ваша корзина. Вы можете выбрать желаемые товары или нажать "Продолжить", чтобы выбрать всю корзину'
        # buttons = []
        # for basket_position in basket:
        #     product = CRUD.for_model(Product).get(db_session, id=basket_position.products_id)[0]
        #     buttons.append(InlineButton(product.name + " ❌", "basket_check__" + str(product.id)))

        # await state.set_data({"isBasket": True})
        # keyboard = keyboardFabric.createCustomInlineKeyboard([
        #         InlineButton(
        #             "Удалить сообщение 🗑",
        #             "delete_message"
        # )])

        # current_message = message.answer(text, reply_markup=keyboard)
        if len(CRUD.for_model(Basket).get(db_session, user_id=message.from_user.id)) != 0:
            keyboard = keyboardFabric.createCustomInlineKeyboard([
                InlineButton(
                    "Перейти к оформлению 💳",
                    "register_basket"
                ),
                InlineButton(
                    "Удалить сообщение 🗑",
                    "delete_message"
                )
            ])
            current_message = await message.answer("Нажмите, чтобы перейти к оформлению", reply_markup=keyboard)
            data = await state.get_data()
            data.update({'current_message': current_message})
        else:
            await message.answer("В вашей корзине ничего нет! Добавьте товар или обратитесь к менеджеру",
                reply_markup=keyboardFabric.createCustomInlineKeyboard([
                    InlineButton(
                        "Связь с менеджером",
                        "manager"
                    )
                ])
            )

    else:
        for button in Json.getMainDataset()["menu"]:
            if button[0] == message.text:
                mg = messageGenerator.MessageGenerator(button[1])
                await message.answer(
                    mg.getText(),
                    reply_markup = mg.getInlineKeyboard()
                )