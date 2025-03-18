from starter import *
from keyboards import keyboardFabric

# Копипаста, но да
async def copy1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=data["productId"])[0]
    buttons = []
    keyboard = await keyboardFabric.createBeforeBasketKeyboard(state)
    await message.delete()
    await message.answer_photo(
        types.FSInputFile(
            f"{photo_path}/{product.photo}"
        ),
        caption="{}\n\n{}\n\n{}".format(product.name, product.description, product.price),
        reply_markup=keyboard
    )

@fsm_router.message(StatesForButtons.ready_to_enter_new_quantity)
async def enter_new_quantity(message: types.Message, state:FSMContext):
    data = await state.get_data()
    try:
        newQuantity = int(message.text.strip())
        if newQuantity <= 0:
            await message.reply("Quantity can't be negative or 0")
        elif newQuantity > data["maxQuantity"]:
            await message.reply("Quantity is too big")
        else:
            await state.update_data(currQuantity=newQuantity)
            await copy1(message, state)
    except Exception as e:
        await message.reply("Wrong input")
        print(e)

