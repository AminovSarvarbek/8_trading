from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Prognoz 📈"),
                KeyboardButton(text="Sozlamalar ⚙️")
            ],
            [
                KeyboardButton(text="➕Add admin"),
                KeyboardButton(text="➖Remove admin")
            ],
            [
                KeyboardButton(text="➕Add channel"),
                KeyboardButton(text="➖Remove channel") 
            ],
            [
                KeyboardButton(text="🪙Add crypto"),
                KeyboardButton(text="🗑Remove crypto") 
            ],
            [
                KeyboardButton(text="🌟Add Premium"),
                KeyboardButton(text="🗑Remove Premium")
            ],
            [
                KeyboardButton(text="📲 Reklama"),
            ]
        ],
        resize_keyboard=True
    )
