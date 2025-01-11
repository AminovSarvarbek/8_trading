import requests
from aiogram.types import FSInputFile
from loader import rt, bot
from aiogram import types, F
from utils.get_data import get_binance_data, get_tradingv_data
from data.config import API_KEY, SECRET_KEY


@rt.message(F.text=="/getbnc")
async def send_ready_image(message: types.Message):
    # df = get_binance_data(symbol="BTCUSDT", interval="1h")
    await message.answer(f"{get_tradingv_data()}")

