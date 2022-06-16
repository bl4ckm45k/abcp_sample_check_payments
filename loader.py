from aioabcpapi import AdminApi
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from config import load_config
from database import Database

config = load_config(".env")
db = Database(config.db)
bot = Bot(token=config.tg_bot.token, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2()
dp = Dispatcher(bot, storage=storage)
api = AdminApi(config.abcp.host, config.abcp.login, config.abcp.password)
