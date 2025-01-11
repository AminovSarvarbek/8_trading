from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def mainmenu_uz():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Prognoz 📈"),
                KeyboardButton(text="Sozlamalar ⚙️")
            ],
            [
                KeyboardButton(text="Premium 🌟")
            ]
        ],
        resize_keyboard=True
    )

def mainmenu_ru():

    return ReplyKeyboardMarkup(
        keyboard=[
        [
            KeyboardButton(text="Прогноз 📈"),
            KeyboardButton(text="Настройки ⚙️")
        ],
        [
            KeyboardButton(text="Премиум 🌟")
        ]
    ],
        resize_keyboard=True
    )
