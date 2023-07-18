from datetime import datetime

from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import db, BASE_DIR, time_sub_day
from tgbot.filters.is_ban import IsBanFilter
from tgbot.misc.commands import Commands
from tgbot.misc.keyboards import main_info, mainMenu, sub_inline_markup, cancel_inline, subMenu
from tgbot.misc.states import FeedbackState
from tgbot.misc.text import start_message


async def user_start(message: Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id, message.from_user.username, message.from_user.full_name, datetime.now())
        await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
        with open(BASE_DIR /'contents/info.MP4', 'rb') as gif_file:
            await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenu)
    else:
        if db.get_sub_status(message.from_user.id):
            await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
            with open(BASE_DIR / 'contents/info.MP4', 'rb') as gif_file:
                await message.bot.send_animation(message.chat.id, gif_file, reply_markup=subMenu)
        else:
            await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
            with open(BASE_DIR /'contents/info.MP4', 'rb') as gif_file:
                await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenu)


async def bot_message(message: Message):
    if message.chat.type == 'private':
        if message.text == '💻 Мои подписки':
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            if user_sub is False:
                user_sub = "<b>Нет</b>"
            user_sub = "\nПодписка: " + user_sub
            await message.bot.send_message(message.from_user.id, user_sub)
        elif message.text == '❤ Тарифы':
            await message.bot.send_message(message.from_user.id,
                                   "Выберите желаемый для вас тарифный план: ",
                                   reply_markup=sub_inline_markup)
        elif message.text == '📨 Обратная связь':
            await message.bot.send_message(message.from_user.id, "Задайте ваш вопрос текстом, фотографией или любым другим медиавложением: ", reply_markup=cancel_inline)
            await FeedbackState.waiting_for_message.set()
        elif message.text == '📨 Чат':
            if db.get_sub_status(message.from_user.id):
                await message.bot.send_message(message.from_user.id, "Вы получили приглашение в канал/чат 👇\n"
                                                                     "<b>- ТРАНСФЕР-МОСТ Заказы</b>\n"
                                                                     "https://t.me/+VHuzPV-cvZlkZWQy")
            else:
                await message.bot.send_message(message.from_user.id, "<b>У вас нет активных подписок!</b>")


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start, IsBanFilter(),
        text=["/start", Commands.come_back.value],
        state="*",
    )
    dp.register_message_handler(
        bot_message, IsBanFilter(), state="*"
    )