from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_product_types_eng = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="🛍Заказать"),
		],
		[
			KeyboardButton(text="✍️Оставить отзыв"),
			KeyboardButton(text="☎️Связаться с нами"),
		],
		[
			KeyboardButton(text=" ⚙️Настройки"),
		],
	], 
	resize_keyboard=True
	)


menu_product_types_uz = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="🛍Buyurtma berish"),
		],
		[
			KeyboardButton(text="✍️Fikr bildirish"),
			KeyboardButton(text="☎️Biz bilan aloqa"),
		],
		[
			KeyboardButton(text=" ⚙️Sozlamalar"),
		],
	], 
	resize_keyboard=True
	)