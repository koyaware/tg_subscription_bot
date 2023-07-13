from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.filters import AdminFilter


async def admin_start(message: Message):
    await message.reply('Hello, admin!')


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, AdminFilter(),
        commands=['start'],
        state='*', is_superuser=True,
        commands_prefix='!/'
    )
