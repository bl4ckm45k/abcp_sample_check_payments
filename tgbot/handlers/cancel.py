from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from loader_bot import bot


async def cancel_callback(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer('Отмена действия')
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()


async def cancel(message: Message, state: FSMContext):
    await message.answer('Отмена действия')
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()


def register_cancel(dp: Dispatcher):
    dp.register_message_handler(cancel, commands=["cancel"], state="*")


def register_cancel_callback(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_callback, lambda c: c.data == 'cancel', state='*')
