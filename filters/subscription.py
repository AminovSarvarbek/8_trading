from aiogram.filters import BaseFilter
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.exceptions import TelegramAPIError

from models.channel import Channel


class SubscriptionFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        channels = await Channel.all()  # Kanallar ro'yxatini olish (DB dan olingan ma'lumot)
        unsubscribed_channels = []  # Obuna bo'lmagan kanallarni saqlash uchun
        print('(((((((((((((((())))))))))))))))')
        for channel in channels:
            try:
                # Foydalanuvchini kanalga obuna bo'lganligini tekshirish
                member = await message.bot.get_chat_member(chat_id=-int(channel.chat_id), user_id=message.from_user.id)
                if member.status not in ("member", "administrator", "creator"):
                    print("+++")
                    unsubscribed_channels.append(channel)
            except ZeroDivisionError:
                continue

        if unsubscribed_channels:
            # Obuna bo'lmagan kanallar ro'yxati mavjud bo'lsa
            keyboards = []
            for channel in unsubscribed_channels:
                chat_id = channel.chat_id

                try:
                    # Kanal ma'lumotlarini olish
                    chat = await message.bot.get_chat(-int(chat_id))
                    invite_link = chat.invite_link  # Kanalning "invite link"i
                except Exception as e:
                    print(f"Kanal uchun invite linkni olishda xatolik yuz berdi: {e}")
                    invite_link = None

                if invite_link:
                    keyboards.append(
                        InlineKeyboardButton(text="Obuna bo'lish🔗", url=invite_link)
                    )

            if keyboards:
                await message.answer(
                    "📢 Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
                    reply_markup=InlineKeyboardMarkup(
                        inline_keyboard=[
                            keyboards
                        ]
                    )
                )
            return False

        return True