from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from database.database import session, Customer, Product, Organization

products = session.query(Product).all()

product_titles = [p.title for p in products]

products_menu = ReplyKeyboardMarkup(
	keyboard = [
	[
		KeyboardButton(text="📥Savat"),
		KeyboardButton(text="🚖Buyrtuma berish")
	],
	],
	resize_keyboard=True
	)


products_menu.add(*(KeyboardButton(text=product.title) for product in products))
