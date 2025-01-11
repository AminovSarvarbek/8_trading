import os
import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
from aiogram import types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from loader import rt, bot, lt
from keyboards.inline.cryptocurrencies_4 import crypto, candlestick_interval
from states.prognoz_state import GetCoinTypeUz
from models.user import User
from models.crypto import Crypto
from utils.get_data import get_binance_data


# Prognoz boshlash komandasi
@rt.message(F.text == 'Prognoz 📈')
@rt.message(F.text == "Прогноз 📈")
async def get_analiz(message: types.Message, state: FSMContext):
    # Lokalizatsiyalangan matnni yuklash
    msg = lt._(id=message.chat.id, key="prognoz")
    await message.answer(msg, reply_markup=await crypto())  # Tugmalarni olish
    await state.set_state(GetCoinTypeUz.coin)

# Kriptovalyuta turini saqlash
@rt.callback_query(GetCoinTypeUz.coin)
async def coin_type_saveuz(call: types.CallbackQuery, state: FSMContext):
    user = await User.get(chat_id=call.message.chat.id)
    crypto = await Crypto.get(symbol=call.data)

    # Check if the user is premium or the crypto is not premium
    if crypto.is_premium and not user.is_premium:
        await call.message.answer(lt._(id=call.message.chat.id, key="none_premium_message"))
        await state.clear()
        return

    # Send the message for both cases (premium user with premium crypto or non-premium crypto)
    await bot.send_message(
        chat_id=call.from_user.id,
        text=lt._(id=call.message.chat.id, key="coin_time_choose_message"),
        reply_markup=candlestick_interval()
    )
    await state.update_data(coin=call.data)
    await call.answer(cache_time=60)
    await call.message.delete()
    await state.set_state(GetCoinTypeUz.interval)

# Interval tanlash va grafik yaratish
@rt.callback_query(GetCoinTypeUz.interval)
async def interval_candle(call: types.CallbackQuery, state: FSMContext):
    await call.answer(cache_time=60)
    await call.message.delete()

    # Holat (state) dan coin va intervalni o'qiymiz
    data = await state.get_data()
    coin = data.get("coin", "BTCUSDT")  # Default qiymat BTCUSDT
    interval = call.data  # Foydalanuvchi tanlagan interval
    days = 7  # O'tgan kunlar soni
    additional_days = 10  # Kelajak kunlar soni
    await state.clear()

    # Tasdiqlash xabarini yuborish
    msg = lt._(
        id=call.message.chat.id,
        key="accept_interval_candle"
    ).format(coin=coin, interval=interval, days=days)
    await bot.send_message(chat_id=call.from_user.id, text=msg)

    # Limitni aniqlash (intervalga qarab)
    limit = {
        "4h": days * 6,
        "2h": days * 12,
    }.get(interval, days * 24)

    # Binance dan ma'lumotlarni olish
    df = get_binance_data(symbol=coin, interval=interval, limit=limit)

    if df.empty:
        await bot.send_message(chat_id=call.from_user.id, text="Ma'lumotlarni olishda xatolik yuz berdi.")
        return

    # Yopilish narxiga asoslangan kirish, stop-loss va take-profit qiymatlari
    latest_close = df["close"].iloc[-1]
    entry_price = latest_close
    stop_loss = entry_price * 0.98  # 2% pasayish
    take_profit = entry_price * 1.05  # 5% oshish

    # Kelajak kunlar uchun bo'sh DataFrame yaratish va birlashtirish
    last_date = df.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=additional_days)
    empty_df = pd.DataFrame(index=future_dates, columns=df.columns)
    df = pd.concat([df, empty_df])

    # Har bir foydalanuvchi uchun noyob fayl nomi yaratish
    file_path = f"trend_{call.from_user.id}.png"

    # Kandl grafik (candlestick chart) yaratish
    fig, axlist = mpf.plot(
        df,
        type="candle",
        style="yahoo",
        title=f"{coin} - {interval}",
        ylabel="Price (K USD)",
        figsize=(12, 6),
        returnfig=True
    )

    # O'qlarni formatlash
    axlist[0].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x / 1000)}K"))
    plt.setp(axlist[0].xaxis.get_majorticklabels(), rotation=0, ha="right")

    # Grafikka saqlash
    fig.savefig(file_path, bbox_inches="tight")
    plt.close(fig)

    # Grafikni yuborish
    fl = FSInputFile(file_path)
    caption = (
        f"📊 Candlestick Chart\n"
        f"Entry Price: {entry_price:.2f} USD\n"
        f"Stop Loss: {stop_loss:.2f} USD\n"
        f"Take Profit: {take_profit:.2f} USD"
    )
    await bot.send_photo(chat_id=call.from_user.id, photo=fl, caption=caption)

    # Faylni o'chirish
    if os.path.exists(file_path):
        os.remove(file_path)