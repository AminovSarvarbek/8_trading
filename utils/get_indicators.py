import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

x = np.arange(1, 11)  # 10 kunlik vaqt
y = np.array([100, 102, 104, 103, 105, 107, 108, 110, 112, 115])  # Narxlar

# Parametrlar
future_days = 5
entry_price = 108
stop_loss = 105
take_profit = 115

plt.figure(figsize=(12, 6))
plt.plot(x, y, label="Narx harakati", color="blue")  # Asosiy narx harakati

future_x = np.arange(x[-1] + 1, x[-1] + 1 + future_days)  # 5 kunlik bo'sh joy
plt.gca().add_patch(Rectangle((future_x[0], stop_loss), future_days, take_profit - stop_loss,
                              color='orange', alpha=0.3, label="Tahlil zonasi"))

plt.axhline(y=stop_loss, color='red', linestyle='--', label='Stop Loss')
plt.axhline(y=entry_price, color='blue', linestyle='--', label='Entry')
plt.axhline(y=take_profit, color='green', linestyle='--', label='Take Profit')

plt.xlabel("Kunlar")
plt.ylabel("Narxlar")
plt.title("Keyingi 5 kunlik zonalar bilan tahlil")
plt.legend()
plt.grid()
plt.show()
