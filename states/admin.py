from aiogram.fsm.state import State, StatesGroup

class AddAdminState(StatesGroup):
    chat_id = State()

class DelAdminState(StatesGroup):
    chat_id = State()

class AdProcess(StatesGroup):
    text = State()
    media = State()


class AddChannelState(StatesGroup):
    chat_id = State()

class DelChannelState(StatesGroup):
    chat_id = State()


class AddPremiumState(StatesGroup):
    chat_id = State()

class DelPremiumState(StatesGroup):
    chat_id = State()


class AddCryptoState(StatesGroup):
    name = State()
    symbol = State()
    is_premium = State()

class DelCryptoState(StatesGroup):
    symbol = State()