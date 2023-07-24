import time

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

from tgbot.config import db
from tgbot.filters.is_ban import IsBanFilter
from tgbot.misc.keyboards import sub_link_private_inline, sub_link_open_inline


async def sub_link_private(call: CallbackQuery):
    if db.get_sub_status(call.from_user.id):
        await call.bot.edit_message_text("<b>Ваши приватные ссылки для доступа</b> 👇\n\n"
                                         "<code>⚠ Если у вас появляется ошибка ссылка не действительна"
                                         " или чат не существует или вы не можете войти "
                                         "в сообщество, просто попробуйте ещё раз через пару минут"
                                         " (особенность Telegram)</code>\n\n"
                                         "Нажмите на кнопку ниже 👇",
                                         call.message.chat.id, call.message.message_id,
                                         reply_markup=sub_link_private_inline)
    else:
        await call.bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, "<b>У вас нет активных подписок!</b>")


async def sub_link_open(call: CallbackQuery):
    if db.get_sub_status(call.from_user.id):
        await call.bot.edit_message_text("✅ Вход открыт, вступайте (нажмите на кнопку ниже):",
                                         call.message.chat.id, call.message.message_id,
                                         reply_markup=sub_link_open_inline)
        time.sleep(4)
        await call.bot.edit_message_text("<b>Ваши приватные ссылки для доступа</b> 👇\n\n"
                                         "<code>⚠ Если у вас появляется ошибка ссылка не действительна"
                                         " или чат не существует или вы не можете войти "
                                         "в сообщество, просто попробуйте ещё раз через пару минут"
                                         " (особенность Telegram)</code>\n\n"
                                         "Нажмите на кнопку ниже 👇",
                                         call.message.chat.id, call.message.message_id,
                                         reply_markup=sub_link_private_inline)
    else:
        await call.bot.delete_message(call.from_user.id, call.message.message_id)
        await call.bot.send_message(call.from_user.id, "<b>У вас нет активных подписок!</b>")


def register_private_link(dp: Dispatcher):
    dp.register_callback_query_handler(
        sub_link_private, IsBanFilter(),
        text='sublink',
        state="*",
    )
    dp.register_callback_query_handler(
        sub_link_open, IsBanFilter(), text='subprivatelink',
        state="*"
    )