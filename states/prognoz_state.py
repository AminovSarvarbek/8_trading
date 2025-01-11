from aiogram.fsm.state import State, StatesGroup

class GetCoinTypeUz(StatesGroup):
    coin = State()
    interval = State()
class GetCoinTypeRu(StatesGroup):
    coin = State()
    interval = State()