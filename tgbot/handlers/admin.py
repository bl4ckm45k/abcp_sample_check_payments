import logging
import os
from aiogram import Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message
from asyncpg.exceptions import UniqueViolationError

from loader import dp, db, config

logger = logging.getLogger(__name__)


async def chat_id(message: Message):
    await message.answer(f"chat_id: {message.chat.id}")


def register_admin(dp: Dispatcher):
    dp.register_message_handler(chat_id, commands=["chat_id"], state="*", is_admin=True)
