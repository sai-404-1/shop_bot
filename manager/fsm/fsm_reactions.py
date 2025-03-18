from starter import *
from keyboards import keyboardFabric

# Копипаста, но да
async def copy1(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product = CRUD.for_model(Product).get(db_session, id=data["productId"])[0]
    if data.get("isBasket"):
        keyboard = await keyboardFabric.createProductFromBasketKeyboard(state)
    else:
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
    isBasket = data.get("isBasket")
    try:
        newQuantity = int(message.text.strip())
        if newQuantity <= 0:
            await message.reply("Quantity can't be negative or 0")
        elif newQuantity > data["maxQuantity"]:
            await message.reply("Quantity is too big")
        elif isBasket:
            await state.update_data(currQuantity=newQuantity)
            basket_position = CRUD.for_model(Basket).get(db_session, user_id = message.from_user.id, products_id=data["productId"])[0]
            CRUD.for_model(Basket).update(db_session, basket_position.id, quantity=newQuantity)
            await copy1(message, state)
        else:
            await state.update_data(currQuantity=newQuantity)
            await copy1(message, state)
    except Exception as e:
        await message.reply("Wrong input")
        print(e)

