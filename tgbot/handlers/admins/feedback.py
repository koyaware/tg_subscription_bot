import re

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from tgbot.config import ADMIN_IDS, connect_to_redis
from tgbot.filters.is_ban import IsBanFilter
from tgbot.misc.keyboards import feedback_inline, cancel_inline
from tgbot.misc.states import FeedbackState


async def send_message(message: Message, state: FSMContext):
    for admin in ADMIN_IDS:
        if message.text == "💻 Мои подписки":
            await message.answer("Действие отменено.")
            return await state.finish()
        elif message.text == "❤ Тарифы":
            await message.answer("Действие отменено.")
            return await state.finish()
        elif message.text == "📨 Обратная связь":
            await message.answer("Действие отменено.")
            return await state.finish()
        elif message.text == "📨 Чат":
            await message.answer("Действие отменено.")
            return await state.finish()
        await message.bot.copy_message(chat_id=admin, from_chat_id=message.from_user.id, message_id=message.message_id)
        await message.bot.send_message(admin, f"🔺🔺🔺"
                                              f"\nПользователь: @{message.from_user.username}, <b>{message.from_user.first_name}</b>\n"
                                              f"[ID:{message.from_user.id}] оставил вопрос.", reply_markup=feedback_inline)
    await message.answer("Вопрос отправлен, ожидайте ответа")
    await state.finish()
    redis_pool = await connect_to_redis()
    await redis_pool.set(name='user_id', value=message.from_user.id)


async def feedback_user(call: CallbackQuery):
    await call.bot.send_message(call.from_user.id, "Отправьте ответ на вопрос. "
                                                   "Это может быть текст, фото, видео или любое другое медиавложение: ",
                                reply_markup=cancel_inline)
    await FeedbackState.waiting_for_admin_message.set()


async def feedback_user_state(message: Message, state: FSMContext):
    redis_pool = await connect_to_redis()
    user_id = await redis_pool.get(name='user_id')
    numbers_only = re.sub(r'\D', '', user_id.decode())
    await message.bot.send_message(numbers_only, 'Вам пришло сообщение от администратора: ')
    await message.bot.send_message(numbers_only, message.text)
    await message.bot.send_message(message.from_user.id, 'Сообщение было отправлено.')
    await state.finish()


async def cancel_button(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.bot.delete_message(call.from_user.id, call.message.message_id)
    await call.bot.send_message(call.from_user.id, "Действие отменено.")


def register_feedback_handlers(dp: Dispatcher):
    dp.register_message_handler(
        send_message, IsBanFilter(),
        state=FeedbackState.waiting_for_message,
        content_types=["text", "sticker", "pinned_message", "photo", "audio", "document", "animation ", "video",
                       "voice", "has_media_spoiler", "contact", "location"]
    )
    dp.register_callback_query_handler(
        feedback_user, IsBanFilter(), text="feedback_user", state='*'
    )
    dp.register_message_handler(
        feedback_user_state, IsBanFilter(),
        state=FeedbackState.waiting_for_admin_message,
        content_types=["text", "sticker", "pinned_message", "photo", "audio", "document", "animation ", "video",
                       "voice", "has_media_spoiler", "contact", "location"]
    )
    dp.register_callback_query_handler(
        cancel_button, IsBanFilter(), text="cancelbutton", state='*'
    )