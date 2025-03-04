import inline_buttons.buttons as inline_buttons
import inline_buttons.callbacks as inline_callbacks

from starter import *

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(templates.start_message, reply_markup=inline_buttons.categories())

@dp.message()
async def all_messages(message: Message):
    await message.answer('пиши /start, дэбик')


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())