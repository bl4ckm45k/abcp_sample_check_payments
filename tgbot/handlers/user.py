import logging

from aiogram import Dispatcher
from aiogram.types import Message

from loader import dp

logger = logging.getLogger(__name__)


async def start(message: Message):
    await dp.bot.send_message(message.from_user.id,
                              "Привет, я работаю")


async def help_handler(message: Message):
    await dp.bot.send_message(message.from_user.id, text=f'Тут должна быть какая-то информация, кнопки')


async def chat_id_user(message: Message):
    await message.answer(f"chat_id: {message.chat.id}")


def register_user(dp: Dispatcher):
    dp.register_message_handler(start, commands=["start"], state="*")
    dp.register_message_handler(help_handler, commands=["help"], state="*")
    dp.register_message_handler(chat_id_user, commands=["chat_id"], state="*")
