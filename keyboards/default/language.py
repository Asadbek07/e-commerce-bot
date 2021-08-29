from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menuStart = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="🇺🇿O'zbekcha"),
		],
		[
			KeyboardButton(text="🇬🇧English")
		]
	], 
	one_time_keyboard=True,
	resize_keyboard=True
	)