import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from tgbot.config import connect_to_redis, db
from tgbot.filters import AdminFilter
from tgbot.misc.keyboards import cancel_inline
from tgbot.misc.states import RatesState


async def ban_user(call: CallbackQuery, state: FSMContext):
    redis_pool = await connect_to_redis()
    user_id = await redis_pool.get(name='user_id')
    numbers_only = re.sub(r'\D', '', user_id.decode())
    await state.finish()
    db.set_ban_status(numbers_only, 1)
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(call.from_user.id, "Пользователь был успешно забанен.")


async def ban_user_id(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Введите @username (@ без собачки) или ID пользователя: ', reply_markup=cancel_inline)
    await RatesState.ban_id.set()


async def ban_user_id_state(message: Message, state: FSMContext):
    db.set_ban_status(message.text, 1)
    await message.bot.send_message(message.from_user.id, "Пользователь был успешно забанен.")
    await state.finish()


async def unban_user(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, 'Введите @username (@ без собачки) или ID пользователя: ', reply_markup=cancel_inline)
    await RatesState.message.set()


async def unban_user_state(message: Message, state: FSMContext):
    db.set_ban_status(message.text, 0)
    await message.bot.send_message(message.from_user.id, "Пользователь был успешно разбанен.")
    await state.finish()


async def banned_users(call: CallbackQuery):
    banned_users = db.get_ban_users()
    if not banned_users:
        return await call.bot.send_message(call.from_user.id, "<b>Нет заблокированных пользователей.</b>")
    else:
        for user in banned_users:
            formatted_user = f"Заблокированный пользователь: \n{user}"
            await call.bot.send_message(call.from_user.id, formatted_user)


def register_rates(dp: Dispatcher):
    dp.register_callback_query_handler(
        ban_user, AdminFilter(),
        text='ban_user',
        state='*'
    )
    dp.register_callback_query_handler(
        ban_user_id, AdminFilter(),
        text='ban_user_id',
        state='*'
    )
    dp.register_message_handler(
        ban_user_id_state, AdminFilter(),
        state=RatesState.ban_id
    )
    dp.register_callback_query_handler(
        unban_user, AdminFilter(),
        text='unban_user',
        state='*'
    )
    dp.register_message_handler(
        unban_user_state, AdminFilter(),
        state=RatesState.message
    )
    dp.register_callback_query_handler(
        banned_users, AdminFilter(),
        text='banned_user',
        state='*'
    )