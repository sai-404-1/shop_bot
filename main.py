import keyboards.keyboardFabric as keyboardFabric
import keyboards.callbacks as inline_callbacks
import keyboards.buttons as button_types

import myUtils.Json as Json

from starter import *

@dp.message(Command("start"))
async def cmd_start(message: Message):
    dataset = Json.getMainDataset()
    message_text = dataset["message_texts"]["main"]
    buttons = []
    for button_data in dataset["main"]:
        buttons.append(button_types.InlineButton(button_data[0], button_data[1]))

    await message.answer(message_text, reply_markup=keyboardFabric.createCustomInlineKeyboard(buttons))

@dp.message()
async def all_messages(message: Message):
    await message.answer('пиши /start, дэбик')



if __name__ == "__main__":
    import asyncio
    # function main is declared in starter.py
    asyncio.run(main())