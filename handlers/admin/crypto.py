import tortoise
from aiogram import F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from loader import admin_router
from models.crypto import Crypto
from keyboards.inline.cancel import cancel_button
from states.admin import AddCryptoState, DelCryptoState

# Crypto qo'shish
@admin_router.message(F.text == "🪙Add crypto")
async def add_crypto(message: Message, state: FSMContext):
    await message.answer("Iltimos, qo'shmoqchi bo'lgan kriptovalyutaning nomini kiriting:", reply_markup=cancel_button)
    await state.set_state(AddCryptoState.name)


@admin_router.message(AddCryptoState.name)
async def process_crypto_name(message: Message, state: FSMContext):
    crypto_name = message.text.strip()
    await state.update_data(crypto_name=crypto_name)

    await message.answer("Iltimos, kriptovalyutaning simbolini kiriting:")
    await state.set_state(AddCryptoState.symbol)


@admin_router.message(AddCryptoState.symbol)
async def process_crypto_symbol(message: Message, state: FSMContext):
    crypto_symbol = message.text.strip()
    data = await state.get_data()
    crypto_name = data.get("crypto_name")

    await message.answer("Kriptovalyuta premiummi? (yes/no):")
    await state.update_data(crypto_symbol=crypto_symbol)
    await state.set_state(AddCryptoState.is_premium)


@admin_router.message(AddCryptoState.is_premium)
async def process_crypto_is_premium(message: Message, state: FSMContext):
    is_premium_input = message.text.strip().lower()
    data = await state.get_data()
    crypto_name = data.get("crypto_name")
    crypto_symbol = data.get("crypto_symbol")

    # `is_premium` qiymatini belgilash
    is_premium = True if is_premium_input == 'yes' else False

    # Kriptovalyutani yaratish
    try:
        crypto = Crypto(name=crypto_name, symbol=crypto_symbol, is_premium=is_premium)
        await crypto.save()

        await message.answer(f"Kriptovalyuta (nomi: {crypto_name}, simboli: {crypto_symbol}, premium: {is_premium}) muvaffaqiyatli qo'shildi.")
    except Exception as e:
        await message.answer("Kriptovalyutani qo'shishda xatolik yuz berdi.")

    await state.clear()


# Crypto o'chirish
@admin_router.message(F.text == "🗑Remove crypto")
async def remove_crypto(message: Message, state: FSMContext):
    await message.answer("Iltimos, o'chirmoqchi bo'lgan kriptovalyutaning simbolini kiriting:", reply_markup=cancel_button)
    await state.set_state(DelCryptoState.symbol)


@admin_router.message(DelCryptoState.symbol)
async def process_remove_crypto(message: Message, state: FSMContext):
    crypto_symbol = message.text.strip()

    try:
        # Kriptovalyutani simboli orqali olish
        crypto = await Crypto.get(symbol=crypto_symbol)
        await crypto.delete()

        await message.answer(f"Kriptovalyuta (simboli: {crypto_symbol}) muvaffaqiyatli o'chirildi.")
    except tortoise.exceptions.DoesNotExist:
        await message.answer("Kriptovalyuta topilmadi.")

    await state.clear()
