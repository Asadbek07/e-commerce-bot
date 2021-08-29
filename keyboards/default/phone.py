from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

phone_uz = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="Raqamni jo'natish", request_contact=True),
		],
	], 
	one_time_keyboard=True,
	resize_keyboard=True
	)


phone_eng = ReplyKeyboardMarkup(
	keyboard=[
		[
			KeyboardButton(text="Send phone number", request_contact=True),
		],
	], 
	one_time_keyboard=True,
	resize_keyboard=True
	)