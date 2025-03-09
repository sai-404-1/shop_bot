import keyboards.keyboardFabric as keyboardFabric
import keyboards.callbacks as inline_callbacks

from starter import *

@dp.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(templates.start_message, reply_markup=keyboardFabric.categories())

@dp.message()
async def all_messages(message: Message):
    await message.answer('пиши /start, дэбик')



if __name__ == "__main__":
    import asyncio
    # function main is declared in starter.py
    asyncio.run(main())