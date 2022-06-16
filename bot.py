import asyncio
import logging

from abcp.run_coroutines import coroutines
from loader import api, db
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.error_handler import register_error_handler
from tgbot.handlers.user import register_user

logger = logging.getLogger(__name__)

DELAY = 60


def repeat_start():
    _loop = asyncio.get_running_loop()
    asyncio.ensure_future(coroutines(), loop=_loop)
    _loop.call_later(DELAY, repeat_start)


def register_all_middlewares(dp):
    pass


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)
    register_user(dp)
    register_error_handler(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    from loader import dp, bot
    register_all_middlewares(dp)
    register_all_filters(dp)
    register_all_handlers(dp)

    # start
    try:
        await db.create_tables()
        asyncio.get_running_loop().call_later(DELAY, repeat_start)
        await dp.start_polling()

    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()
        await api.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
