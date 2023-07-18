import asyncio
import datetime
import logging
import time

from aiogram import Bot, types, Dispatcher
from aiogram.types import Message
from aiogram.utils import executor

from tgbot.config import db, time_sub_day, CHAT_BOT_TOKEN, storage

logger = logging.getLogger(__name__)


logging.basicConfig(
    level=logging.INFO,
    format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
)
logger.info("Starting bot")

bot = Bot(CHAT_BOT_TOKEN, parse_mode='HTML')
dp = Dispatcher(bot, storage)


@dp.message_handler()
async def check_user(message: Message):
    user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
    if user_sub is False:
        await message.reply(f'Пользователь: <b>{message.from_user.full_name}</b> был кикнут.\nПричина: <b>Кончился срок подписки</b>')
        return await remove_user(chat_id=message.chat.id, user_id=message.from_user.id)


@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_chat_members(message: Message):
    user_sub = time_sub_day(db.get_time_sub(message.from_user.id))
    user_sub_time = db.get_time_sub(message.from_user.id)

    for user in message.new_chat_members:
        if user_sub is False:
            await message.reply(
                f'Пользователь: {message.from_user.full_name} был кикнут.\nПричина: <b>Кончился срок подписки</b>')
            return await remove_user(chat_id=message.chat.id, user_id=user.id)
        time_now = int(time.time())
        middle_time = int(user_sub_time) - time_now
        duration = datetime.timedelta(seconds=middle_time)
        finish_time = datetime.datetime.now() + duration
        await message.reply(f'Добро пожаловать <b>{message.from_user.full_name}</b>!\n'
                            f'У вас активная подписка до {finish_time.replace(microsecond=0)}')
        await schedule_user_removal(user.id, message.chat.id, finish_time)


async def remove_user(user_id: int, chat_id: int):
    await bot.kick_chat_member(chat_id=chat_id, user_id=user_id)


async def schedule_user_removal(user_id: int, chat_id: int, finish_time: datetime.datetime):
    await asyncio.sleep((finish_time - datetime.datetime.now()).total_seconds())
    await remove_user(user_id, chat_id)


if __name__ == '__main__':
    executor.start_polling(dp)
