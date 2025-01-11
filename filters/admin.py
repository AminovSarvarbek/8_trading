from typing import List
from aiogram.filters import BaseFilter
from aiogram.types import Message

from models.user import User


class IsAdmin(BaseFilter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        print('+++')
        user = await User.get(chat_id=message.chat.id)
        return user.is_admin