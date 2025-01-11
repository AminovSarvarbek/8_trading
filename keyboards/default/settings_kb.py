from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def settings_btns_uz():
    keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Til 🇺🇿"),
            KeyboardButton(text="Bildirishnoma 💬")
        ],
        [
            KeyboardButton(text="⬅️ Orqaga")
        ]
    ],
        resize_keyboard=True
    )
    return keyboard

def settings_btns_ru():
    keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Язык 🇷🇺"),
            KeyboardButton(text="Уведомление 💬")
        ],
        [
            KeyboardButton(text="⬅️ Назад")
        ]
    ],
        resize_keyboard=True
    )
    return keyboard
