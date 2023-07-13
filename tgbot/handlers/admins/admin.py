from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import BASE_DIR
from tgbot.filters import AdminFilter
from tgbot.misc.keyboards import main_info, mainMenu
from tgbot.misc.text import start_message


async def admin_start(message: Message):
    await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
    with open(BASE_DIR / 'contents/info.MP4', 'rb') as gif_file:
        await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenu)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, AdminFilter(),
        commands=['start'],
        state='*', is_superuser=True,
        commands_prefix='!/'
    )
