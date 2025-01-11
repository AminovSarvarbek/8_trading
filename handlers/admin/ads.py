from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery

from loader import admin_router
from keyboards.inline.cancel import cancel_button
from states.admin import AdProcess
from models.user import User

# Reklamalarni barcha foydalanuvchilarga yuborish funksiyasi
async def send_admin_ads(bot: any, ad_text: str, media: str = None, media_type: str = None):
    users = await User.all()  # Barcha foydalanuvchilarni bazadan olish
    for user in users:
        try:
            if media_type == "image":
                await bot.send_photo(user.chat_id, media, caption=ad_text)
            elif media_type == "video":
                await bot.send_video(user.chat_id, media, caption=ad_text)
            elif media_type == "document":
                await bot.send_document(user.chat_id, media, caption=ad_text)
            else:  # Default holatda matnli xabar yuborish
                await bot.send_message(user.chat_id, ad_text)
        except Exception as e:
            print(f"Reklamani {user.chat_id} ga yuborishda xatolik yuz berdi: {e}")

# "📲 Reklama yuborish" jarayonini boshlash
@admin_router.message(F.text == "📲 Reklama")
async def start_sending_ads(message: Message, state: FSMContext):
    await message.answer("Iltimos, reklamani matnini yuboring: ", reply_markup=cancel_button)
    await state.set_state(AdProcess.text)

# Adminning matnli reklamasini olish
@admin_router.message(AdProcess.text)
async def get_ad_text(message: Message, state: FSMContext):
    await state.update_data(ad_text=message.text)
    await message.answer("Endi esa media faylni yuboring (rasm, video yoki hujjat)", reply_markup=cancel_button)
    await state.set_state(AdProcess.media)

# Admindan media faylni qabul qilish
@admin_router.message(AdProcess.media, F.content_type.in_({"photo", "video", "document"}))
async def get_ad_media(message: Message, state: FSMContext):
    media_type = None
    media = None

    # Media turini aniqlash
    if message.photo:
        media = message.photo[-1].file_id
        media_type = "image"
    elif message.video:
        media = message.video.file_id
        media_type = "video"
    elif message.document:
        media = message.document.file_id
        media_type = "document"

    await state.update_data(media=media, media_type=media_type)
    user_data = await state.get_data()
    
    ad_text = user_data["ad_text"]
    media = user_data.get("media")
    media_type = user_data.get("media_type")

    await message.answer("✅ Reklama qabul qilindi! Endi barcha foydalanuvchilarga yuborilmoqda.")

    # Reklamani barcha foydalanuvchilarga yuborish
    await send_admin_ads(message.bot, ad_text, media, media_type)

    await state.clear()
    await message.answer("📩 Reklamalar barcha foydalanuvchilarga yuborildi!")

# Mediani o'tkazib yuborishni boshqarish
@admin_router.message(AdProcess.media)
async def skip_media(message: Message, state: FSMContext):
    user_data = await state.get_data()
    ad_text = user_data["ad_text"]

    await message.answer("❌ Media fayl yuborilmadi! Reklama faqat matn sifatida yuboriladi.", reply_markup=cancel_button)

    # Reklamani barcha foydalanuvchilarga yuborish
    await send_admin_ads(message.bot, ad_text)

    await state.clear()
    await message.answer("📩 Reklamalar barcha foydalanuvchilarga yuborildi!")
