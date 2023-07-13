from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.config import ADMIN_IDS
from tgbot.misc.states import FeedbackState


async def send_message(message: Message, state: FSMContext):
    await state.update_data(user_message=message.text)
    data = await state.get_data()
    user_message = data.get('user_message')
    for admin in ADMIN_IDS:
        await message.bot.send_message(admin, f"Получено новое соощение от пользователя: {user_message}")
    await state.finish()
    await message.answer("Вопрос отправлен, ожидайте ответа")


def register_feedback_handlers(dp: Dispatcher):
    dp.register_message_handler(
        send_message,
        state=FeedbackState.waiting_for_message
    )