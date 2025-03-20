from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup

class StatesForCreate(StatesGroup):
    product_name = State()
    product_description = State()
    product_price = State()
    product_photo = State()
    product_type = State()
    product_quantity = State()

class StatesForUpdate(StatesGroup):
    product_name = State()
    product_description = State()
    product_price = State()
    product_photo = State()
    product_type = State()
    product_quantity = State()

class StatesForButtons(StatesGroup):
    ready_to_enter_new_quantity = State()

class StatesForManager(StatesGroup):
    userCommunicate = State()
    managerCommunicate = State()