# from aiogram.fsm.state import State
# from aiogram.fsm.state import StatesGroup
from starter import *


product_create_states = [
    StatesForCreate.product_name,
    StatesForCreate.product_description,
    # StatesForCreate.product_price,
    # StatesForCreate.product_photo,
    # StatesForCreate.product_type,
    # StatesForCreate.product_quantity,
]

product_template = [
    ["Название", "product_name"],
    ["Описание", "product_description"]
]

async def create_progress_message(data):
    result = ""
    for step in product_template:
        result += f"{step[0]}: {'❌' if data.get(step[1]) == None else data.get(step[1])}\n"
    return result

@fsm_router.message(StatesForCreate.product_name)
async def message_try(message: Message, state: FSMContext):
    data = await state.get_data()
    await data.get('current_message').delete()
    current_message = await message.answer('Теперь описание')
    data.update(
        {'product_name': message.text, 'current_message': current_message}
    )
    await state.set_data(data)
    await state.set_state(StatesForCreate.product_description)
    await data['product_create_progress'].edit_text(await create_progress_message(data))
    await message.delete()

@fsm_router.message(StatesForCreate.product_description)
async def message_try(message: Message, state: FSMContext):
    data = await state.get_data()
    await data.get('current_message').delete()
    data.update(
        {'product_description': message.text}
    )
    await message.answer('Товар создан')
    await state.set_data(data)
    await data['product_create_progress'].edit_text(await create_progress_message(data))
    await state.clear()
    await message.delete()