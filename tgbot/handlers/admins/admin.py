from datetime import datetime

from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import BASE_DIR, db
from tgbot.filters import AdminFilter
from tgbot.misc.commands import Commands
from tgbot.misc.keyboards import main_info, mainMenuAdmin, adminMenu, rates_inline, mailing_inline
from tgbot.misc.text import start_message


async def admin_start(message: Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name, datetime.now())
        await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
        with open(BASE_DIR /'contents/info.MP4', 'rb') as gif_file:
            await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenuAdmin)
    else:
        await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
        with open(BASE_DIR / 'contents/info.MP4', 'rb') as gif_file:
            await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenuAdmin)
        await message.bot.send_message(message.from_user.id, 'ПРИВЕТ АДМИН!')


async def admin_menu(message: Message):
        await message.bot.send_message(message.from_user.id, 'Добро пожаловать в админ панель!\n\nДля перехода в главное меню, отправьте боту команду - /start.', reply_markup=adminMenu)


async def rate_users(message: Message):
    await message.bot.send_message(message.from_user.id, '<b>Меню Блокировки пользователей</b>',
                                   reply_markup=rates_inline)


async def mailing_menu(message: Message):
    await message.bot.send_message(message.from_user.id, 'Выберите группу пользователей для рассылки: ', reply_markup=mailing_inline)


def register_admin(dp: Dispatcher):
    dp.register_message_handler(
        admin_start, AdminFilter(),
        text=['/start', Commands.come_back.value],
        state='*',
    )
    dp.register_message_handler(
        admin_menu, AdminFilter(),
        text=Commands.admin_menu.value,
        state='*'
    )
    dp.register_message_handler(
        rate_users, AdminFilter(),
        text=Commands.rates.value,
        state='*'
    )
    dp.register_message_handler(
        mailing_menu, AdminFilter(),
        text=Commands.mailing.value,
        state='*'
    )