import asyncio
import datetime
import logging

from .check_payments import check_online_payments

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def coroutines():
    now_time = datetime.datetime.now().strftime("%H:%M")
    if '08:00' <= now_time <= '21:59':
        update_start = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        update_end = datetime.datetime.now().strftime("%Y-%m-%d")
        asyncio.create_task(check_online_payments(update_start, update_end))
    if now_time == '07:55':
        update_start = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        update_end = datetime.datetime.now().strftime("%Y-%m-%d")
        asyncio.create_task(check_online_payments(update_start, update_end))

