from starter import *
from keyboards.keyboardFabric import InlineButton
import keyboards.messageGenerator as messageGenerator

async def send_generated_message(callback):
    data = callback.data
    mg = messageGenerator.MessageGenerator(data)
    await callback.message.edit_text(
        mg.getText(),
        reply_markup = mg.getInlineKeyboard()
    )

async def show_basket(user_id: int, state: FSMContext, message: Message | types.CallbackQuery):
    basket = CRUD.for_model(Basket).get(db_session, user_id=user_id)
    buttons = []
    text = ""
    
    for basket_position in basket:
        product = CRUD.for_model(Product).get(db_session, id=basket_position.products_id)[0]
        quantity = basket_position.quantity
        buttons.append(InlineButton(product.name, str(product.id)))
        text += f"Товар: {product.name} \nКол-во: {quantity}\n\n"

    await state.set_data({"isBasket": True})
    keyboard = keyboardFabric.createCustomInlineKeyboard([
            InlineButton(
                "Связь с менеджером",
                "manager"
            ),
            InlineButton(
                "Удалить сообщение 🗑",
                "delete_message"
            )
    ])

    # Проверяем, является ли message объектом CallbackQuery
    if isinstance(message, types.CallbackQuery):
        try:
            await message.message.delete()
            await message.message.answer("Ваша корзина:\n\n" + text, reply_markup=keyboard)
        except:
            await message.delete()
            await message.answer("Ваша корзина:\n\n" + text, reply_markup=keyboard)
    else:
        await message.answer("Ваша корзина:\n\n" + text, reply_markup=keyboard)