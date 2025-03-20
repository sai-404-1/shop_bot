import keyboards.keyboardFabric as keyboardFabric
import keyboards.callbacks as inline_callbacks
import manager.fsm.fsm_handler as fsm_handler
import keyboards.buttons as button_types
import keyboards.change_product_callbacks as product_changer

import myUtils.Json as Json

from starter import *

@dp.message(CommandStart(deep_link=True))
async def cmd_start_arguments(message: Message, command: CommandObject, state: FSMContext):
    product = CRUD.for_model(Product).get(db_session, id=int(command.args))[0]
    maxQuantity = product.quantity
    await state.set_data({
        "productId": product.id,
        "currQuantity": 1,
        "maxQuantity": maxQuantity
    })
    keyboard = await keyboardFabric.createBeforeBasketKeyboard(state)
    await message.delete()
    await message.answer_photo(
        types.FSInputFile(
            f"{photo_path}/{product.photo}"
        ),
        caption="{}\n\n{}\n\n[Ссылка на товар]({})".format(product.name, product.price, await create_start_link(bot, str(product.id))),
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


@dp.message(CommandStart())
async def cmd_start(message: Message):
    dataset = Json.getMainDataset()

    # We are creating a new user if that not be was before
    user = CRUD.for_model(Users).get(db_session, user_id=message.from_user.id)
    if len(user) == 0:
        user = CRUD.for_model(Users).create(db_session, 
            username=message.from_user.username, 
            user_id=message.from_user.id
        )
    else: user = user[0]
    
    # Creating /start menu
    buttons = []
    for button_data in dataset["main"] if user.role >= 1 else dataset["main"][:2]:
        buttons.append(button_types.InlineButton(button_data[0], button_data[1]))

    await message.answer(
        text=dataset["message_texts"]["main"],
        reply_markup=keyboardFabric.createCustomInlineKeyboard(buttons)
    )


if __name__ == "__main__":
    import asyncio
    # function main is declared in starter.py
    asyncio.run(main())