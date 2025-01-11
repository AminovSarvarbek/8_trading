from aiogram.fsm.state import State, StatesGroup


class NotificationState(StatesGroup):
    text = State()