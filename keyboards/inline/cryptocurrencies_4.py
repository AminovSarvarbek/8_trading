from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from models.crypto import Crypto


async def crypto():
    # Crypto modelidan kriptovalyutalarni olish
    cryptos = await Crypto.all()
    
    # Tugmalarni qatorlar bilan tashkil qilish
    buttons = []
    row = []
    
    for crypto in cryptos:
        row.append(InlineKeyboardButton(text=crypto.name, callback_data=crypto.symbol))
        
        # Har bir 3 ta tugmadan keyin yangi qatorni yaratamiz
        if len(row) == 3:
            buttons.append(row)
            row = []  # Yangi qator uchun bo'shatamiz
    
    # Qolgan tugmalarni qo'shamiz (agar qator to'ldirilmagan bo'lsa)
    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

def candlestick_interval():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="1H", callback_data="1h"),
                InlineKeyboardButton(text="2H", callback_data="2h"),
                InlineKeyboardButton(text="4H", callback_data="4h")
            ]
        ]
    )
