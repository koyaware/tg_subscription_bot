from datetime import datetime

from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import db, BASE_DIR, time_sub_day, ADMIN_IDS
from tgbot.filters.is_ban import IsBanFilter
from tgbot.misc.commands import Commands
from tgbot.misc.keyboards import main_info, mainMenu, sub_inline_markup, cancel_inline, subMenu, sub_link_inline
from tgbot.misc.states import FeedbackState
from tgbot.misc.text import start_message


async def user_start(message: Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name, datetime.now())
        for admin in ADMIN_IDS:
            await message.bot.send_message(admin, f"🆕 Новый пользователь:"
                                                  f"\n\nПользователь: @{message.from_user.username}, <b>{message.from_user.first_name}</b>\n"
                                                  f"[ID:{message.from_user.id}] только что зарегестрировался в боте.")
        await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
        with open(BASE_DIR /'contents/info.MP4', 'rb') as gif_file:
            await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenu)
        await message.bot.send_message(message.from_user.id,
                                       "Выберите желаемый для вас тарифный план: ",
                                       reply_markup=sub_inline_markup)
    else:
        if db.get_sub_status(message.from_user.id):
            await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
            with open(BASE_DIR / 'contents/info.MP4', 'rb') as gif_file:
                await message.bot.send_animation(message.chat.id, gif_file, reply_markup=subMenu)
        else:
            await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
            with open(BASE_DIR /'contents/info.MP4', 'rb') as gif_file:
                await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenu)
            await message.bot.send_message(message.from_user.id,
                                           "Выберите желаемый для вас тарифный план: ",
                                           reply_markup=sub_inline_markup)


async def user_subs(message: Message):
    user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
    if user_sub is False:
        user_sub = "<b>Нет</b>"
        user_sub = "\nПодписка: " + user_sub
        return await message.bot.send_message(message.from_user.id, f'📊 Информация о купленных подписках:\n'
                                                             f'👥 <b>ТРАНСФЕР-МОСТ Заказы</b>-{user_sub}',
                                              reply_markup=sub_inline_markup)
    user_sub = "\nПодписка: " + f'<b>{user_sub}</b>'
    await message.bot.send_message(message.from_user.id, f'📊 Информация о купленных подписках:\n'
                                                         f'👥 <b>ТРАНСФЕР-МОСТ Заказы</b>-{user_sub}',
                                   reply_markup=sub_link_inline)


async def user_rates(message: Message):
    await message.bot.send_message(message.from_user.id,
                                   "Выберите желаемый для вас тарифный план: ",
                                   reply_markup=sub_inline_markup)


async def user_feedback(message: Message):
    await message.bot.send_message(message.from_user.id,
                                   "Задайте ваш вопрос текстом, фотографией или любым другим медиавложением: ",
                                   reply_markup=cancel_inline)
    await FeedbackState.waiting_for_message.set()


async def sub_chat(message: Message):
    if db.get_sub_status(message.from_user.id):
        await message.bot.send_message(message.from_user.id, "Вы получили приглашение в канал/чат 👇\n"
                                                             "<b>- ТРАНСФЕР-МОСТ Заказы</b>",
                                       reply_markup=sub_link_inline)
    else:
        await message.bot.send_message(message.from_user.id, "<b>У вас нет активных подписок!</b>")


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start, IsBanFilter(),
        text=["/start", Commands.come_back.value],
        state="*",
    )
    dp.register_message_handler(
        user_subs, IsBanFilter(), text=Commands.my_profile.value,
        state="*"
    )
    dp.register_message_handler(
        user_rates, IsBanFilter(), text=Commands.my_subs.value,
        state="*"
    )
    dp.register_message_handler(
        user_feedback, IsBanFilter(), text=Commands.feedback.value,
        state="*"
    )
    dp.register_message_handler(
        sub_chat, IsBanFilter(), text=Commands.chat.value,
        state="*"
    )