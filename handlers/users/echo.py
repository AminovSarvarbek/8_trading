from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from loader import rt, lt, admin_router
from models.user import User
from keyboards.default.main_menu_kb import mainmenu_ru, mainmenu_uz

@rt.callback_query(F.data.startswith('uz_lang'))
@rt.callback_query(F.data.startswith('ru_lang'))
async def change_language(call: CallbackQuery):
    user_id = call.from_user.id
    lang = call.data
    user = await User.get(chat_id=call.message.chat.id)

    if lang == "uz_lang":
        user.lang = "uz"
        await call.message.answer(lt._(id=user_id, key="info_change_lang"), reply_markup=mainmenu_uz())
    elif lang == "ru_lang":
        user.lang = "ru"
        await call.message.answer(lt._(id=user_id, key="info_change_lang"), reply_markup=mainmenu_ru())

    await user.save()
    await call.answer()


@admin_router.callback_query(F.data.startswith('cancel'))
async def cancel_ad_sending(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()
    # await callback_query.answer("Action canceled.")
    await callback_query.message.edit_text(lt._(id=callback_query.message.chat.id, key="process_canceled_message"))