import logging
import sys
import asyncio
from config.db import init_db
from loader import dp, bot, rt, admin_router
import handlers





async def main() -> None:
    # try:
    #      db.create_table_users()
    # except Exception as err:
    #     # print(err)
    #     pass

    await init_db()

    dp.include_routers(rt, admin_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
