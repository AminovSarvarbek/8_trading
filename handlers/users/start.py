from aiogram.types import Message
from aiogram.filters import CommandStart

from loader import rt, lt
from keyboards.default.main_menu_kb import mainmenu_uz, mainmenu_ru
from keyboards.inline.lang_set_inline import lang_set
from keyboards.default.admin import admin_keyboard
from models.user import User  


@rt.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    user_name = message.from_user.full_name

    user = await User.filter(chat_id=user_id).first()
    if not user:
        msg = (
            lt._(id=user_id, key="start_message")
            + "\n\n❗ "
            + lt._(id=user_id, key="info_change_lang")
        )
        await User.create(chat_id=user_id, first_name=user_name, lang="uz")
        await message.answer(msg, reply_markup=lang_set())
    elif user.is_admin:
        await message.answer("Salom admin ✅", reply_markup=admin_keyboard)
    else:
        # if the user first name has change, change to db
        if user_name != user.first_name:
            user.first_name = user_name
            await user.save()
            
        if user.lang == "uz":
            await message.answer(
                lt._(id=user_id, key="start_message"), reply_markup=mainmenu_uz()
            )
        else:
            await message.answer(
                lt._(id=user_id, key="start_message"), reply_markup=mainmenu_ru()
            )
