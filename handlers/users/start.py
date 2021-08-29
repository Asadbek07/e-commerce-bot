from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp, bot
from keyboards.default.language import menuStart
from keyboards.default.menus import menu_product_types_eng, menu_product_types_uz
from aiogram.dispatcher import FSMContext
from states.user_state import Personal
from keyboards.default.phone import phone_uz, phone_eng
from random import randint
from database.database import session, Customer, Product, Organization
from twilio.rest import Client


sms_codes = {}

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = 'AC358cbabe5036f4efb73aa7933864e1a4'
auth_token = '9027a9f95292d28a8545ce876dd7dc10'
client = Client(account_sid, auth_token)


# print(message.sid)
@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    
    custumer = session.query(Customer).filter(Customer.id==message.from_user.id).first()
    if custumer is None:
        await message.answer(f"Salom, {message.from_user.full_name}.\n\nKeling avvaliga xizmat ko'rsatish tilini tanlab olaylik. \n\nHi! Let's first we choose language of serving!", reply_markup=menuStart)
        print(message.from_user)
        await Personal.language.set()
    else:
        print(message.from_user.id)
        lang = "uz" if custumer.language == "🇺🇿O'zbekcha" else "eng"
        text = {
            "uz" : "Bosh menyu",
            "eng" : "Main menu",
        }    
        keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
        await message.answer(text[lang], reply_markup=keyboard)

@dp.message_handler(state=Personal.language)
async def language_choose(message: types.Message, state : FSMContext):
    language = message.text
    await state.update_data({
        'language' : language,
        })

    text = {
            "uz" :{
            "phone_guide" : "Chaykofda elektron hamyon ochish uchun quyidagi qo'llanmaga amal qiling", 
            "guide" : "Telefon raqamingiz qanday ? Telefon raqamingizni jo'natish uchun quyidagi \"Raqamni jo'natish\" tugmasini bosing."
            },
            "eng" : {
            "phone_guide" : "In order to create wallet on Chaykof, you need to follow this guide",
            "guide" : "What is your phone number? For sending phone number press \"Send phone number\" button below."
            },
            "except" : {
                "error" : "Iltimos yaroqli tilni tanlang!\n\nPlease enter valid language!"
            }
            }
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng" if language == "🇬🇧English" else "except"
    if lang != "except":
        send_text1 = text[lang]["phone_guide"]
        send_text2 = text[lang]["guide"]   
        keyboard = phone_uz if lang == "uz" else phone_eng     
        await message.answer(send_text1)
        await message.answer(send_text2, reply_markup=keyboard)
        await Personal.next()
    else:
        await message.answer(text[lang]["error"])

@dp.message_handler(state=Personal.phone,content_types=["contact"])
async def phone_input(message : types.Message, state : FSMContext):
    contact = message.contact.phone_number
    print(contact)
    await state.update_data({
        "phone" : contact,
        })
    text = {
        "uz" : "Kod jo'natildi. Akkauntni aktiv holga keltirish uchun kodni jo'nating.",
        "eng": "A sms code is sent. Please, type the code that was sent to you.",
    }
    code = randint(100000, 999999)
    await state.update_data({
        "code" : code,
        })
    sms_codes[message.from_user.id] = code
    sms_text = {
        "uz" : f"Choykofdan sizning aktivatsiya kodingiz : {code}",
        "eng": f"From Choykof, your activation code : {code}."
    } 
    language = await state.get_data()
    language = language.get('language')
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng" 
    send_text = text[lang] # sms uchun text
    print(sms_text[lang])
    phone_number = contact
    sms = client.messages \
                    .create(
                         body=sms_text[lang],
                         from_='+1 989 310 7966',
                         to=f"+{phone_number}"
                     )
    await message.answer(send_text)
    await Personal.next()

@dp.message_handler(lambda message : message.text is not None, state=Personal.phone)
async def phone_input_incorrect(message : types.Message, state : FSMContext):
    text = {
            "uz" :{ 
            "guide" : "Telefon raqamingiz qanday ? Telefon raqamingizni jo'natish uchun quyidagi \"Raqamni jo'natish\" tugmasini bosing."
            },
            "eng" : {
            "guide" : "What is your phone number? For sending phone number press \"Send phone number\" button below."
            },
        }
    language = await state.get_data()
    language = language.get('language')
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng"    
    keyboard = phone_uz if lang == "uz" else phone_eng
    await message.answer(text[lang]['guide'], reply_markup=keyboard)

@dp.message_handler(state=Personal.code)
async def code_input(message : types.Message, state : FSMContext):
    data = await state.get_data()
    language = data.get('language')
    lang = "uz" if language == "🇺🇿O'zbekcha" else "eng"
    try:

        isauthenticated = data.get('code') == int(message.text)
    except:
        isauthenticated = False    
    text = {
        "uz" : "Ismingizni kiriting: ",
        "eng" : "Enter your name: ",
    }

    code_text = {
        "uz" : "Notog'ri kod kiritildi.",
        "eng" : "Invalid code."
    }
    if isauthenticated:
        await message.answer(text[lang])
        await Personal.next()
    else:
        await message.answer(code_text[lang])    

@dp.message_handler(state=Personal.name)
async def name_input(message : types.Message, state : FSMContext):
    name = message.text
    await state.update_data({
        "name" : name,
        })
    data = await state.get_data()
    name = data.get("name")
    language = data.get("language")
    phone = data.get("phone")
    customer = Customer(username=name, id=message.from_user.id, language=language, phone=phone, location_keng=0, location_uzun=0)
    session.add(customer)
    session.commit()
    await state.reset_state()
    lang = "uz" if customer.language == "🇺🇿O'zbekcha" else "eng"
    text = {
            "uz" : "Bosh menyu",
            "eng" : "Main menu",
    }    
    keyboard = menu_product_types_uz if lang == "uz" else menu_product_types_eng
    await message.answer(text[lang], reply_markup=keyboard)

    # await message.answer(f"Malumotlar -> \nname : {customer.name}\nphone : {custumer.phone},\nlanguage : {custumer.language}.")
