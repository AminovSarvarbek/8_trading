from aiogram import Bot, Dispatcher, Router
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from filters.admin import IsAdmin
from filters.subscription import SubscriptionFilter
from filters.lang import LangMiddleware, lt
from data import config

# Routerlar
rt = Router()
admin_router = Router()  # Faqat adminlar uchun router
dp = Dispatcher()  # Asosiy dispatcher
bot = Bot(
    token=config.BOT_TOKEN,
    session=AiohttpSession(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Middleware va filterlarni alohida bog'lash
dp.update.middleware(LangMiddleware())  # Asosiy dispatcherga lang middleware
rt.message.filter(SubscriptionFilter())  # Faqat asosiy dispatcher uchun subscription filtri

admin_router.message.filter(IsAdmin())  # Admin router uchun faqat IsAdmin filtri

# Admin routerni dispatcherga qo'shish
