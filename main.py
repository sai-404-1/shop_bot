import keyboards.keyboardFabric as keyboardFabric
import keyboards.callbacks as inline_callbacks
import manager.fsm.fsm_handler as fsm_handler
import keyboards.buttons as button_types

import myUtils.Json as Json

from starter import *

@dp.message(Command("start"))
async def cmd_start(message: Message):
    dataset = Json.getMainDataset()
    user = CRUD.for_model(Users).get(db_session, user_id=message.from_user.id)
    
    if len(user) == 0:
        user = CRUD.for_model(Users).create(db_session, 
            username=message.from_user.username, 
            user_id=message.from_user.id
        )
    else: user = user[0]
    
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