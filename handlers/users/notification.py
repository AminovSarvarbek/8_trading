from aiogram.fsm.context import FSMContext
from aiogram import types, F

from loader import rt, lt, bot
from utils.get_data import get_binance_data, get_tradingv_data
from states.user import NotificationState
from keyboards.inline.cancel import cancel_button
from models.user import User
from data.config import API_KEY, SECRET_KEY


@rt.message(F.text=="Bildirishnoma 💬")
@rt.message(F.text=="Уведомление 💬")
async def notification_handler(message: types.Message, state: FSMContext):
    await message.answer(lt._(id=message.chat.id, key="notification_message"), reply_markup=cancel_button)
    await state.set_state(NotificationState.text)

@rt.message(NotificationState.text)
async def get_text_notification(message: types.Message, state: FSMContext):
    text = f"User: {message.chat.id}\n\n{message.text}"
    admins = await User.filter(is_admin=True)
    for admin in admins:
        await bot.send_message(
            chat_id=admin.chat_id,
            text=text
        )
    
    await message.answer("Xabaringiz adminlarga yuborildi✅")
    await state.clear()
