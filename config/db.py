from tortoise import Tortoise
from data.config import DB_URL


TORTOISE_ORM = {
    "connections": {"default": DB_URL},  # Boshqa DB URL'ni kiriting, masalan PostgreSQL
    "apps": {
        "models": {
            "models": ["models.user", "models.channel","models.crypto", "aerich.models"],  # O'zingizning model va aerichni qo'shing
            "default_connection": "default",
        },
    },
}


async def init_db() -> None:
    await Tortoise.init(
        db_url=DB_URL,
        modules={"models": ["models.user","models.channel","models.crypto"]}  # Tortoise modeli uchun to‘g‘ri modul nomi
    )
    await Tortoise.generate_schemas()