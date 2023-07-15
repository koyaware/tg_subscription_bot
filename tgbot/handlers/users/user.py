from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.config import db, BASE_DIR, time_sub_day
from tgbot.misc.keyboards import main_info, mainMenu, sub_inline_markup, cancel_inline
from tgbot.misc.states import FeedbackState
from tgbot.misc.text import start_message


async def user_start(message: Message):
    if (not db.user_exists(message.from_user.id)):
        db.add_user(message.from_user.id)
        await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
        with open(BASE_DIR /'contents/info.MP4', 'rb') as gif_file:
            await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenu)
    else:
        await message.bot.send_message(message.from_user.id, text=start_message, reply_markup=main_info)
        with open(BASE_DIR /'contents/info.MP4', 'rb') as gif_file:
            await message.bot.send_animation(message.chat.id, gif_file, reply_markup=mainMenu)


async def bot_message(message: Message):
    if message.chat.type == 'private':
        if message.text == '💻 Мои подписки':
            user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
            if user_sub == False:
                user_sub = "Нет"
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
                await message.bot.send_message(message.from_user.id, "Чат для донатеров")
            else:
                await message.bot.send_message(message.from_user.id, "Купите тариф!")


def register_user(dp: Dispatcher):
    dp.register_message_handler(
        user_start, commands=["start"],
        state="*", commands_prefix='!/'
    )
    dp.register_message_handler(
        bot_message, state="*"
    )