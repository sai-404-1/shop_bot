from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup

class StatesForCreate(StatesGroup):
    product_name = State()
    product_description = State()
    product_price = State()
    product_photo = State()
    product_type = State()
    product_quantity = State()