from aiogram import Bot, Dispatcher, Router, BaseMiddleware
from utils.lang import LTranslator
from models.user import User


lt = LTranslator(path='locales')

class LangMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data: dict):
        # check message
        if event.message:
            user_id = event.message.from_user.id
            user = await User.get(chat_id=user_id)
            # set the user lang
            lt.add_lang(id=user_id, lang=user.lang)
        return await handler(event, data)