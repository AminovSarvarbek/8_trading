from tradingview_ta import TA_Handler, Interval, Exchange


tesla = TA_Handler(
    symbol="BTCUSD",
    screener="crypto",
    exchange="BINANCE",
    interval=Interval.INTERVAL_1_DAY
)
print(tesla.get_analysis().summary)