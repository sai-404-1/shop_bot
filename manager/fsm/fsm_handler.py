from starter import *

# @dp.message(F.text)
# async def every_message(message: Message, state: FSMContext):
#     if await state.get_state() == FSM_States.product_create:
#         data = await state.get_data()
#         await message.answer(message.text)

"""
Короче, для установки даты, пиши:
await state.set_data()

Чтобы получить дату, пиши:
await state.get_data()

И то и другое должно возвращать словарь
""" 