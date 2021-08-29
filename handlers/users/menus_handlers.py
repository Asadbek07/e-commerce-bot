from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp, CommandStart
from database.database import session, Customer, Product, Organization
from loader import dp
from aiogram.dispatcher.filters import Text
from keyboards.default.product_menus import products_menu


@dp.message_handler(Text(contains="🛍Заказать", ignore_case=True))
async def order_handler(message: types.Message):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.id == user_id).first()
    ordered_products = customer.ordered_products.all()
    if len(ordered_products) == 0:
        await message.answer("С чего начнем?", reply_markup=products_menu) # productlar ro'yxatini chiqar
    else:
        # Location ni olish kerak
        text = "Sizning buyurtmalaringiz : \n"
        i = 1
        for p in ordered_products:
            text += f"{i}. {p.title}\nMiqdor: {p.amount}\n"
        text += f"Umumiy to'lov : {customer.get_total_price}"    
        await message.answer(text)


@dp.message_handler(Text(contains="🛍Buyurtma berish", ignore_case=True))
async def order_handler(message: types.Message):
    user_id = message.from_user.id
    customer = session.query(Customer).filter(Customer.id == user_id).first()
    ordered_products = customer.ordered_products.all()
    if len(ordered_products) == 0:
        await message.answer("Qayerdan boshlaymiz?", reply_markup=products_menu) # productlar ro'yxatini chiqar
    else:
        # Location ni olish kerak
        text = "Sizning buyurtmalaringiz : \n"
        i = 1
        for p in ordered_products:
            text += f"{i}. {p.title}\nMiqdor: {p.amount}\n"
        text += f"Umumiy to'lov : {customer.get_total_price}"    
        await message.answer(text)
