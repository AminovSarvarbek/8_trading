import tortoise
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loader import admin_router
from models.user import User
from keyboards.inline.cancel import cancel_button
from states.admin import AddAdminState, DelAdminState


@admin_router.message(F.text == "➕Add admin")
async def add_admin(message: Message, state: FSMContext):
    await message.answer("Iltimos, admin qilmoqchi bo'lgan foydalanuvchining chat_id raqamini kiriting:", reply_markup=cancel_button)
    await state.set_state(AddAdminState.chat_id)


@admin_router.message(AddAdminState.chat_id)
async def process_admin_id(message: Message, state: FSMContext):
    chat_id = message.text.strip()
    if not chat_id.isdigit():
        await message.answer("Noto'g'ri chat_id. Iltimos, to'g'ri raqam kiriting:")
        return

    try:
        chat_id = int(chat_id)
        user = await User.get(chat_id=chat_id)
        user.is_admin = True
        await user.save()

        await message.answer(f"Foydalanuvchi (chat_id: {chat_id}) admin qilib belgilandi.")
    except tortoise.exceptions.DoesNotExist:
        await message.answer("Foydalanuvchi topilmadi.")

    await state.clear()


# Admin delete
@admin_router.message(F.text == "➖Remove admin")
async def remove_admin(message: Message, state: FSMContext):
    await message.answer("Iltimos, adminlikni olib tashlamoqchi bo'lgan foydalanuvchining chat_id raqamini kiriting:", reply_markup=cancel_button)
    await state.set_state(DelAdminState.chat_id)


@admin_router.message(DelAdminState.chat_id)
async def process_remove_admin(message: Message, state: FSMContext):
    chat_id = message.text.strip()
    if not chat_id.isdigit():
        await message.answer("Noto'g'ri chat_id. Iltimos, to'g'ri raqam kiriting:")
        return

    try:
        chat_id = int(chat_id)
        user = await User.get(chat_id=chat_id)
        user.is_admin = False
        await user.save()

        await message.answer(f"Foydalanuvchi (chat_id: {chat_id}) adminlikdan olib tashlandi.")
    except tortoise.exceptions.DoesNotExist:
        await message.answer("Foydalanuvchi topilmadi.")

    await state.clear()