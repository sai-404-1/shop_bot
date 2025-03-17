from starter import *

from .buttons import *
import keyboards.keyboardFabric as keyboardFabric
import keyboards.messageGenerator as messageGenerator

async def send_generated_message(callback):
    data = callback.data
    mg = messageGenerator.MessageGenerator(data)
    await callback.message.edit_text(
        mg.getText(),
        reply_markup = mg.getInlineKeyboard()
    )

@dp.callback_query(F.data.in_([
    "main", "categories", "menu", "new_devices",
    "used_devices", "beauty", "game_consoles",
    "accessories", "smartphones", 
    "database_change", "admin_menu_products"
]))
async def regenerate_button_callback(callback: types.CallbackQuery):
    await send_generated_message(callback)

@dp.callback_query(F.data.in_(
    [obj.name for obj in CRUD.for_model(Type).get(db_session)]
))
async def product_type_handler(callback: types.CallbackQuery):
    # TODO: add state machine for new_devices/used_devices
    type_id = CRUD.for_model(Type).get(db_session, name=callback.data)[0].id
    phones = CRUD.for_model(Product).get(db_session, type_id=type_id)
    buttons = []
    tg = messageGenerator.TextGenerator(callback.data)

    for phone in phones:
        buttons.append(InlineButton(phone.name, str(phone.id)))
    await callback.message.edit_text(tg.getMessagePart(), reply_markup=keyboardFabric.createCustomInlineKeyboard(buttons))

@dp.callback_query(F.data.in_([
    str(product.id) for product in CRUD.for_model(Product).all(db_session)
]))
async def process_callback(callback: types.CallbackQuery):
    object = CRUD.for_model(Product).get(db_session, type_id=int(callback.data))[0]
    await callback.message.answer_photo(
        types.FSInputFile(
            f"{photo_path}/{object.photo}"
        ),
        caption="{}\n\n{}\n\n{}".format(object.name, object.description, object.price)
    )



@dp.callback_query(F.data == "create_product")
async def db_changer(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(StatesForCreate.product_name)
    await callback.answer("Идёт процесс создния товара...")
    current_message = await callback.message.answer("Введите название")
    progress_message = await callback.message.answer("...")
    data = await state.get_data()
    data.update({
        'product_create_progress': progress_message, 'current_message': current_message
    })
    await state.set_data(data)