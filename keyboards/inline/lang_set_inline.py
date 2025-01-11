from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def lang_set():
    keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="UZ🇺🇿", callback_data="uz_lang"),
            InlineKeyboardButton(text="RU🇷🇺", callback_data="ru_lang")
        ]])
    return keyboard