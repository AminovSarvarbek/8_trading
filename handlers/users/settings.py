from aiogram import F
from aiogram import types

from loader import rt
from models.user import User
from keyboards.default.settings_kb import settings_btns_ru, settings_btns_uz
from keyboards.inline.lang_set_inline import lang_set
from keyboards.default.main_menu_kb import mainmenu_uz, mainmenu_ru

@rt.message(F.text=="Sozlamalar ⚙️")
@rt.message(F.text=="Настройки ⚙️")
async def settings_menu(message: types.Message):
    user = await User.get(chat_id=message.chat.id)
    if user.lang == "uz":
        msg = f"Sozlamalar menyusi:"
        await message.answer(msg, reply_markup=settings_btns_uz())
    else:
        msg = f"Меню настроек:"
        await message.answer(msg, reply_markup=settings_btns_ru())


@rt.message(F.text=="Til 🇺🇿")
@rt.message(F.text=="Язык 🇷🇺")
async def set_lang_again(message: types.Message):
    user = await User.get(chat_id=message.chat.id)
    if user.lang == "uz":
        await message.answer(text="Tilni o'zgartirish:", reply_markup=lang_set())
    else:
        await message.answer("Изменить язык:", reply_markup=lang_set())


@rt.message(F.text=="⬅️ Orqaga")
@rt.message(F.text=="⬅️ Назад")
async def get_back(message: types.Message):
    user = await User.get(chat_id=message.chat.id)
    if user.lang == "uz":
        await message.answer("Asosiy menyu:", reply_markup=mainmenu_uz())
    else:
        await message.answer("Главное меню:", reply_markup=mainmenu_ru())

