from aiogram import types, F
from loader import rt, lt
from models.user import User


@rt.message(F.text=="Premium 🌟")
@rt.message(F.text=="Премиум 🌟")
async def premium_info(message: types.Message):
    user = await User.get(chat_id=message.chat.id)
    if user.is_premium:
        await message.answer(lt._(id=message.chat.id, key="premium_user_info"))
    await message.answer(lt._(id=message.chat.id, key="premium_info"))

