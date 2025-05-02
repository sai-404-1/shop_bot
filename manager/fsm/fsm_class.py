from aiogram.fsm.state import State
from aiogram.fsm.state import StatesGroup

class StatesForCreate(StatesGroup):
    product_name = State()
    product_description = State()
    product_price = State()
    multiple_photos_handler = State()
    single_photo_handler = State()
    product_photo = State()         # Кажется нигде не используется
    product_type = State()
    product_quantity = State()

class StatesForUpdate(StatesGroup):
    product_name = State()
    product_description = State()
    product_price = State()
    multiple_photos_handler = State()
    single_photo_handler = State()
    product_type = State()
    product_quantity = State()

class StatesForButtons(StatesGroup):
    ready_to_enter_new_quantity = State()

class StatesForManager(StatesGroup):
    userCommunicate = State()
    managerCommunicate = State()

class StatesForRegBasket(StatesGroup):
    name = State()
    phone_number = State()
