import time

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import days_to_seconds, db
from tgbot.filters import AdminFilter
from tgbot.misc.keyboards import cancel_inline
from tgbot.misc.states import SubGiftState


async def sub_gift_week(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Введите @username (@ без собачки) или ID пользователя: ',
                                   reply_markup=cancel_inline)
    await SubGiftState.week.set()


async def sub_gift_week_state(message: Message, state: FSMContext):
    time_sub = int(time.time()) + days_to_seconds(7)
    users = db.get_users()
    usernames = db.get_usernames()
    try:
        user_id = int(message.text)
        if user_id not in users:
            await message.bot.send_message(
                message.from_user.id,
                "Такого пользователя нет в базе данных. Пожалуйста, убедитесь, что вы ввели правильный @username или ID пользователя.",
            )
            return await state.finish()
    except Exception as e:
        username = str(message.text)
        if username not in usernames:
            await message.bot.send_message(
                message.from_user.id,
                "Такого пользователя нет в базе данных. Пожалуйста, убедитесь, что вы ввели правильный @username или ID пользователя.",
            )
            return await state.finish()
    db.set_time_sub(message.text, time_sub)
    await message.bot.send_message(message.from_user.id, 'Вы успешно выдали подписку на неделю.')
    return await state.finish()


async def sub_gift_month(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Введите @username (@ без собачки) или ID пользователя: ',
                                   reply_markup=cancel_inline)
    await SubGiftState.month.set()


async def sub_gift_month_state(message: Message, state: FSMContext):
    time_sub = int(time.time()) + days_to_seconds(30)
    users = db.get_users()
    usernames = db.get_usernames()
    try:
        user_id = int(message.text)
        if user_id not in users:
            await message.bot.send_message(
                message.from_user.id,
                "Такого пользователя нет в базе данных. Пожалуйста, убедитесь, что вы ввели правильный @username или ID пользователя.",
            )
            return await state.finish()
    except Exception as e:
        username = str(message.text)
        if username not in usernames:
            await message.bot.send_message(
                message.from_user.id,
                "Такого пользователя нет в базе данных. Пожалуйста, убедитесь, что вы ввели правильный @username или ID пользователя.",
            )
            return await state.finish()
    db.set_time_sub(message.text, time_sub)
    await message.bot.send_message(message.from_user.id, 'Вы успешно выдали подписку на месяц.')
    return await state.finish()


async def sub_gift_three_month(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Введите @username (@ без собачки) или ID пользователя: ',
                                   reply_markup=cancel_inline)
    await SubGiftState.three_month.set()


async def sub_gift_three_month_state(message: Message, state: FSMContext):
    time_sub = int(time.time()) + days_to_seconds(90)
    users = db.get_users()
    usernames = db.get_usernames()
    try:
        user_id = int(message.text)
        if user_id not in users:
            await message.bot.send_message(
                message.from_user.id,
                "Такого пользователя нет в базе данных. Пожалуйста, убедитесь, что вы ввели правильный @username или ID пользователя.",
            )
            return await state.finish()
    except Exception as e:
        username = str(message.text)
        if username not in usernames:
            await message.bot.send_message(
                message.from_user.id,
                "Такого пользователя нет в базе данных. Пожалуйста, убедитесь, что вы ввели правильный @username или ID пользователя.",
            )
            return await state.finish()
    db.set_time_sub(message.text, time_sub)
    await message.bot.send_message(message.from_user.id, 'Вы успешно выдали подписку на 3 месяца.')
    return await state.finish()


async def sub_gift_half_year(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Введите @username (@ без собачки) или ID пользователя: ',
                                   reply_markup=cancel_inline)
    await SubGiftState.half_year.set()


async def sub_gift_half_year_state(message: Message, state: FSMContext):
    time_sub = int(time.time()) + days_to_seconds(180)
    users = db.get_users()
    usernames = db.get_usernames()
    try:
        user_id = int(message.text)
        if user_id not in users:
            await message.bot.send_message(
                message.from_user.id,
                "Такого пользователя нет в базе данных. Пожалуйста, убедитесь, что вы ввели правильный @username или ID пользователя.",
            )
            return await state.finish()
    except Exception as e:
        username = str(message.text)
        if username not in usernames:
            await message.bot.send_message(
                message.from_user.id,
                "Такого пользователя нет в базе данных. Пожалуйста, убедитесь, что вы ввели правильный @username или ID пользователя.",
            )
            return await state.finish()
    db.set_time_sub(message.text, time_sub)
    await message.bot.send_message(message.from_user.id, 'Вы успешно выдали подписку на полгода.')
    return await state.finish()


def register_sub_gift(dp: Dispatcher):
    dp.register_callback_query_handler(
        sub_gift_week, AdminFilter(),
        text='giftweek',
        state='*'
    )
    dp.register_message_handler(
        sub_gift_week_state, AdminFilter(),
        state=SubGiftState.week
    )
    dp.register_callback_query_handler(
        sub_gift_month, AdminFilter(),
        text='giftmonth',
        state='*'
    )
    dp.register_message_handler(
        sub_gift_month_state, AdminFilter(),
        state=SubGiftState.month
    )
    dp.register_callback_query_handler(
        sub_gift_three_month, AdminFilter(),
        text='giftthreemonth',
        state='*'
    )
    dp.register_message_handler(
        sub_gift_three_month_state, AdminFilter(),
        state=SubGiftState.three_month
    )
    dp.register_callback_query_handler(
        sub_gift_half_year, AdminFilter(),
        text='gifthalfyear',
        state='*'
    )
    dp.register_message_handler(
        sub_gift_half_year_state, AdminFilter(),
        state=SubGiftState.half_year
    )

