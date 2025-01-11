import tortoise
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loader import admin_router
from models.user import User
from keyboards.inline.cancel import cancel_button
from states.admin import AddPremiumState, DelPremiumState


@admin_router.message(F.text == "🌟Add Premium")
async def add_premium(message: Message, state: FSMContext):
    await message.answer("Iltimos, premium qilishni xohlagan foydalanuvchining chat_id raqamini kiriting:", reply_markup=cancel_button)
    await state.set_state(AddPremiumState.chat_id)


@admin_router.message(AddPremiumState.chat_id)
async def process_add_premium(message: Message, state: FSMContext):
    chat_id = message.text.strip()
    if not chat_id.isdigit():
        await message.answer("Noto'g'ri chat_id. Iltimos, to'g'ri raqam kiriting:")
        return

    try:
        chat_id = int(chat_id)
        user = await User.get(chat_id=chat_id)
        user.is_premium = True
        await user.save()

        await message.answer(f"Foydalanuvchi (chat_id: {chat_id}) premium qilib belgilandi.")
    except tortoise.exceptions.DoesNotExist:
        await message.answer("Foydalanuvchi topilmadi.")

    await state.clear()


# Remove Premium
@admin_router.message(F.text == "🗑Remove Premium")
async def remove_premium(message: Message, state: FSMContext):
    await message.answer("Iltimos, premiumlikni olib tashlamoqchi bo'lgan foydalanuvchining chat_id raqamini kiriting:", reply_markup=cancel_button)
    await state.set_state(DelPremiumState.chat_id)


@admin_router.message(DelPremiumState.chat_id)
async def process_remove_premium(message: Message, state: FSMContext):
    chat_id = message.text.strip()
    if not chat_id.isdigit():
        await message.answer("Noto'g'ri chat_id. Iltimos, to'g'ri raqam kiriting:")
        return

    try:
        chat_id = int(chat_id)
        user = await User.get(chat_id=chat_id)
        user.is_premium = False
        await user.save()

        await message.answer(f"Foydalanuvchi (chat_id: {chat_id}) premiumlikdan olib tashlandi.")
    except tortoise.exceptions.DoesNotExist:
        await message.answer("Foydalanuvchi topilmadi.")

    await state.clear()