import requests
import pandas as pd
import mplfinance as mpf
from binance.client import Client
from data.config import API_KEY, SECRET_KEY
from tradingview_ta import TA_Handler, Interval, Exchange


def get_coingecko_data(symbol, vs_currency, days, interval):
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart"
    params = {
        "vs_currency": vs_currency,
        "days": days}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error: {response.status_code}, {response.text}")
        return pd.DataFrame()

    data = response.json()
    if "prices" not in data or "market_caps" not in data or "total_volumes" not in data:
        print("Error: Required data not found in response")
        return pd.DataFrame()

    prices = data["prices"]
    volumes = data["total_volumes"]

    df = pd.DataFrame(prices, columns=["timestamp", "close"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["close"] = df["close"].astype(float)

    df["open"] = df["close"].shift(1)
    df["high"] = df["close"].rolling(2).max()
    df["low"] = df["close"].rolling(2).min()
    df["volume"] = [v[1] for v in volumes]
    df = df.dropna()
    df.set_index("timestamp", inplace=True)

    df_resampled = df.resample(interval).agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum",
    }).dropna()

    return df_resampled





def get_binance_data(symbol, interval, limit):
    """
        binance api dan malumotlar olish

    """
    client = Client(API_KEY, SECRET_KEY)
    klines = client.get_klines(symbol=symbol, interval=interval, limit=limit)

    # DataFrame yaratish
    df = pd.DataFrame(klines, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "number_of_trades",
        "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume", "ignore"
    ])

    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df["open"] = df["open"].astype(float)
    df["high"] = df["high"].astype(float)
    df["low"] = df["low"].astype(float)
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)

    df = df[["timestamp", "open", "high", "low", "close", "volume"]]

    # df["timestamp"] = df["timestamp"].dt.strftime("%m-%d")

    df.set_index("timestamp", inplace=True)

    return df

def get_tradingv_data():
    tesla = TA_Handler(
        symbol="TSLA",
        screener="america",
        exchange="NASDAQ",
        interval=Interval.INTERVAL_1_DAY
    )
    print(tesla.get_analysis().summary)
# Example output: {"RECOMMENDATION": "BUY", "BUY": 8, "NEUTRAL": 6, "SELL": 3}


