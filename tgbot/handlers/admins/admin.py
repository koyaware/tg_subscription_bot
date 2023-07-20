from datetime import datetime

from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import BASE_DIR, db, ADMIN_IDS
from tgbot.filters import AdminFilter
from tgbot.misc.commands import Commands
from tgbot.misc.keyboards import main_info, mainMenuAdmin, adminMenu, rates_inline, mailing_inline, \
    admin_sub_gift_inline, promocode_menu_inline, sub_inline_markup
from tgbot.misc.text import start_message


async def admin_start(message: Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name, datetime.now())
        for admin in ADMIN_IDS:
            await message.bot.send_message(admin, f"🆕 Новый пользователь:"
                                                  f"\nПользователь: @{message.from_user.username}, <b>{message.from_user.first_name}</b>\n"
                                                  f"[ID:{message.from_user.id}] только что зарегестрировался в боте.")
        await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
        with open(BASE_DIR /'contents/info.MP4', 'rb') as gif_file:
            await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenuAdmin)
        await message.bot.send_message(message.from_user.id,
                                       "Выберите желаемый для вас тарифный план: ",
                                       reply_markup=sub_inline_markup)
    else:
        await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
        with open(BASE_DIR / 'contents/info.MP4', 'rb') as gif_file:
            await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenuAdmin)
        await message.bot.send_message(message.from_user.id,
                                       "Выберите желаемый для вас тарифный план: ",
                                       reply_markup=sub_inline_markup)


async def admin_menu(message: Message):
        await message.bot.send_message(message.from_user.id, 'Добро пожаловать в админ панель!\n\nДля перехода в главное меню, отправьте боту команду - /start.', reply_markup=adminMenu)


async def rate_users(message: Message):
    await message.bot.send_message(message.from_user.id, '<b>Меню Блокировки пользователей</b>',
                                   reply_markup=rates_inline)


async def mailing_menu(message: Message):
    await message.bot.send_message(message.from_user.id, 'Выберите группу пользователей для рассылки: ', reply_markup=mailing_inline)


async def sub_gift(message: Message):
    await message.bot.send_message(message.from_user.id, 'Выберите желаемый для вас тарифный план: ', reply_markup=admin_sub_gift_inline)


async def promocode_menu(message: Message):
    await message.bot.send_message(message.from_user.id, 'Выберите меню настроек для промокода: ', reply_markup=promocode_menu_inline)


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
    dp.register_message_handler(
        sub_gift, AdminFilter(),
        text=Commands.admin_sub.value,
        state='*'
    )
    dp.register_message_handler(
        promocode_menu, AdminFilter(),
        text=Commands.promocode_menu.value,
        state='*'
    )