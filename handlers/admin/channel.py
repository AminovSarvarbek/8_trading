import tortoise
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loader import admin_router
from models.channel import Channel
from keyboards.inline.cancel import cancel_button
from states.admin import AddChannelState, DelChannelState


@admin_router.message(F.text == "➕Add channel")
async def add_channel(message: Message, state: FSMContext):
    await message.answer("Iltimos, qo'shmoqchi bo'lgan kanalning chat_id raqamini kiriting:", reply_markup=cancel_button)
    await state.set_state(AddChannelState.chat_id)


@admin_router.message(AddChannelState.chat_id)
async def process_add_channel(message: Message, state: FSMContext):
    chat_id = message.text.strip()
    if not chat_id.isdigit():
        await message.answer("Noto'g'ri chat_id. Iltimos, to'g'ri raqam kiriting:")
        return

    try:
        chat_id = int(chat_id)
        channel, created = await Channel.get_or_create(chat_id=chat_id)

        if created:
            await message.answer(f"Kanal (chat_id: {chat_id}) muvaffaqiyatli qo'shildi.")
        else:
            await message.answer(f"Kanal (chat_id: {chat_id}) allaqachon mavjud.")
    except Exception as e:
        await message.answer(f"Kanalni qo'shishda xatolik yuz berdi: {e}")

    await state.clear()


# Remove channel
@admin_router.message(F.text == "➖Remove channel")
async def remove_channel(message: Message, state: FSMContext):
    await message.answer("Iltimos, olib tashlamoqchi bo'lgan kanalning chat_id raqamini kiriting:", reply_markup=cancel_button)
    await state.set_state(DelChannelState.chat_id)


@admin_router.message(DelChannelState.chat_id)
async def process_remove_channel(message: Message, state: FSMContext):
    chat_id = message.text.strip()
    if not chat_id.isdigit():
        await message.answer("Noto'g'ri chat_id. Iltimos, to'g'ri raqam kiriting:")
        return

    try:
        chat_id = int(chat_id)
        channel = await Channel.get(chat_id=chat_id)
        await channel.delete()

        await message.answer(f"Kanal (chat_id: {chat_id}) muvaffaqiyatli olib tashlandi.")
    except tortoise.exceptions.DoesNotExist:
        await message.answer("Kanal topilmadi.")

    await state.clear()
